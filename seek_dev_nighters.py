from datetime import datetime
import json
import requests

from pytz import timezone


def _main():
    midnighters = get_midnighters(fetch_attempts())
    for midnighter in sorted(midnighters):
        print(midnighter)


def fetch_attempts():
    page_num = 1
    while True:
        attempts_page = json.loads(fetch_attempts_page(page_num))
        for record in attempts_page['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }
        if page_num == attempts_page['number_of_pages']:
            break
        else:
            page_num += 1


def fetch_attempts_page(page):
    return requests.get(
        'https://devman.org/api/challenges/solution_attempts/',
        params={'page': page}
    ).text


def get_midnighters(attempts):
    midnighters = set()
    midnight = 0
    working_hours_start = 6

    for attempt in attempts:
        attempt_dt = datetime.fromtimestamp(
            attempt['timestamp'],
            timezone(attempt['timezone'])
        )
        if midnight < attempt_dt.hour < working_hours_start:
            midnighters.add(attempt['username'])

    return list(midnighters)


if __name__ == '__main__':
    _main()
