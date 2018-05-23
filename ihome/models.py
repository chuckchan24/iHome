# coding=utf-8
"""项目模型类"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ihome import constants
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间和更新事件"""

    # 模型创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 模型更新事件
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseModel, db.Model):
    """用户模型"""

    __tablename__ = 'ih_user_profile'

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号码
    real_name = db.Column(db.String(32))  # 真实姓名
    id_card = db.Column(db.String(20))  # 身份证号
    avatar_url = db.Column(db.String(128))  # 用户头像的保存路径

    houses = db.relationship('House', backref='user')  # 用户发布的房屋信息
    orders = db.relationship('Order', backref='user')  # 用户下的订单

    @property
    def password(self):
        raise AttributeError('不能读取密码内容')

    @password.setter
    def password(self, value):
        # 对注册用户的密码进行加密
        self.password_hash = generate_password_hash(value)

    def check_user_password(self, password):
        # 校验用户密码是否正确
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """将对象的信息转化为字典"""
        resp = {
            'user_id': self.id,
            'username': self.name,
            'mobile': self.mobile,
            'avatar_url': constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else '',
        }
        return resp

    def auth_to_dict(self):
        """讲用户的实名认证信息转化为字典"""
        resp = {
            'user_id': self.id,
            'real_name': self.real_name,
            'id_card': self.id
        }
        return resp


class Area(BaseModel, db.Model):
    """区域模型"""

    __tablename__ = 'ih_area_info'

    id = db.Column(db.Integer, primary_key=True)  # 区域编号
    name = db.Column(db.String(32), nullable=False)  # 区域名称

    houses = db.relationship('House', backref='area')  # 区域内的房屋

    def do_dict(self):
        """将对象转换成字典数据"""

        area_dict = {
            'aid': self.id,
            'aname': self.name
        }
        return area_dict


# 房屋设施表，建立房屋与设施的多对多关系
house_facility = db.Table(
    'ih_house_facility',
    db.Column('house_id', db.Integer, db.ForeignKey('ih_house_info.id'), primary_key=True),  # 房屋编号
    db.Column('facility_id', db.Integer, db.ForeignKey('ih_facility_info.id'), primary_key=True),  # 设施编号
)


class House(BaseModel, db.Model):
    """房屋模型"""

    __tablename__ = 'ih_house_info'

    id = db.Column(db.Integer, primary_key=True)  # 房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey('ih_user_profile.id'), nullable=False)  # 房屋主人的用户编号
    area_id = db.Column(db.Integer, db.ForeignKey('ih_area_info.id'), nullable=False)  # 房屋归属地的区域编号
    title = db.Column(db.String(64), nullable=False)  # 标题
    price = db.Column(db.Integer, default=0)  # 单价，单位：分
    address = db.Column(db.String(512), default='')  # 地址
    room_count = db.Column(db.Integer, default=1)  # 房间数目
    areaage = db.Column(db.Integer, default=0)  # 房屋面积
    unit = db.Column(db.String(32), default='')  # 房屋单元， 如几室几厅
    capacity = db.Column(db.Integer, default=1)  # 房屋容纳的人   cap数
    beds = db.Column(db.String(64), default='')  # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0)  # 房屋押金
    min_days = db.Column(db.Integer, default=1)  # 最少入住天数
    max_days = db.Column(db.Integer, default=1)  # 最多入住天数
    order_count = db.Column(db.Integer, default=0)  # 预订完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default='')  # 房屋主图片的路径

    facilities = db.relationship('Facility', secondary=house_facility)  # 房屋的设施
    images = db.relationship('HouseImage')  # 房屋的图片
    orders = db.relationship('Order', backref='house')  # 房屋的订单

    def do_dict(self):
        """将基本信息转换为字典数据"""

        house_dict = {
            "house_id": self.id,
            "title": self.title,
            "price": self.price,
            "area_name": self.area.name,
            "img_url": constants.QINIU_DOMIN_PREFIX + self.index_image_url if self.index_image_url else "",
            "room_count": self.room_count,
            "order_count": self.order_count,
            "address": self.address,
            "user_avatar": constants.QINIU_DOMIN_PREFIX + self.user.avatar_url if self.user.avatar_url else "",
            "ctime": self.create_time.strftime("%Y-%m-%d")
        }
        return house_dict

    def to_full_dict(self):
        """将详细信息转换为字典数据"""
        house_dict = {
            "hid": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name,
            "user_avatar": constants.QINIU_DOMIN_PREFIX + self.user.avatar_url if self.user.avatar_url else "",
            "title": self.title,
            "price": self.price,
            "address": self.address,
            "room_count": self.room_count,
            "acreage": self.acreage,
            "unit": self.unit,
            "capacity": self.capacity,
            "beds": self.beds,
            "deposit": self.deposit,
            "min_days": self.min_days,
            "max_days": self.max_days,
        }

        # 房屋图片
        img_urls = []
        for image in self.images:
            img_urls.append(constants.QINIU_DOMIN_PREFIX + image.url)
        house_dict['img_urls'] = img_urls

        # 房屋设施
        facilities = []
        for facility in self.facilities:
            facilities.append(facility.id)
        house_dict['facilities'] = facilities

        # 评论信息
        comments = []
        orders = Order.query.filter(Order.house_id == self.id, Order.status == 'COMPLETE', Order.comment != None) \
            .order_by(Order.update_time.desc()).limit(constants.HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS)

        for order in orders:
            comment = {
                'comment': order.comment,  # 评论的内容
                'user_name': order.user.name if order.user.name != order.user.mobile else '匿名用户',  # 发表评论的用户
                'ctime': order.update_time.strftime('%Y-%m-%d %H:%M:%S')  # 评价的时间
            }
            comments.append(comment)
        house_dict['comments'] = comments
        return house_dict


class Facility(BaseModel, db.Model):
    """设施信息模型"""

    __tablename__ = 'ih_facility_info'

    id = db.Column(db.Integer, primary_key=True)  # 设施编号
    name = db.Column(db.String(32), nullable=False)  # 设施名字


class HouseImage(BaseModel, db.Model):
    """房屋图片模型"""

    __tablename__ = 'ih_house_image'

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('ih_house_info.id'), nullable=False)  # 房屋编号
    url = db.Column(db.String(256), nullable=False)  # 图片的路径


class Order(BaseModel, db.Model):
    """订单模型"""

    __tablename__ = 'ih_order_info'

    id = db.Column(db.Integer, primary_key=True)  # 订单编号
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)  # 下订单的用户编号
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 预订的房间编号
    begin_date = db.Column(db.DateTime, nullable=False)  # 预订的起始时间
    end_date = db.Column(db.DateTime, nullable=False)  # 预订的结束时间
    days = db.Column(db.Integer, nullable=False)  # 预订的总天数
    house_price = db.Column(db.Integer, nullable=False)  # 房屋的单价
    amount = db.Column(db.Integer, nullable=False)  # 订单的总金额
    status = db.Column(  # 订单的状态
        db.Enum(
            "WAIT_ACCEPT",  # 待接单,
            "WAIT_PAYMENT",  # 待支付
            "PAID",  # 已支付
            "WAIT_COMMENT",  # 待评价
            "COMPLETE",  # 已完成
            "CANCELED",  # 已取消
            "REJECTED"  # 已拒单
        ),
        default="WAIT_ACCEPT", index=True)
    comment = db.Column(db.Text)  # 订单的评论信息或者拒单原因
