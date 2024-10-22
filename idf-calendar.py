import requests
import arrow
from ics import Calendar, Event
import re

ical_url = 'https://idfeulatam2.bamboohr.com/feeds/feed.php?id=629d07619116cbc01491f8a34191e683'
holiday_urls = {
        'BY': 'https://calendar.google.com/calendar/ical/en.by%23holiday%40group.v.calendar.google.com/public/basic.ics',
        'PL': 'https://calendar.google.com/calendar/ical/en.polish%23holiday%40group.v.calendar.google.com/public/basic.ics',
        'ES': 'https://calendar.google.com/calendar/ical/en.spain%23holiday%40group.v.calendar.google.com/public/basic.ics'
}

def fetch_ical(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Calendar(response.text)
    else:
        raise Exception(f"Failed to fetch iCal data: {response.status_code}")


def filter_ical_events(ical_data, keywords):
    filtered_events = []
    for event in ical_data.events:
        for keyword in keywords:
            if keyword.lower() in event.name.lower():
                filtered_events.append(event)
    return filtered_events


def create_filtered_ical(filtered_events):
    cal = Calendar()
    for event in filtered_events:
        cal.events.add(event)
    return cal

def filter_by_policy(employees, policy):
    result = []
    for name in employees:
        if employees[name] == policy:
            result.append(name)
    return result

def create_holidays_events(employees, policy):
    result = []
    holidays = fetch_ical(holiday_urls[policy])
    employees = filter_by_policy(employees, 'PL')
    min_date = arrow.now().shift(days=-100)
    max_date = arrow.now().shift(days=365)
    for employee in employees:
        for holiday in holidays.events:
            if holiday.begin > min_date and holiday.begin < max_date:
                event = Event()
                event.name = employee
                event.begin = holiday.begin
                event.end = holiday.end
                event.uid = employee.lower() + '_' + holiday.uid
                event.created = holiday.created
                event.last_modified = holiday.last_modified
                event.description = holiday.description
                result.append(event)
    return result

if __name__ == "__main__":
    ical_data = fetch_ical(ical_url)
    employees = {
            'Pavel Mukashev': 'ES',
            'Darya Pesnyak': 'PL',
            'Vladislav Artsiukh': 'PL',
            'Sergey Zhabinskiy': 'PL',
            'Anton Shtabnoy': 'BY',
            'Vladislav Goncharenko': 'BY',
            'Petr Shamburov': 'PL',
            'Anastasiya Mikulskaya': 'BY',
            'Karina Mihey': 'PL',
            'Sergei Mikhailovskii': 'PL',
            'Slatvinskiy Egor': 'BY',
            'Darya Mihalik': 'BY',
            'Evgeny Kuntsevich': 'PL',
            'Nikita Prokopenko': 'BY',
            'Polina Belous': 'PL',
            'Vitaly Burim': 'BY',
            'Aleksandr Pashchenko': 'BY',
            'Evgeniy Solovey': 'BY',
            'Klimov Vasiliy': 'BY',
            'Ekaterina Daineko': 'PL'
    }
    filtered_events = filter_ical_events(ical_data, employees.keys())
    filtered_events += create_holidays_events(employees, 'BY')
    filtered_events += create_holidays_events(employees, 'PL')
    filtered_events += create_holidays_events(employees, 'ES')
    filtered_ical = create_filtered_ical(filtered_events)
    with open('filtered_calendar.ics', 'w') as f:
        f.writelines(filtered_ical.serialize_iter())


