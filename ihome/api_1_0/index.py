# coding=utf-8
from flask import current_app

from . import api
import logging


@api.route('/', methods=['GET', 'POST'])
def index():
    # # 测试日志功能
    # logging.fatal('Fatal Message')
    # logging.error('Error Message')
    # logging.warn('Warn Message')
    # logging.info('Info Message')
    # logging.debug('Debug Message')
    # # flask的current_app也有log功能，在终端显示更加详尽。
    # current_app.logger.fatal('Fatal Message')

    return 'index'
