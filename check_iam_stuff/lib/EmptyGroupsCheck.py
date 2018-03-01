import csv
import boto3

__author__ = 'Tobias Braecker'


class EmptyGroupsCheck:
    def __init__(self, path):
        self.path = path

    def get_lists(self):
        group_list = []
        user_groups_list = []
        user_list = []
        client = boto3.client('iam')

        r_all_groups = client.list_groups()
        for row in r_all_groups['Groups']:
            group_list.append(row['GroupName'])

        with open(self.path + '/user.csv','r') as f_user:
            input_file = csv.DictReader(f_user)
            for row in input_file:
                user_list.append(row['user'])

        for row in user_list:
            if row != '<root_account>':
                r_user_groups = client.list_groups_for_user(UserName=row)
                for group in r_user_groups['Groups']:
                    user_groups_list.append(group['GroupName'])

        return group_list, user_groups_list

    def find(self, group_list, user_groups_list):
        dead_list = []

        for row in group_list:
            if row not in user_groups_list:
                dead_list.append(row)
        return dead_list

    def out(self, dead_list):
        if dead_list:
            dead_list_sorted = sorted(dead_list)

            print('STATUS EMPTY GROUPS CHECK : RED')
            print('-------------------------------')
            print('{:20}'.format('Following groups are empty'))
            for row in dead_list_sorted:
                print('{:20}'.format(row))
            print('')
        else:
            print('STATUS EMPTY GROUPS CHECK : GREEN')
            print('----------------------------------')
            print('')
