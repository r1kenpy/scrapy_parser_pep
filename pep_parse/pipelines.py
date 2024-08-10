# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from collections import defaultdict
from datetime import datetime as dt

from pep_parse.settings import BASE_DIR, RESULTS_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.number_statuses = defaultdict(int)
        self.result_dir = BASE_DIR / RESULTS_DIR
        self.result_dir.mkdir(exist_ok=True)

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
            fieldnames = ('status', 'quantity')
            w = csv.DictWriter(f, dialect=csv.excel, fieldnames=fieldnames)
            w.writeheader()
            for k, v in self.number_statuses.items():
                w.writerow({fieldnames[0]: k, fieldnames[1]: v})
