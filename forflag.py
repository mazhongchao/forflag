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

    today = time.strftime("%Y-%m-%d", time.localtime())

    git_api = "https://api.github.com/users/mazhongchao/events?page=1&per_page=10"

    readme_text = ""
    #ssl._create_default_https_context = ssl._create_unverified_context
    context = ssl._create_unverified_context()
    with request.urlopen(git_api, context=context) as r:
        data = r.read()

        # print('Data:', (json.loads(data.decode('utf-8'))))
        data_list = json.loads(data.decode('utf-8'))
        for event in data_list:

            if event['type'] == "PushEvent":
                create_date = event['created_at'].split('T')[0]
                readme_text = f'Last push at {create_date}, need to push: '
                #if create_date == today:
                #    return
                #else:
                #    readme_text = f'Last push at {create_date}, need to push: '
                    # print(f'last push at {create_date}, need to push')
                    # exit(0)

    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # This file will work when the repository is private,
    # in which case the GITHUB-API will not provide related events.
    with open(f'{baseurl}/last-push.txt', 'r+') as f:
        text = f.read()
        f.seek(0)

        text_list = text.split('|')
        date = text_list[0]
        stat = text_list[1]

        if date == today and stat == '1':
            return

        with open(f'{baseurl}/log.txt', 'a+') as ff:
            ff.write(f"{readme_text}{now} commit.\n")

        cmd_list = [f"cd {baseurl}",
                    "git add log.txt",
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
            print(ret.stdout, ret.stderr)

            if idx == (len(cmd_list) - 1) and ret.returncode == 0:
                f.truncate()
                f.write(f"{today}|1")


if __name__ == "__main__":

    run()


