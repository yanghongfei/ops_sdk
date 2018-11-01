#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2017/4/11 下午1:54
role   : 常量管理
'''

from enum import IntEnum as Enum

class ConstError(TypeError):
    pass

class IntEnum(Enum):
    @staticmethod
    def find_enum(cls, value):
        for k, v in cls._value2member_map_.items():
            if k == value:
                return v
        return None


class ErrorCode(IntEnum):
    """ 错误码枚举 """

    not_found = 404
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_allowed = 405
    not_acceptable = 406
    conflict = 409
    gone = 410
    precondition_failed = 412
    request_entity_too_large = 413
    unsupport_media_type = 415
    internal_server_error = 500
    service_unavailable = 503
    service_not_implemented = 501
    handler_uncatched_exception = 504
    config_import_error = 1001
    config_item_notfound_error = 1002


class _const(object):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError("Can't rebind const (%s)" % name)
        if not name.isupper():
            raise ConstError("Const must be upper.")
        self.__dict__[name] = value


const = _const()

const.DB_CONFIG_ITEM = 'databases'
const.DBHOST_KEY = 'host'
const.DBPWD_KEY = 'pwd'
const.DBUSER_KEY = 'user'
const.DBNAME_KEY = 'name'
const.DBPORT_KEY = 'port'
const.SF_DB_KEY = 'vmobel'
const.DEFAULT_DB_KEY = 'default'
const.READONLY_DB_KEY = 'readonly'

const.REDIS_CONFIG_ITEM = 'redises'
const.RD_HOST_KEY = 'host'
const.RD_PORT_KEY = 'port'
const.RD_DB_KEY = 'db'
const.RD_AUTH_KEY = 'auth'
const.RD_CHARSET_KEY = 'charset'
const.RD_DECODE_RESPONSES = 'decode_responses'
const.RD_PASSWORD_KEY = 'password'
const.DEFAULT_RD_KEY = 'default'

const.MQ_CONFIG_ITEM = 'mqs'
const.MQ_ADDR = 'MQ_ADDR'
const.MQ_PORT = 'MQ_PORT'
const.MQ_VHOST = 'MQ_VHOST'
const.MQ_USER = 'MQ_USER'
const.MQ_PWD = 'MQ_PWD'
const.DEFAULT_MQ_KEY = 'default'

const.APP_NAME = 'app_name'
const.LOG_PATH = 'log_path'
const.LOG_BACKUP_COUNT = 'log_backup_count'
const.LOG_MAX_FILE_SIZE = 'log_max_filesize'

const.REQUEST_START_SIGNAL = 'request_start'
const.REQUEST_FINISHED_SIGNAL = 'request_finished'

const.NW_SALT = 'nw'
const.ALY_SALT = 'aly'
const.TX_SALT = 'tx'
const.SG_SALT = 'sg'
const.DEFAULT_SALT = 'default'
const.SALT_API = 'salt_api'
const.SALT_USER = 'salt_username'
const.SALT_PW = 'salt_password'
const.SALT_OUT = 'salt_timeout'

const.NW_INCEPTION = 'nw'
const.ALY_INCEPTION = 'aly'
const.TX_INCEPTION = 'tx'
const.DEFAULT_INCEPTION = 'default'

const.REGION = "cn-hangzhou"
const.PRODUCT_NAME = "Dysmsapi"
const.DOMAIN = "dysmsapi.aliyuncs.com"