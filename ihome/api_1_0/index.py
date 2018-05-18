# coding=utf-8
from . import api


@api.route('/', methods=['GET', 'POST'])
def index():
    print('index')

    return 'index'
