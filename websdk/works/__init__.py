#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
author : shenshuo
date   : 2018年6月15日
role   : 任务调用
"""

import json
import requests
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.gen import coroutine


class SubmitJob:
    def __init__(self, task_url, auth_key):
        self.task_url = task_url
        req = requests.get(self.task_url, cookies=dict(auth_key=auth_key))
        csrf_key = json.loads(req.text)['csrf_key']
        self.cookies = dict(auth_key=auth_key, csrf_key=csrf_key)

    def post_task(self, temp_id, exec_hosts, submitter, task_name, task_args='{}', exec_time=None, task_schedule='new',
                  details=None):

        the_body = json.dumps({"task_name": task_name, "temp_id": temp_id, "args": str(task_args),
                               "details": details, "hosts": str(exec_hosts), "submitter": submitter,
                               "exec_time": exec_time, "schedule": task_schedule})
        req = requests.post(self.task_url, data=the_body, cookies=self.cookies)
        req_code = json.loads(req.text)['status']
        if req_code != 0:
            print('submit task filed !!!')
            exit(-111)
        else:
            print('success !!!')
            return


@coroutine
def fetch_coroutine(url, method='GET', body=None, **kwargs):
    request = HTTPRequest(url, method=method, body=body, connect_timeout=5, request_timeout=10)
    http_client = AsyncHTTPClient(**kwargs)
    response = yield http_client.fetch(request)
    body = json.loads(response.body)
    return body


#req = yield Task(fetch_coroutine, url, method='POST', body=the_body)