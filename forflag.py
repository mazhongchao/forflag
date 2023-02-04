#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess


def run():
    today = time.strftime("%Y-%m-%d", time.localtime())

    with open('/Users/mach/projects/forflag/last-commit.txt', 'r+') as f:
        text = f.read()
        text_list = text.split('|')
        date = text_list[0]
        stat = text_list[1]

        if date == today and stat == '1':
            return

        cmd_list = ["git add .", "git commit -m 'update'", 'git push origin main']

        # ret是类subprocess.CompletedProcess对象(args, returncode(0=成功), stdout子进程输出, stderr,check_returncode()
        ret = subprocess.run(cmd_list,
          shell = True,
          timeout = 10,
          stdout = subprocess.PIPE,
          stdin = subprocess.PIPE)

        if ret.returncode == 0:
            f.write(f"{today}|1")
        else:
            f.write(f"{today}|0")


if __name__ == "__main__":

    run()

