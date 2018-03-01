import boto3
from botocore.exceptions import ClientError
import time

__author__ = 'Tobias Braecker'


class CredentialReport:
    def __init__(self, path):
        self.path = path
        self.client = boto3.client('iam')

    def generate(self):
        status = self.client.generate_credential_report()
        while status['State'] != 'COMPLETE':
            print('wait to finish report generation')
            time.sleep(10)
            status = self.client.generate_credential_report()

    def get(self):
        try:
            response = self.client.get_credential_report()
        except ClientError as e:
            print("Unexpected client error: %s" % e)

        response_list = response['Content'].splitlines()

        try:
            f_user = open(self.path + '/user.csv', 'a+')
            for row in response_list:
                print(row.decode("utf-8"), file=f_user)
            f_user.close()
        except Exception as e:
            print("Unexpected Exception: %s" % e)
