asdfasdf#说明:
import salt.config
opts = salt.config.client_config('/etc/salt/master')
import salt.runner
rclient = salt.runner.RunnerClient(opts)
rclient.cmd('jobs.list_jobs', '')

资产调用api
获取项目列表
http://192.168.1.192:8000/api/project/

获取项目信息，主机列表，相关人员，联系方式
http://192.168.1.192:8000/api/project/7/


graceful-down:
  cmd.run:
    - name: service apache graceful
    - prereq:
      - file: site-code

site-code:
  file.recurse:
    - name: /opt/site_code
    - source: salt://site/code

这个例子的处理流程是: 首先通过test=True检查 salt://site/code是否有更新, 如果有更新, 则执行graceful-down的cmd指令关闭apache, 待apache关闭完毕后(必须要保证成功)然后进行site-code的file更新操作; 如果没有更新, 则不执行grace-down.
为什么会有prereq,  个人觉得因为之前提供的reqire, watch并不能解决的这类场景需求. 只是觉得这类动作放到配置管理中总感觉到不是个味道, 但是又觉得通过prereq让这类需求处理起来变得更简单
同时也看到新增了”use”, 也很实用  http://docs.saltstack.com/ref/states/requisites.html#use


redis初始化执行
db.conf.insert({"prod_name":"jm-nginx", "init_sls":"", "templates": ""})
db.conf.insert({"prod_name":"jm-php", "init_sls":"", "templates": ""})
db.conf.insert({"prod_name":"jm-user", "init_sls":"", "templates": ""})
db.conf.insert({"prod_name":"jm-lvs", "init_sls":"", "templates": ""})
db.conf.insert({"prod_name":"jm-haproxy", "init_sls":"", "templates": ""})



alert table assets_host change column Cabinets cabinet varchar;

##from config.ini
[salt_api]
url=http://192.168.49.14/
[salt_user]
user=sa
password=centos



l-pxe1.ops.prod.cn1:8888/config/init/openstack-post-install.sh


sed -i "s#l-saltstack1.ops.prod.localdomain#10.1.2.7#g" /etc/salt/minion
sed -i "s#localhost.localdomain#$(ifconfig |grep "inet addr:"|awk -F ":" '{print $2}'|grep 10.0|awk '{print $1}')#g" /etc/salt/minion
sed -i "s#l-pxe1.ops.prod.localdomain.jumei.com:8888#l-pxe1.ops.prod.cn1.jumei.com:8888#g" /etc/yum.repos.d/jm-epel.repo


curl --data "ip_addr=10.0.197.62&name=10.0.197.62&sysop=xushuangs&project=jwms&services=tomcat" http://ops.int.jumei.com/plugin/host/add/?api_key=24e718014ff2a464c1015f64c6b65dbb

curl --data "ip_addr=127.0.0.1" http://ops.int.jumei.com/plugin/host/delete/?api_key=24e718014ff2a464c1015f64c6b65dbb



from uuidfield import UUIDField

class MyModel(models.Model):
    uuid = UUIDField(auto=True)



# 修改用户session
from django.contrib.sessions.backends.db import SessionStore
s = SessionStore(session_key='2b1189a188b44ad18c35e113ac6ceead')
s['last_login']



python manage.py makemigrations
python manage.py  migrate





./configure  --prefix=/usr/local/php5.3.26 --with-openssl --enable-pcntl --enable-shmop --enable-simplexml --with-pcre-regex --with-zlib --enable-xml --enable-bcmath --with-zlib --with-curl --enable-exif --enable-ftp --with-gd --with-gettext --with-gmp --with-mhash --with-ldap --with-mcrypt --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-mysql-sock --enable-sockets --enable-zip --enable-fpm --with-pdo-mysql=mysqlnd --enable-mbstring --with-jpeg-dir=/usr --with-png-dir=/usr --with-gmp=/usr --with-iconv-dir=/usr/local/www/libiconv --with-freetype-dir --with-config-file-path=/usr/local/php5.3.26


./configure --prefix=/usr/local/php5.3.26 --with-openssl --enable-mbstring --with-zlib --enable-xml --with-gd=/usr/local/webserver/gd2/ --with-jpeg-dir  \
--enable-bcmath --with-mcrypt --with-iconv --enable-pcntl --enable-shmop --enable-simplexml --enable-ftp







ALTER TABLE incident MODIFY source INT(11) NOT NULL;
ALTER TABLE incident MODIFY grade INT(11) NOT NULL;
ALTER TABLE incident ADD mail_count INT(11) DEFAULT 0 NULL;
ALTER TABLE incident ADD project_principal VARCHAR(32) NULL;
