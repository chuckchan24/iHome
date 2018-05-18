# coding:utf-8
"""次文件中api用于提供给图片验证码和短信验证码"""
from ihome.utils.response_code import RET
from . import api
from ihome.utils.captcha.captcha import captcha
from flask import make_response, request, jsonify, current_app
from ihome import redis_store, constants


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
