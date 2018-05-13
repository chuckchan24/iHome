# coding=utf-8
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from cofig import config_dict


db = SQLAlchemy()


# 工厂方法：传入不同参数，返回不同的对象
def create_app(config_name):
    """根据不同开发阶段，创建不同类型config配置的app对象"""

    app = Flask(__name__)

    config_type = config_dict[config_name]

    app.config.from_object(config_type)

    # 创建sqlalchemy对象
    db.init_app(app)

    # 创建redis数据库链接对象
    redis_store = redis.StrictRedis(host=config_type.REDIS_HOST,
                                    port=config_type.REDIS_PORT)

    # 开启CSRF保护，这一步只做保护校验
    # 至于生成csrf_token cookie还有请求时携带的csrf_token需要再设置
    CSRFProtect(app)

    # session信息存储
    Session(app)

    return app
