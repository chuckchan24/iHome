# coding=utf-8
"""项目应用初始化文件(应用程序实例、数据库实例、蓝图注册、日志等)"""
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from cofig import config_dict
from ihome.utils.commons import RegexConverter
import redis
import logging


db = SQLAlchemy()

redis_store = None


def set_logging(log_level):

    # 设置日志的记录等级
    logging.basicConfig(level=log_level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 工厂方法：传入不同参数，返回不同的对象
def create_app(config_name):
    """根据不同开发阶段，创建不同类型config配置的app对象"""

    app = Flask(__name__)

    config_type = config_dict[config_name]

    app.config.from_object(config_type)

    set_logging(config_type.LOG_LEVEL)

    # 创建sqlalchemy对象
    db.init_app(app)

    # 创建redis数据库链接对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_type.REDIS_HOST,
                                    port=config_type.REDIS_PORT)

    # 开启CSRF保护，这一步只做保护校验
    # 至于生成csrf_token cookie还有请求时携带的csrf_token需要再设置
    CSRFProtect(app)

    # session信息存储
    Session(app)

    # 向app注册自定义正则转换器
    app.url_map.converters['re'] = RegexConverter

    # 导入app_1_0，注册蓝图
    from ihome.api_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    # 注册html静态页面的蓝图
    import web_html
    app.register_blueprint(web_html.html)

    return app
