# 导入CertClient配置文件
import cert_conf
# 导入证书服务相关模块
from baidubce.services.cert.cert_client import CertClient
# Import CertCreateRequest
from baidubce.services.cert.cert_model import CertCreateRequest
# 其他
import time, sys, os, getopt


command_create = "/home/work/.acme.sh/acme.sh --force --issue -d %s --dns dns_dp --dnssleep 60"
command_create2 = "/home/work/.acme.sh/acme.sh --force --issue -d %s -d www.%s --dns dns_dp --dnssleep 60"
command_create3 = "/home/work/.acme.sh/acme.sh --force --issue -d %s -d *.%s --dns dns_dp --dnssleep 60"
command_rm = "mkdir -p %s"
command_install = "/home/work/.acme.sh/acme.sh --install-cert -d %s --key-file %s/key.pem --fullchain-file %s/cert.pem"
command_qiniu = "/home/work/.acme.sh/acme.sh --deploy -d %s --deploy-hook qiniu"

def execute_cmd(cmd):
    print("execute: %s" % cmd)
    os.system(cmd)

# 生成证书文件
def generate_cert(domain_name, is_wildcard):
    if is_wildcard:
        command = command_create3 % (domain_name, domain_name)
    elif domain_name.count(".") == 1:
        command = command_create2 % (domain_name, domain_name)
    else:
        command = command_create % (domain_name)
    execute_cmd(command)

    command = command_rm % (domain_name)
    execute_cmd(command)
    
    command = command_install % (domain_name, domain_name, domain_name)
    execute_cmd(command)

def upload_qiniu(domain_name):
    command = command_qiniu % (domain_name)
    execute_cmd(command)

# 上传证书文件到百度云
def upload_cert(domain_name):
    # 新建CertClient
    cert_client = CertClient(cert_conf.config)

    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
    cert_type = 1
    cert_content = read_cert(domain_name, "cert")
    private_content = read_cert(domain_name, "key")

    cert_name = domain_name + "-" + current_time
    if cert_name[0].isdigit():
        cert_name = "cert-" + cert_name
    cert_create_request = CertCreateRequest(cert_name, cert_content, private_content, None, cert_type)

    # Create a certificate
    response = cert_client.create_cert(cert_create_request)
    print(response)


# 读取已经生成好的pem文件
def read_cert(cert_name, cert_type):
    cert_path = "%s/%s.pem" % (cert_name, cert_type)
    with open(cert_path, 'r', encoding='utf-8') as cert_file:
        cert_content =  cert_file.read()
    return cert_content

def show_help():
    print("./cert_client.py")
    print("-h   show help info")
    print("-d [domain]")
    print("--domain [domain]  set domain name")
    print("-q")
    print("--qiniu          update qiniu cert")
    print("default: baidu bch cert")
    print("-w")
    print("--wildcard       generate wildcard domain cert, eg: xxx.com & *.xxx.com")
    print("default: not wildcard")
    print("-n")
    print("--not-upload     not to upload to bch or qiniu")
    print("default: generate, then upload")
    sys.exit(1)

domain_name = ""
is_qiniu = False
is_wildcard = False
need_upload = True

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:qwn", ["domain=", "qiniu", "wildcard", "not-upload"])
except getopt.GetoptError:
    show_help()
for opt, arg in opts:
    if opt == '-h':
        show_help()
    elif opt in ("-d", "--domain"):
        domain_name = arg
    elif opt in ("-q", "--qiniu"):
        is_qiniu = True
    elif opt in ("-w", "--wildcard"):
        is_wildcard = True
    elif opt in ("-n", "--not-upload"):
        need_upload = False

generate_cert(domain_name, is_wildcard)
if need_upload:
    if is_qiniu:
        upload_qiniu(domain_name)
    else:
        upload_cert(domain_name)




