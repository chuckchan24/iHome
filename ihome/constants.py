# coding=utf-8
"""项目常量信息(数据库缓存信息、验证码、房屋信息等)"""

# 图片验证码redis有效期，单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300

# 短信验证码redis有效期，单位：秒
SMS_CODE_REDIS_EXPIRES = 300

# 七牛空间域名
QINIU_DOMIN_PREFIX = 'http://p8wjiurts.bkt.clouddn.com/'

# 城区信息redis缓存时间，单位：秒
AREA_INFO_REDIS_EXPIRES = 7200

# 首页展示最多的房屋数
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋评论页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页数据的redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRES = 7200

# 房屋列表页面每次显示的条目数
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列秒页面redis缓存时间，单位：秒
HOUSE_LIST_REDIS_EXPIRES = 7200
