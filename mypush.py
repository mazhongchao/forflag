#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import ssl
import json
import time
import datetime
import subprocess

from urllib import request

from setting import baseurl

def utc_to_local_str(utc_time_str):
    utc_datetime = datetime.datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
    local_datetime = utc_datetime + datetime.timedelta(hours=8)
    local_datedate_str = datetime.datetime.strftime(local_datetime ,'%Y-%m-%d %H:%M:%S')

    return local_datedate_str

    # utc_time_str = "2017-07-28T08:28:47.776Z"
    # UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    # utc_time = datetime.datetime.strptime(utc_time_str, UTC_FORMAT)
    # local_time = utc_time + datetime.timedelta(hours=8)
    # return local_time

def run():

    github_api = "https://api.github.com/users/mazhongchao/events?page=1&per_page=30"
    context = ssl._create_unverified_context()

    with request.urlopen(github_api, context=context) as r:
        data = r.read()

        data_list = json.loads(data.decode('utf-8'))

        a = []
        for event in data_list:

            utc = event['created_at']
            utc_date = utc.split('T')[0]
            local_time = utc_to_local_str(utc)
            local_date = local_time.split(' ')[0]

            if event['type'] == "PushEvent":
                s = (utc, utc_date, local_date, event['repo']['name'])
                a.append(s)

        print("UTC-TIME              ", "UTC-DATE    ", "Local date", "Repo")
        for one in a:
            print(one[0], " ", one[1], " ", one[2], one[3])


if __name__ == "__main__":

    run()

