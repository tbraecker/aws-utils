import csv
import boto3

__author__ = "Tobias Braecker"


class MfaCheck:
    def __init__(self, path):
        self.path = path

    def find_mfa(self):
        user_list = []
        with open(self.path + '/user.csv','r') as f_user:
            input_file = csv.DictReader(f_user)
            for row in input_file:
                if row['mfa_active'] == 'false':
                    user_list.append(row['user'])

        return user_list

    def get_admin(self, user_list):
        group_list = []
        client = boto3.client('iam')
        for row in user_list:
            if row == '<root_account>':
                group_list.append(row)
            else:
                response = client.list_groups_for_user(UserName=row)
                for group in response['Groups']:
                    if group['GroupName'] == 'Account_Admin':
                        group_list.append(row)
        return group_list

    def out(self, user_list):
        if user_list:
            user_list_sorted = sorted(user_list)

            print('STATUS MFA AUTH CHECK : RED')
            print('----------------------------')
            print('{:20}'.format('admins without mfa protection'))
            for row in user_list_sorted:
                print('{:20}'.format(row))
            print('')
        else:
            print('STATUS MFA AUTH CHECK : GREEN')
            print('------------------------------')
            print('')
