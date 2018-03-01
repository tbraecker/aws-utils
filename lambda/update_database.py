#!/usr/bin/python
"""update database with a specified update statement"""

import os
import sys
import pymysql
import datetime
import rds_config

__author__ = 'Tobias Braecker'


def main(event, context):
    # db connection vars
    db_host = rds_config.db_host
    db_name = rds_config.db_name
    db_user = rds_config.db_user
    db_pass = rds_config.db_pass
    db_tab = rds_config.db_tab

    time = os.environ['starttime']
    checkpoint = os.environ['checkpoint']
    timecheck = '{:%H:%M:%S}'.format(datetime.datetime.now())
    timestamp = '{:%Y-%m-%d ' + time + '}'.format(datetime.datetime.now())

    # timecheck exceeds checkpoint
    if timecheck > checkpoint:
        timestamp = ('{:%Y-%m-%d ' + time + '}').format(
            datetime.datetime.now() + datetime.timedelta(days=1))

    print(timestamp)

    # db connection and update
    try:
        dbc = pymysql.connect(db_host, user=db_user, passwd=db_pass,
                              db=db_name)
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    with dbc.cursor() as cursor:
        cursor.execute("""<UPDATE STATEMENT>""", [timestamp])
        dbc.commit()
        dbc.close()
