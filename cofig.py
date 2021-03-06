# coding=utf-8
"""项目配置文件"""

import redis
import logging


class Config(object):
    """配置项"""

    # 设置csrf的secret_key
    SECRET_KEY = 'lRca3y6BjCxE9dmlwB7/LIPlsu5QAY2ESBWQ+jTatfbc72UUPxXDnrVQ+bUQ6s3P'

    # mysql数据库相关配置
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/db_ihome'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # session存储配置
    # 设置session存储的数据库，这里使用的是redis
    SESSION_TYPE = 'redis'
    # 设置session数据库redis的地址跟端口
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session签名
    SESSION_USE_SIGNER = True
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2


class DevelopmentConfig(Config):
    """开发环境中的配置类"""

    DEBUG = True

    # 开发阶段日志等级
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产环境中的配置类"""

    # 生产阶段日志等级
    LOG_LEVEL = logging.WARNING


class TestingConfig(Config):
    """测试环境中的配置类"""

    TESTING = True


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
