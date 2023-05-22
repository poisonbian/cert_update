# -*- coding: utf-8 -*- 

# 导入Python标准日志模块
import logging

# 从Baidu BCE Python SDK导入证书服务配置管理模块以及安全认证模块
# SDK下载地址：https://cloud.baidu.com/doc/Developer/index.html?sdk=python
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
import baidubce

# 设置CertClient的Host，Access Key ID和Secret Access Key
# 设置和查看：https://console.bce.baidu.com/iam/#/iam/accesslist
cert_host = "certificate.baidubce.com"
access_key_id = "baidu_access_key_id"
secret_access_key = "baidu_secret_access_key"

# 设置日志文件的句柄和日志级别
logger = logging.getLogger('baidubce.services.cert.certclient')
fh = logging.FileHandler("sample.log")
fh.setLevel(logging.DEBUG)

# 设置日志文件输出的顺序、结构和内容
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

# 创建BceClientConfiguration
#config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint = cert_host)
config = BceClientConfiguration(
        credentials = BceCredentials(access_key_id, secret_access_key),
        endpoint = cert_host,
        protocol = baidubce.protocol.HTTPS
)


