#!/usr/bin/env python
# -*-coding:utf-8-*-
""""
author : shenshuo
date   : 2018年2月5日13:37:54
desc   : 运维SDK
update : 添加tornado SDK
"""
from distutils.core import setup

setup(
    name='opssdk',
    version='0.0.6',
    packages=['opssdk', 'opssdk.logs', 'opssdk.operate', 'opssdk.install', 'opssdk.get_info', 'opssdk.utils', 'websdk'],
    url='https://github.com/ss1917/ops_sdk/',
    license='',
    install_requires=['fire', 'shortuuid', 'Crypto===1.4.1', 'PyMySQL==0.7.11', 'requests','tornado===5.0'],
    author='shenshuo',
    author_email='191715030@qq.com',
    description='SDK of the operation and maintenance script'
                'logs'
                'operate'
)
