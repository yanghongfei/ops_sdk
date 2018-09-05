#!/usr/bin/env python
# -*-coding:utf-8-*-

import json
from datetime import timedelta
import shortuuid
from .cache import get_cache
from tornado.web import RequestHandler, HTTPError
from tornado.gen import with_timeout, coroutine, TimeoutError
from .tools import Executor
from .db_context import DBContext
from .jwt_token import AuthToken
# from models.mg import Users, OperationRecord
from .my_verify import MyVerify


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        self.new_csrf_key = str(shortuuid.uuid())
        super(BaseHandler, self).__init__(*args, **kwargs)

    def prepare(self):

        # 验证客户端CSRF，如请求为GET，则不验证，否则验证。最后将写入新的key
        cache = get_cache()
        if self.request.method != 'GET':
            csrf_key = self.get_cookie('csrf_key')
            pipeline = cache.get_pipeline()
            result = cache.get(csrf_key, private=False, pipeline=pipeline)
            cache.delete(csrf_key, private=False, pipeline=pipeline)
            if result != '1':
                raise HTTPError(400, 'csrf error')

        cache.set(self.new_csrf_key, 1, expire=1800, private=False)
        self.set_cookie('csrf_key', self.new_csrf_key)

        ### 登陆验证
        auth_key = self.get_cookie('auth_key', None)
        if not auth_key:
            # 没登录，就让跳到登陆页面
            raise HTTPError(401, 'auth failed')

        else:
            auth_token = AuthToken()
            user_info = auth_token.decode_auth_token(auth_key)
            user_id = user_info.get('user_id', None)
            username = user_info.get('username', None)
            nickname = user_info.get('nickname', None)

            if not user_id:
                raise HTTPError(401, 'auth failed')
            else:
                user_id = str(user_id)
                self.set_secure_cookie("user_id", user_id)
                # self.set_cookie('enable_nickname', base64.b64encode(nickname.encode('utf-8')))
                self.set_secure_cookie("nickname", nickname)
                self.set_secure_cookie("username", username)
                my_verify = MyVerify(user_id)

        ### 如果不是超级管理员,开始鉴权
        if not self.is_superuser():

            # 没权限，就让跳到权限页面 0代表有权限，1代表没权限
            if my_verify.get_verify(self.request.method, self.request.uri) != 0:
                '''如果没有权限，就刷新一次权限'''
                my_verify.write_verify()

            if my_verify.get_verify(self.request.method, self.request.uri) != 0:
                raise HTTPError(403, 'request forbidden!')

        ### 写入日志
        ### pass

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_current_id(self):
        return self.get_secure_cookie("user_id")

    def get_current_nickname(self):
        return self.get_secure_cookie("nickname")

    def is_superuser(self):
        user_id = self.get_current_id()
        # with DBContext('readonly') as session:
        #     user_info = session.query(Users).filter(Users.user_id == user_id, Users.superuser == '0',
        #                                              Users.status == '0').first()
        # if user_info:
        #     return True
        return False

    @coroutine
    def async_execute_sync(self, handler, *args, **kwargs):
        future = Executor().submit(self.execute_sync_function, handler, *args, **kwargs)
        result = yield with_timeout(timedelta(seconds=5), future, quiet_exceptions=TimeoutError)
        return self.return_result(result)

    def execute_sync_function(self, handler, *args, **kwargs):
        result = handler(*args, **kwargs)
        return result

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.set_status(status_code)
            return self.render('404.html')

        elif status_code == 400:
            self.set_status(status_code)
            return self.finish('bad request')

        elif status_code == 403:
            self.set_status(status_code)
            return self.finish('Sorry, you have no permission. Please contact the administrator')

        elif status_code == 500:
            self.set_status(status_code)
            return self.finish('服务器内部错误')

        elif status_code == 401:
            self.set_status(status_code)
            return self.redirect("/login/")

        else:
            self.set_status(status_code)


class LivenessProbe(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("I'm OK")
