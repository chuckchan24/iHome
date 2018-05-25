# coding=utf-8
"""次文件定义和房屋相关的api接口"""

from flask import current_app, jsonify, request, g

from ihome import db, constants
from ihome.models import Area, House, Facility, HouseImage
from ihome.utils.commons import login_required
from ihome.utils.image_storage import storage_image
from ihome.utils.response_code import RET
from . import api


@api.route('/house/image', methods=['POST'])
@login_required
def save_house_image():
    """
    保存上传的房屋图片
    1.接收房屋id和房屋文件对象
    2.根据房屋id获取房屋的信息（如果获取不到，说明房屋不存在）
    3.讲房屋图片上传到七牛云
    4.创建HouseImage对象并保存房屋图片记录
    5.放回应答
    :return:
    """
    # 1.接收房屋id和房屋文件对象
    house_id = request.form.get('house_id')
    image_file = request.files.get('house_image')

    if not all([house_id, image_file]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    # 2.根据房屋id获取房屋的信息（如果获取不到，说明房屋不存在）
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取房屋信息失败')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋不存在')

    # 3.讲房屋图片上传到七牛云
    try:
        key = storage_image(image_file.read())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='上传房屋图片失败')

    # 4.创建HouseImage对象并保存房屋图片记录
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = key

    if not house.index_image_url:
        house.index_image_url = key

    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存房屋图片记录失败')

    # 5.放回应答
    img_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='上传房屋图片记录成功', data={'img_url': img_url})


@api.route('/houses', methods=['POST'])
@login_required
def save_house_info():
    """
    保存发布房屋的信息
    1.接收参数并进行参数校验
    2.创建House对象并保存房屋的基本信息
    3.讲房屋的信息添加到数据库
    4.返回应答
    :return:
    """
    # 1.接收参数并进行参数校验
    req_dict = request.json

    title = req_dict.get('title')
    price = req_dict.get('price')
    address = req_dict.get('address')
    area_id = req_dict.get('area_id')
    room_count = req_dict.get('room_count')
    acreage = req_dict.get('acreage')
    unit = req_dict.get('unit')
    capacity = req_dict.get('capacity')
    beds = req_dict.get('beds')
    deposit = req_dict.get('deposit')
    min_days = req_dict.get('min_days')
    max_days = req_dict.get('max_days')

    if not all([title, price, address, area_id, room_count, acreage, unit, capacity,
                beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    try:
        # 数据库中房屋的单价和押金是以分为单位保存的
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2.创建House对象并保存房屋的基本信息
    house = House()

    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 获取房屋的设施信息
    facility = req_dict.get('facility')

    if facility:
        # 获取房屋设施的信息
        try:
            facilities = Facility.query.filter(Facility.id.in_(facility)).all()
            house.facilities = facilities
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='获取房屋信息失败')

    # 3.讲房屋的信息添加到数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存房屋信息失败')
    # 4.返回应答
    return jsonify(errno=RET.OK, errmsg='发布房屋信息成功', data={'house_id': house.id})


@api.route('/areas')
def get_areas():
    """
    获取所有城区的信息：
    1.获取所有城区信息
    2.组织数据，返回应答
    :return:
    """
    # 1.获取所有城区信息
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取城区信息失败')

    # 2.组织数据，返回应答
    areas_dict_li = list()
    for area in areas:
        areas_dict_li.append(area.to_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=areas_dict_li)

