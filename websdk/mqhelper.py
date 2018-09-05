#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2017/3/3 下午9:31
role   : Version Update
'''
import traceback
import pika
from libs.consts import const
from settings import settings
from libs.web_logs import ins_log
from libs.errors.business import ConfigError


class MessageQueueBase(object):
    def __init__(self, exchange, exchange_type, routing_key='', queue_name='', no_ack=False, mq_key=''):
        mq_config = settings[const.MQ_CONFIG_ITEM][const.DEFAULT_MQ_KEY]
        if const.MQ_ADDR not in mq_config:
            raise ConfigError(const.MQ_ADDR)
        if const.MQ_PORT not in mq_config:
            raise ConfigError(const.MQ_PORT)
        if const.MQ_VHOST not in mq_config:
            raise ConfigError(const.MQ_VHOST)
        if const.MQ_USER not in mq_config:
            raise ConfigError(const.MQ_USER)
        if const.MQ_PWD not in mq_config:
            raise ConfigError(const.MQ_PWD)
        self.addr = mq_config[const.MQ_ADDR]
        self.port = mq_config[const.MQ_PORT]
        self.vhost = mq_config[const.MQ_VHOST]
        self.user = mq_config[const.MQ_USER]
        self.pwd = mq_config[const.MQ_PWD]
        self.__exchange = exchange
        self.__exchange_type = exchange_type
        self.__routing_key = routing_key
        self.__queue_name = queue_name
        self.__no_ack = no_ack

    def start_consuming(self):
        channel = self.create_channel()

        channel.exchange_declare(exchange=self.__exchange, exchange_type=self.__exchange_type)
        if self.__queue_name:
            result = channel.queue_declare(queue=self.__queue_name, durable=True)
        else:
            result = channel.queue_declare(exclusive=True)
        channel.queue_bind(exchange=self.__exchange, queue=result.method.queue, routing_key=self.__routing_key)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.call_back, queue=result.method.queue, no_ack=self.__no_ack)
        ins_log.read_log('info', '[*]Queue %s started.' % (result.method.queue))

        channel.start_consuming()

    def __enter__(self):
        self.__channel = self.create_channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()

    def create_channel(self):
        credentials = pika.PlainCredentials(self.user, self.pwd)
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.addr, self.port, self.vhost, credentials=credentials))
        channel = self.__connection.channel()
        return channel

    def call_back(self, ch, method, properties, body):
        try:
            ins_log.read_log('info', 'get message')
            self.on_message(body)

            if not self.__no_ack:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except:
            ins_log.read_log('error', traceback.format_exc())
            if not self.__no_ack:
                ch.basic_nack(delivery_tag=method.delivery_tag)

    def on_message(self, body):
        pass

    def publish_message(self, body, durable=True):
        self.__channel.exchange_declare(exchange=self.__exchange, exchange_type=self.__exchange_type)
        if self.__queue_name:
            result = self.__channel.queue_declare(queue=self.__queue_name)
        else:
            result = self.__channel.queue_declare(exclusive=True)

        self.__channel.queue_bind(exchange=self.__exchange, queue=result.method.queue)

        if durable:
            properties = pika.BasicProperties(delivery_mode=2)
            self.__channel.basic_publish(exchange=self.__exchange, routing_key=self.__routing_key, body=body,
                                         properties=properties)
        else:
            self.__channel.basic_publish(exchange=self.__exchange, routing_key=self.__routing_key, body=body)
        ins_log.read_log('info', 'Publish message %s sucessfuled.' % body)
