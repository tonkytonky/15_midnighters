from datetime import datetime
import json
import requests

from pytz import utc, timezone


def _main():
    midnighters = get_midnighters(load_attempts(load_number_of_pages()))
    for midnighter in sorted(midnighters):
        print(midnighter)


def load_attempts(number_of_pages):
    for page_num in range(number_of_pages):
        shift = 1
        attempts_page = load_attempts_page(page_num + shift)
        for record in json.loads(attempts_page)['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def load_number_of_pages():
    return int(json.loads(load_attempts_page(1))['number_of_pages'])


def load_attempts_page(page):
    return requests.get(
        'https://devman.org/api/challenges/solution_attempts/',
        params={'page': page}
    ).text


def get_midnighters(attempts):
    midnighters = set()
    for attempt in attempts:
        utc_dt = utc.localize(datetime.utcfromtimestamp(attempt['timestamp']))
        local_tz = timezone(attempt['timezone'])
        local_dt = utc_dt.astimezone(local_tz)
        local_date = {
            'year': local_dt.year,
            'month': local_dt.month,
            'day': local_dt.day,
        }
        midnight = local_tz.localize(datetime(
            **local_date,
            hour=0,
            minute=0,
            second=0
        ))
        working_hours_start = local_tz.localize(datetime(
            **local_date,
            hour=9,
            minute=0,
            second=0
        ))
        if midnight < local_dt < working_hours_start:
            midnighters.add(attempt['username'])

    return list(midnighters)


if __name__ == '__main__':
    _main()
