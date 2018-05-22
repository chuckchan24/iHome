# coding=utf-8
"""次文件中定义和用户登录，注册相关的api"""
import re

from flask import request, jsonify, current_app, session
from ihome import redis_store, db
from ihome.models import User
from ihome.utils.response_code import RET
from . import api


@api.route('/session', methods=['POST'])
def login():
    """
    用户登录功能
    1.接收参数（手机号，密码）并进行校验
    2.根据手机号取查询User信息（如果查不到，说明用户不存在）
    3.校验登录密码是否正确
    4.记住用户登录的状态
    5.返回应答，登录成功
    :return:
    # """
    # 1.接收参数（手机号，密码）并进行校验
    req_dict = request.json
    print req_dict
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 2.根据手机号取查询User信息（如果查不到，说明用户不存在）
    try:
        user = User.query.filter(User.mobile == mobile).first()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    # 3.校验登录密码是否正确
    if not user.check_user_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='登录密码错误')

    # 4.记住用户登录的状态
    session['user_id'] = user.id
    session['username'] = user.name
    session['mobile'] = user.mobile

    # 5.返回应答，登录成功
    return jsonify(errno=RET.OK, errmsg='登录成功')


@api.route('/users', methods=['POST'])
def register():
    """
    用户注册功能
    1.接受参数（手机号，短信验证码，密码）并进行参数校验
    2.从redis中获取短信验证码（如果取不到，说明短信验证码过期）
    3.对比短信验证码，
    4.如果一致，创建User对象并保存注册用户的信息
    5.把注册用户的信息添加进数据库
    6.返回应答，注册成功
    :return:
    """
    # 1.接受参数（手机号，短信验证码，密码）并进行参数校验
    req_dict = request.json
    mobile = req_dict.get('mobile')
    sms_code = req_dict.get('sms_code')
    password = req_dict.get('password')

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整!')

    if not re.match(r'^1[35789]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确!')

    # 2.从redis中获取短信验证码（如果取不到，说明短信验证码过期）
    try:
        real_sms_code = redis_store.get('smscode: %s' % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取短信验证码失败')

    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码已过期!')

    # 3.对比短信验证码，
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码错误')

    # 判断手机号是否已经被注册
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg='手机号已被注册')

    # 4.如果一致，创建User对象并保存注册用户的信息
    user = User()
    user.mobile = mobile
    user.name = mobile
    # todo: 注册码加密
    user.password = password

    # 5.把注册用户的信息添加进数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存注册用户信息失败')

    # 6.记住用户登录的状态
    session['user_id'] = user.id
    session['username'] = user.name
    session['mobile'] = user.mobile

    # 7.返回应答，注册成功
    return jsonify(errno=RET.OK, errmsg='注册成功')
