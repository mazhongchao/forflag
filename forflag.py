#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess


def run():
    today = time.strftime("%Y-%m-%d", time.localtime())
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    with open('/data/projects/testflag/last-commit.txt', 'r+') as f:
        text = f.read()
        f.seek(0)

        text_list = text.split('|')
        date = text_list[0]
        stat = text_list[1]

        if date == today and stat == '1':
            return

        with open('/data/projects/testflag/README.md', 'a+') as ff:
            ff.write(f"{now} commit\n")

        cmd_list = ["cd /data/projects/testflag/forflag",
                    "git add README.md",
                    "git commit -m 'update'",
                    'git push origin main']

        # ret是类subprocess.CompletedProcess对象:
        # (args, returncode(0=成功), stdout子进程的输出, stderr子进程错误, check_returncode())
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

