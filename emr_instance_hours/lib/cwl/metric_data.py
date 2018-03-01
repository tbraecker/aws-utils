"""Put metric data to cloudwatch"""

import boto3

__author__ = 'Tobias Braecker'
__version__ = '2.0'


class MetricData:
    def __init__(self):
        self.client = boto3.client('cloudwatch')

    def put_with_dim(self, cwl_metric_list, cwl_dimension_list, namespace,
                     metric_name):
        """
        Description:
            Iterate through cwl_metric_list and cwl_dimension_list in parallel
            to get the information and put the cloudwatch metric.
        Parameters:
            cwl_metric_list: List of dicts with metric_values
            cwl_dimension_list: List of dicts with metric_dimenions
            namespace
            metric_name
        """
        print("Task: Put Metrics with dimension to AWS Cloudwatch")

        for x, y in zip(cwl_metric_list, cwl_dimension_list):
            try:
                self.client.put_metric_data(
                    Namespace=namespace,
                    MetricData=[
                        {
                            'MetricName': metric_name,
                            'Dimensions': [y],
                            'Value': x['Value'],
                            'Unit':'None'
                        }
                    ]
                )
            except Exception as e:
                print("Unexpected client error: %s" % e)

    def put_without_dim(self, cwl_metric_list, namespace, metric_name):
        """
        Description:
            Iterate through cwl_metric_list to get the information
            and put the cloudwatch metric.
        Parameters:
            cwl_metric_list: List of dicts with metric_values
            namespace
            metric_name
        """

        print("Task: Put Metrics without dimension to AWS Cloudwatch")

        for x in cwl_metric_list:
            try:
                self.client.put_metric_data(
                    Namespace=namespace,
                    MetricData=[
                        {
                            'MetricName': metric_name,
                            'Value': x['Value'],
                            'Unit':'None'
                        }
                    ]
                )
            except Exception as e:
                print("Unexpected client error: %s" % e)
