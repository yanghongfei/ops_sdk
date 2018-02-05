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
    version='0.0.2',
    packages=['opssdk','opssdk.logs','opssdk.operate','opssdk.install'],
    url='http://baidu.com',
    license='',
    install_requires=['fire==0.1.2','shortuuid==0.5.0','pycrypto==2.6.1'],
    author='shenshuo',
    author_email='191715030@qq.com',
    description='SDK of the operation and maintenance script' 
                'logs'
                'install'
)
