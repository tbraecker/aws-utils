import csv

__author__ = 'Tobias Braecker'


class DeadUsersCheck:
    def __init__(self, path):
        self.path = path

    def find(self):
        d_list = []
        with open(self.path + '/user.csv', 'r') as f_user:
            input_file = csv.DictReader(f_user)
            for row in input_file:
                if (row['access_key_1_active'] == 'false' and
                        row['access_key_2_active'] == 'false' and
                        row['password_enabled'] == 'false'):
                    d_list.append(row['user'])
        return d_list

    def out(self, d_list):
        if d_list:
            d_list_sorted = sorted(d_list)

            print('STATUS DEAD USER CHECK : RED')
            print('----------------------------')
            print('{:20}'.format('users without access_keys and password'))
            for row in d_list_sorted:
                print('{:20}'.format(row))
            print('')
        else:
            print('STATUS DEAD USER CHECK : GREEN')
            print('------------------------------')
            print('')
