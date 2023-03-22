#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import ssl
import json
import time
import subprocess

from urllib import request

from setting import baseurl


def run():

    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    today_date = now.split(' ')[0]

    github_api = "https://api.github.com/users/mazhongchao/events?page=1&per_page=30"

    readme_text = ""

    ssl._create_default_https_context = ssl._create_unverified_context
    context = ssl._create_unverified_context()
    with request.urlopen(github_api, context=context) as r:
        data = r.read()

        data_list = json.loads(data.decode('utf-8'))

        has_flag = False
        for event in data_list:

            if event['type'] == "PushEvent":

                create_date = event['created_at'].split('T')[0]
                if create_date == today_date:
                    print(f'[{now}] Already pushed at {create_date}.')
                    has_flag = True
                else:
                    readme_text = f'[{now}] Last push at {create_date}, need to push. '
                    print(f'[{now}] Last push at {create_date}, need to push')

                break

        if has_flag:
            return

    # This file will work when the repository is private,
    # in which case the GITHUB-API will not provide related events.
    with open(f'{baseurl}/last-push.txt', 'r+') as f:
        text = f.read()
        f.seek(0)

        text_list = text.split('|')
        date = text_list[0]
        stat = text_list[1]

        if date == today_date and stat == '1':
            print(f'[{now}] Already pushed at {create_date}.')
            return

        with open(f'{baseurl}/log.txt', 'a+') as ff:
            ff.write(f"{readme_text}Commits at {now}.\n")

        os.chdir(f"{baseurl}")
        cmd_list = ["git add log.txt",
                    "git commit -m 'update log'",
                    "git push origin main"]

        # ret is an object of the class subprocess.CompletedProcess:
        # (args, returncode(0=success), stdout(sub process output), stderr(sub process error), check_returncode())
        for idx, cmd in enumerate(cmd_list):
            ret = subprocess.run(cmd,
              shell = True,
              timeout = 10,
              stdout = subprocess.PIPE,
              stdin = subprocess.PIPE)
            print(ret.stdout, ret.stderr, ret.returncode)

            if idx == (len(cmd_list) - 1):
                f.truncate()
                if ret.returncode == 0:
                    f.write(f"{today_date}|1")
                else:
                    f.write(f"{today_date}|0")


if __name__ == "__main__":

    run()


