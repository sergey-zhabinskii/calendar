import requests
import re

ical_url = 'https://idfeulatam2.bamboohr.com/feeds/feed.php?id=629d07619116cbc01491f8a34191e683'

def fetch_ical(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch iCal data: {response.status_code}")


def filter_ical_events(ical_data, keywords):
    filtered_events = []
    events = re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', ical_data, re.DOTALL)
    for event in events:
        for keyword in keywords:
            if keyword.lower() in event.lower():
                filtered_events.append(event)
    return filtered_events


def create_filtered_ical(filtered_events):
    ical_header = 'BEGIN:VCALENDAR\nVERSION:2.0\n'
    ical_footer = 'END:VCALENDAR\n'
    ical_body = ''
    for event in filtered_events:
        ical_body += f'BEGIN:VEVENT{event}END:VEVENT\n'
    return ical_header + ical_body + ical_footer

if __name__ == "__main__":
    ical_data = fetch_ical(ical_url)
    search_keywords = [
            'Petr Shamburov',
            'Vladislav Goncharenko',
            'Anton Shtabnoy',
            'Sergey Zhabinskiy',
    ]
    filtered_events = filter_ical_events(ical_data, search_keywords)
    filtered_ical = create_filtered_ical(filtered_events)
    with open('filtered_calendar.ics', 'w') as f:
        f.write(filtered_ical)


