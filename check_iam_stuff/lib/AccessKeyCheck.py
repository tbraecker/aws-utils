import csv
from . import DateCalc as Dc

__author__ = "Tobias Braecker"


class AccessKeyCheck:

    def __init__(self, period, path):
        self.period = period
        self.path = path

    def last_used(self):
        a_list = []
        date_calc = Dc.DateCalc()

        with open(self.path + '/user.csv', 'r') as f_user:
            input_file = csv.DictReader(f_user)
            for row in input_file:
                if row['access_key_1_active'] == 'true':
                    if row['access_key_1_last_used_date'] != 'N/A':
                        diff = \
                            date_calc.diff(row['access_key_1_last_used_date'])
                        if diff.days > self.period:
                            a_list.append([row['user'],
                                           'access_key_1',
                                           diff.days])
                    else:
                        a_list.append([row['user'],
                                       'access_key_1',
                                       row['access_key_1_last_used_date']])
                if row['access_key_2_active'] == 'true':
                    if row['access_key_2_last_used_date'] != 'N/A':
                        diff = \
                            date_calc.diff(row['access_key_2_last_used_date'])
                        if diff.days > self.period:
                            a_list.append([row['user'],
                                           'access_key_2',
                                           diff.days])
                    else:
                        a_list.append([row['user'],
                                       'access_key_2',
                                       row['access_key_1_last_used_date']])
        return a_list

    def out(self, a_list):
        if a_list:
            a_list_sorted = sorted(a_list, key=lambda x: str(x[2]))
            print('STATUS ACCESS KEY CHECK : RED')
            print('-----------------------------')
            print('{:20} {:20} {:20}'.format('user',
                                             'access_key',
                                             'last_used'))
            for i in range(0,len(a_list_sorted)):
                print('{:20} {:20} {:1}'.format(a_list_sorted[i][0],
                                                a_list_sorted[i][1],
                                                a_list_sorted[i][2]))
        else:
            print('STATUS ACCESS KEY CHECK : GREEN')
            print('-------------------------------')
        print('')
