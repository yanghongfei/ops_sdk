#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : ss
date   : 2018年4月12日
role   : 工具类
"""

import sys
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def bytes_to_unicode(input_bytes):
    if sys.version_info.major >= 3:
        return str(input_bytes, encoding='utf-8')
    else:
        return (input_bytes).decode('utf-8')


def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)
    return data


def check_password(data):
    return True if re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", data) and len(data) >= 8 else False


class Executor(ThreadPoolExecutor):
    """ 线程执行类 """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=10)
        return cls._instance


def exec_shell(cmd):
    '''执行shell命令函数'''
    sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = sub.communicate()
    ret = sub.returncode
    if ret == 0:
        return ret, stdout.decode('utf-8').split('\n')
    else:
        return ret, stdout.decode('utf-8').replace('\n', '')
