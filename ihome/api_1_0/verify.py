# coding:utf-8
"""次文件中api用于提供给图片验证码和短信验证码"""
from ihome.utils.response_code import RET
from . import api
from ihome.utils.captcha.captcha import captcha
from flask import make_response, request, jsonify, current_app
from ihome import redis_store, constants
from ihome.utils.sms import CCP
import re
import random


@api.route('/sms_code', methods=['POST'])
def send_sms_code():
    """
    发送短信验证码
    1.接受参数（手机号，图片验证码，图片验证码标识uuid）并进行参数校验
    2.从redis中获取图片验证码（如果取不到，说明图片验证码过期）
    3.对比图片验证码是否否一致
    4.一致则使用云通讯发送短信验证码
    5.返回应答，发送短信成功
    :return:
    """
    # 1.接受参数（手机号，图片验证码，图片验证码标识uuid）并进行参数校验
    # req_data = request.data
    # req_dict = json.loads(req_data)
    # req_dict = request.get_json()
    req_dict = request.json
    mobile = req_dict.get('mobile')
    image_code = req_dict.get('image_code')
    image_code_id = req_dict.get('image_code_id')

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r'^1[35789]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 2.从redis中获取图片验证码(如果取不到，说明图片验证码过期)
    try:
        real_image_code = redis_store.get('imagecode: %s' % image_code_id)
    except Exception as e:
        current_app.logger(e)
        return jsonify(errno=RET.DBERR, errmsg='获取图片验证码失败')

    if not real_image_code:
        # 图片验证码过期
        return jsonify(errno=RET.NODATA, errmsg='图片验证码过期')

    # 3.对比图片验证码是否否一致
    if real_image_code != image_code:
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')

    # 4.一致则使用云通讯发送短信验证码
    # 随机生成短信验证码：6位数字
    sms_code = '%06s' % random.randint(0, 999999)

    try:
        res = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信失败')

    if res != 1:
        # 发送短信验证码失败
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信验证码失败')

    # 在redis中保存短信验证码内容
    try:
        redis_store.set('smscode: %s' % mobile, sms_code, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存短信验证码失败')

    # 5.返回应答，发送短信成功
    return jsonify(errno=RET.OK, errmsg='发送短信验证码成功')


@api.route('/image_code')
def get_image_code():
    """
    产生图片的验证码
    1. 接受参数（图片验证码表示）并进行校验
    2. 生成图片验证码
    3. 在redis中保存图片的验证码
    4. 返回验证码图片
    :return:
    """

    # 1.接受参数（图片验证码表示）并进行校验
    image_code_id = request.args.get('cur_id')

    if not image_code_id:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 2.生成图片验证码
    # 文件名称， 验证码文本， 验证码图片内容
    name, text, content = captcha.generate_captcha()

    response = make_response(content)
    # 指定返回内容的类型
    response.headers['Content-Type'] = 'image/jpg'

    # 3.在redis中保存图片的验证码
    try:
        # redis_store.set('key', 'value', 'expiry')
        redis_store.set('imagecode: %s' % image_code_id,
                    text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片验证码失败')
    # 4.返回验证码图片
    return response


@api.route('/sms_code')
def get_sms_code():
    """
    产生手机短信验证码
    :return:
    """
    pass
