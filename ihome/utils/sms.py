# coding=gbk
# coding=utf-8
# -*- coding: UTF-8 -*-
"""发送短信"""

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf0708635e4ce00163777c908510aa'

# 主帐号Token
accountToken = '9ad9c8550bf0441291cfc63bd2c5e18c'

# 应用Id
appId = '8aaf0708635e4ce00163777c90d610b0'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


class CCP(object):
    # cls._instance
    def __new__(cls, *args, **kwargs):
        # 判断cls是否拥有_instance属性，此属性用来保存这个类的唯一对象（单例模式）
        if not hasattr(cls, '_instance'):
            # 创建一个单例对象
            obj = super(CCP, cls).__new__(cls)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls._instance = obj

        # 如果有_instance属性，直接返回
        return cls._instance

    # def __init__(self):
    #     # 初始化REST SDK
    #     self.rest = REST(serverIP, serverPort, softVersion)
    #     self.rest.setAccount(accountSid, accountToken)
    #     self.rest.setAppId(appId)

    # 发送模板短信
    # @param to 手机号码
    # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
    # @param $tempId 模板Id
    def send_template_sms(self, to, datas, tempId):

        # sendTemplateSMS(手机号码,内容数据,模板Id)
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        print(result)

        if result.get('statusCode') == '000000':
            # 短信发送成功
            return 1
        else:
            # 短信发送失败
            return 0


if __name__ == '__main__':
    # sendTemplateSMS('18617166803', ['123456', 5], 1)
    CCP().send_template_sms('18617166803', ['123456', 5], 1)