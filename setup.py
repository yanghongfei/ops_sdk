#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2018年2月5日13:37:54
role   : 运维SDK
'''
from distutils.core import setup

setup(
    name='opssdk',
    version='0.0.3',
    packages=['opssdk', 'opssdk.logs', 'opssdk.operate', 'opssdk.install','opssdk.get_info'],
    url='http://baidu.com',
    license='',
    install_requires=['fire==0.1.2', 'shortuuid==0.5.0', 'pycrypto==2.6.1', 'PyMySQL==0.7.11', 'salt==2017.7.2',
                      'requests==2.18.4'],
    author='shenshuo',
    author_email='191715030@qq.com',
    description='SDK of the operation and maintenance script'
                'logs'
                'operate'
)
