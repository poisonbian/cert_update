# cert_update
通过acme，更新https域名证书，并更新至百度BCH或者七牛云。

其中，七牛云无需其他操作，直接生效；百度BCH需要手动到百度云的管理后台点击域名证书的刷新按钮。

## 使用步骤：
1. 安装acme
https://github.com/acmesh-official/acme.sh
2. 安装python执行环境
3. 在python中安装百度BCE SDK
https://cloud.baidu.com/doc/Developer/index.html?sdk=python
4. 配置cert_conf.py
5. 运行

### 典型场景：更新qiniu的ssl证书
python ./cert_client.py -d qiniu.mydomain.com -q

### 典型场景：更新百度BCH的SSL证书
python ./cert_client.py -d mydomain.com -w

### 配置说明
-d / --domain：更新证书的域名，一级、二级等不同级别的域名均可
-w / --wildcard：是否更新一级域名对应的www域名
例如 -d mydomain.com 生成的证书，只支持mydomain.com的认证，而-d mydomain.com -w可以支持mydomain.com和www.mydomain.com这两个域名的认证
-q / --qiniu：域名是七牛上的域名（可以触发七牛证书的自动更新）；如果不使用-q则表示为百度云上的证书
-h / --help：帮助信息
-n / --not-upload：如果加上该参数，则生成的证书不上传至百度云/七牛云；不加参数，则生成的证书会自动上传至七牛云、百度云。其中七牛云会触发自动更新，替换使用新证书；百度云暂时没有接口进行触发，需要登录到百度云之后手动执行

### run_cert_update.sh
这个脚本可用于jenkins中的定时执行，默认满85天进行更新。

jenkins中可以设置2个任务进行关联，一个判断是否满足天数条件，即使用run_cert_update.sh，一个调用更新脚本，即cert_client.py。

exit 0 表示脚本执行成功（即天数达到配置天数），则触发后续更新任务。

exit 1 表示脚本执行失败，则不触发后续更新任务。


