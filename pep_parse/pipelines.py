import csv
from collections import defaultdict
from datetime import datetime as dt

from pep_parse.settings import BASE_DIR, RESULTS_DIR


class PepParsePipeline:

    def __init__(self):
        self.result_dir = BASE_DIR / RESULTS_DIR
        self.result_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.number_statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.number_statuses[item['status']] += 1
        return item

    def close_spider(self, spider):
        with open(
            self.result_dir / f'status_summary_'
            f'{dt.now().strftime("%d-%m-%Y_%H:%M:%S")}.csv',
            'w',
            encoding='utf-8',
        ) as f:
            csv.writer(
                f,
                dialect=csv.excel,
                quoting=csv.QUOTE_NONE).writerows(
                [('Статус', 'Количество'),
                 *self.number_statuses.items(),
                 ('Всего', sum(self.number_statuses.values()))]
            )
