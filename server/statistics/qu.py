import signal
import sys
import time
import json
from requests import get
from datetime import date, datetime
from openpyxl import Workbook


def get_conf() -> tuple:
    file_conf = open('config.json', 'r')
    conf = json.load(file_conf)
    file_conf.close()
    domain = conf.pop('domain')
    routes = [["30.214610,60.003559~30.338024,60.012473", "30.338024,60.012473~30.214610,60.003559"]]
    return domain, conf, routes


def get_price(url: str, params: dict) -> list:
    now = datetime.now()
    timestamp = f'{now.hour}:{now.minute}'
    try:
        response = get(url, params=params)
        content = response.json()
        data_list = [int(content.get('time')),
                     int(content.get('options')[0].get('min_price')),
                     int(content.get('options')[0].get('price')),
                     timestamp]
        return data_list
    except Exception as e:
        print(e)
        return [0, 0, 0, timestamp]


def write_data(book: Workbook(), row: int, data: list) -> None:
    book.append(data)


def main_function(url, params, routes):
    wb = Workbook()
    now = datetime.now()

    ws_forth = wb.create_sheet('forth')
    ws_back = wb.create_sheet('back')
    timestamp_start = f'{now.hour}-{now.minute}'

    def signal_handler(*args):
        now = datetime.now()
        timestamp_end = f'{now.hour}-{now.minute}'
        wb.save(f"data/{str(date.today())} data({timestamp_start} {timestamp_end}).xlsx")
        sys.exit()

    signal.signal(signal.SIGINT, signal_handler) # Or whatever signal

    row = 1
    while True:
        for route in routes:
            params["rll"] = route[0]
            result = get_price(url, params)
            print(result)
            write_data(ws_forth, row, result)

            params["rll"] = route[1]
            result = get_price(url, params)
            print(result)
            write_data(ws_back, row, result)
        row += 1
        time.sleep(60)


if __name__ == '__main__':
    a, b, c = get_conf()
    main_function(a, b, c)
