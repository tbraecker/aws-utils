import csv
import operator
from . import DateCalc as Dc

__author__ = 'Tobias Braecker'


class PasswordCheck:
    def __init__(self, period, path):
        self.period = period
        self.path = path

    def last_used(self):
        p_list = []
        date_calc = Dc.DateCalc()
        with open(self.path + '/user.csv') as f_user:
            input_file = csv.DictReader(f_user)
            for row in input_file:
                try:
                    diff = date_calc.diff(row['password_last_used'])
                    if diff.days > self.period:
                        p_list.append([row['user'], diff.days])
                except ValueError:
                    continue
        return p_list

    def out(self, p_list):
        if p_list:
            p_list_sorted = sorted(p_list, key=operator.itemgetter(1))

            print('STATUS PASSWORD CHECK : RED')
            print('---------------------------')
            print('{:20} {:20}'.format('user', 'pass_last_used'))
            for i in range(0,len(p_list_sorted)):
                print('{:20} {:1}'.format(p_list_sorted[i][0],
                                          p_list_sorted[i][1]))
            print('')
        else:
            print('STATUS PASSWORD CHECK : GREEN')
            print('-----------------------------')
            print('')
