"""execute a select statement on a database via AWS lambda"""

import os
import sys
import pymysql
import json
import datetime
import rds_config

__author__ = 'Tobias Braecker'

def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def main(event,context):
    # db connection vars
    db_host = rds_config.db_host
    db_name = rds_config.db_name
    db_user = rds_config.db_user
    db_pass = rds_config.db_pass

    # get sql information from lambda call
    columns = event['columns']
    tables = event['tables']
    conditions = event['conditions']

    # db connection and update
    try:
        dbc = pymysql.connect(db_host, user=db_user, passwd=db_pass, db=db_name )
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    with dbc.cursor() as cursor:
        cursor.execute('SELECT ' + columns + ' FROM ' + tables + ' WHERE ' +
                       conditions)
        result = cursor.fetchall()
        dbc.commit()
        dbc.close()
        return json.dumps(result, default = datetime_converter)

