# coding=utf-8
"""通用设施文件(正则url、登录验证装饰器)"""
from flask import session, jsonify, g
from werkzeug.routing import BaseConverter

from ihome.utils.response_code import RET


class RegexConverter(BaseConverter):
    """自定义正则转换器"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


# 自定义登录验证装饰器
def login_required(view_func):
    def wrapper(*args, **kwargs):
        """闭包函数"""

        # 进行登录验证
        user_id = session.get('user_id')

        if user_id:
            # 用户已登录，调用视图函数

            # 使用g变量零食保存登录用户的id
            # g变量中的内容可以在每次请求开始到请求结束的范围使用
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            # 用户未登录
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')

    return wrapper
