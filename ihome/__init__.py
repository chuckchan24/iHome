# coding=utf-8
"""项目应用初始化文件(应用程序实例、数据库实例、蓝图注册、日志等)"""

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from cofig import config_dict
from ihome.utils.commons import RegexConverter

db = SQLAlchemy()

redis_store = None


# 工厂方法：传入不同参数，返回不同的对象
def create_app(config_name):
    """根据不同开发阶段，创建不同类型config配置的app对象"""

    app = Flask(__name__)

    config_type = config_dict[config_name]

    app.config.from_object(config_type)

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
