# coding=utf-8
"""专门为静态文件设置访问路径，为静态文件的访问创建一个蓝图"""

from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

html = Blueprint('html', __name__)


@html.route('/<re(".*"):file_name>', methods=['GET', 'POST'])
def get_html(file_name):
    """提供html静态文件"""
    # 根据用户访问路径中指定的html文件名，找到指定的静态文件并返回
    if not file_name:
        # 表示用户访问的是'/'
        file_name = 'index.html'

    # 判断如果不是网站logo
    if file_name != 'favicon.ico':
        # 拼接路径
        file_name = 'html/' + file_name

    # 生成csrf_token
    csrf_token = generate_csrf()
    # 将 csrf_token 设置到 cookie 中
    response = make_response(current_app.send_static_file(file_name))
    response.set_cookie('csrf_token', csrf_token)

    return response
