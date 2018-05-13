# coding=utf-8

from flask import Blueprint
# 创建蓝图对象
api = Blueprint('app_1_0', __name__)
from . import index
