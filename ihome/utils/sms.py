# coding=gbk
# coding=utf-8
# -*- coding: UTF-8 -*-
"""���Ͷ���"""

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf0708635e4ce00163777c908510aa'

# ���ʺ�Token
accountToken = '9ad9c8550bf0441291cfc63bd2c5e18c'

# Ӧ��Id
appId = '8aaf0708635e4ce00163777c90d610b0'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


class CCP(object):
    # cls._instance
    def __new__(cls, *args, **kwargs):
        # �ж�cls�Ƿ�ӵ��_instance���ԣ���������������������Ψһ���󣨵���ģʽ��
        if not hasattr(cls, '_instance'):
            # ����һ����������
            obj = super(CCP, cls).__new__(cls)
            # ��ʼ��REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls._instance = obj

        # �����_instance���ԣ�ֱ�ӷ���
        return cls._instance

    # def __init__(self):
    #     # ��ʼ��REST SDK
    #     self.rest = REST(serverIP, serverPort, softVersion)
    #     self.rest.setAccount(accountSid, accountToken)
    #     self.rest.setAppId(appId)

    # ����ģ�����
    # @param to �ֻ�����
    # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
    # @param $tempId ģ��Id
    def send_template_sms(self, to, datas, tempId):

        # sendTemplateSMS(�ֻ�����,��������,ģ��Id)
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        print(result)

        if result.get('statusCode') == '000000':
            # ���ŷ��ͳɹ�
            return 1
        else:
            # ���ŷ���ʧ��
            return 0


if __name__ == '__main__':
    # sendTemplateSMS('18617166803', ['123456', 5], 1)
    CCP().send_template_sms('18617166803', ['123456', 5], 1)