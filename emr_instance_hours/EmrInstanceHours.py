"""Get EMR Instance Hours"""

import lib.cwl.metric_data as md

import boto3
from botocore.exceptions import ClientError
import time
import sys

__author__ = 'Tobias Braecker'


class EmrInstanceHours:
    def __init__(self):
        self.client = boto3.client('emr')

    def get_clusters(self):
        print("Task: Getting EMR clusters from AWS")

        try:
            return self.client.list_clusters(ClusterStates=['RUNNING'])
        except Exception as e:
            print("Unexpected client error: %s" % e)

    def get_cluster_ids(self, clusters):
        print("Task: Extract Cluster ID's")
        if not clusters:
            print("Info: There are no running clusters. Exit program now")
            sys.exit(0)

        return(x['Id'] for x in clusters['Clusters'])

    def get_cluster_information(self, cluster_ids):
        print("Task: Get Cluster information from AWS via Cluster ID")

        cwl_metric_list = []
        cwl_dimension_list = []

        for x in cluster_ids:
            while True:
                try:
                    cluster_inf_dict = \
                        self.client.describe_cluster(ClusterId=x)
                    break
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ThrottlingException':
                        print(e.response['Error']['Code'] +
                              ': wait a few seconds and try again')
                        time.sleep(5)
                except Exception as e:
                    print("Unexpected client error: %s" % e)

            cwl_metric_dict = {}
            cwl_dimension_dict = {}

            cwl_metric_dict['Value'] = \
                cluster_inf_dict['Cluster']['NormalizedInstanceHours']

            cwl_dimension_dict['Name'] = 'Clustergroup'
            cwl_dimension_dict['Value'] = 'NOT_SET'

            for y in cluster_inf_dict['Cluster']['Tags']:
                if y['Key'] == '<YOUR TAG>':
                    cwl_dimension_dict['Value'] = y['Value']

            cwl_metric_list.append(cwl_metric_dict)
            cwl_dimension_list.append(cwl_dimension_dict)
        return cwl_metric_list, cwl_dimension_list


if __name__ == '__main__':
    emr = EmrInstanceHours()
    metrics = md.MetricData()

    cwl_metric_list, cwl_dimension_list = \
        emr.get_cluster_information(emr.get_cluster_ids(emr.get_clusters()))

    metrics.put_with_dim(cwl_metric_list, cwl_dimension_list, '<YOUR '
                                                              'NAMESPACE>',
                         'NormalizedInstanceHours')
    metrics.put_without_dim(cwl_metric_list, '<YOUR NAMESPACE>',
                            'NormalizedInstanceHours')
