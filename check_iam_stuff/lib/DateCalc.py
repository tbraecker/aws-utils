from datetime import datetime

__author__ = 'Tobias Braecker'


class DateCalc:
    def diff(self, last_used):
        now = datetime.now()
        date_format = '%Y-%m-%d'
        last_used = datetime.strptime(last_used[0:10], date_format)
        now = datetime.strptime(str(now)[0:10], date_format)
        date_diff = now - last_used
        return date_diff
