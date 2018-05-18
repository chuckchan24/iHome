# coding=utf-8
from . import api

print('index.py')
@api.route('/', methods=['GET', 'POST'])
def index():
    print('index')

    return 'index'
