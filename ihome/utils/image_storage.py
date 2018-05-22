# coding:utf-8
"""云存储设施文件(七牛云)"""

import qiniu


access_key = "uzc59bVURbUbazey9vrexXKocNKBUN8NuLijk57N"
secret_key = "-9lenw28jU2REojvGkcsEPWk5Nm9V2HIVqb5Nkts"

# 存储空间名称
bucket_name = 'ihome-sz08'


def storage_image(data):
    """上传文件到七牛云"""

    q = qiniu.Auth(access_key, secret_key)

    token = q.upload_token(bucket_name)

    ret, info = qiniu.put_data(token, None, data)

    if info.status_code == 200:
        # 上传成功
        key = ret.get('key')
        return key
    else:
        # 上传失败
        raise Exception('上传文件到七牛云失败')


if __name__ == '__main__':
    filename = raw_input('请输入上传文件名称：')

    with open(filename, 'rb') as f:
        storage_image(f.read())