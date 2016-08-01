# 运维规范

标签（空格分隔）： 运维 规范

---

### 业务
* 业务描述
    * 媒资系统是风行电视-视频应用的数据支撑系统。媒资系统分为接口和管理后台两部分。其中媒资接口提供首页/媒体/视频/直播/轮播/点子节目单/专题等数据。管理后台实现管理和运营电视平台所有数据的功能。

* 主要流程
* 主要API
* 系统拓扑图

```flow
st=>start: 用户登陆
op=>operation: 登陆操作
cond=>condition: 登陆成功 Yes or No?
e=>end: 进入后台

st->op->cond
cond(yes)->e
cond(no)->op
```

```seq
Andrew->China: Says Hello 
Note right of China: China thinks\nabout it 
China-->Andrew: How are you? 
Andrew->>China: I am good thanks!
```

### 部署
* 各模块部署过程及注意事项，研发提供部署文档，运维根据文档转换成saltstack自动化配置文件
* 以oms为例

```python
include:
  - fun_tomcat
  - nginx

zookeeper:
  pkg:
    - installed
    - name: fun-zookeeper

oms_webapps:
  file.directory:
    - name: /data/www/webapps
    - user: tomcat
    - group: tomcat
    - dir_mode: 755
    - file_mode: 644
    - recurse:
        - user
        - group
        - mode

{% for i in ["dubbo_admin",  "task_manager"] %}
php_lib_{{ i }}:
  cmd.run:
    - name: cp -rf /usr/local/tomcat /data/{{ i }};chown -R tomcat:tomcat /usr/local/tomcat /data/{{ i }};
    - unless: test -d /data/{{ i }}

  file.managed:
    {% if i == "dubbo_admin" %}
    - source: salt://fun_tomcat/templates/server_8081.xml 
    {% elif i == "task_manager" %}
    - source: salt://fun_tomcat/templates/server_8083.xml
    {% endif %}
    - name: /data/{{ i }}/conf/server.xml
    - user: tomcat
    - group: tomcat
    - mode: 644
{% endfor %}

{% for i in ["dubbo_admin", "task_manager"] %}
conf_service{{ i}}:
  file.managed:
    - source: salt://oms/file/init.d/tomcat_{{ i }}
    - name: /etc/init.d/tomcat_{{ i }}
    - user: tomcat
    - group: tomcat
    - mode: 755
{% endfor %}

{% if grains['fqdn'] == "l-oms115115.shop.prod.ctc"%}
dubbo_admin_war:
  file.managed:
    - source: salt://oms/file/ROOT.war
    - name: /data/dubbo_admin/webapps/ROOT.war
    - user: tomcat
    - group: tomcat
    - mode: 644
{% endif %}


zoo_cfg:
  file.managed:
    - source: salt://oms/file/zoo.cfg
    - name: /usr/local/zookeeper/conf/zoo.cfg
    - user: zookeeper
    - group: zookeeper
    - mode: 644


oms_path:
  file.managed:
    - source: salt://oms/file/oms.sh
    - name: /etc/profile.d/oms.sh
    - user: root
    - group: root
    - mode: 755


/etc/hosts:
  file.append:
    - text:
      - 192.168.115.115 server.1
      - 192.168.115.116 server.2
      - 192.168.115.117 server.3

zookeeper_log:
  file.directory:
    - name: /data/logs/zookeeper
    - user: zookeeper
    - group: zookeeper
    - dir_mode: 755
    - file_mode: 644
    - recurse:
        - user
        - group
        - mode

zookeeper_data:
  file.directory:
    - name: /data/zookeeper
    - user: zookeeper
    - group: zookeeper
    - dir_mode: 755
    - file_mode: 644
    - recurse:
        - user
        - group
        - mode

webapps_data:
  file.directory:
    - name: /data/www/webapps
    - user: tomcat
    - group: tomcat
    - dir_mode: 755
    - file_mode: 644
    - makedirs: True
    - recurse:
        - user
        - group
        - mode

/data/zookeeper/myid:
  file.managed:
    - source: salt://oms/file/myid
    - user: zookeeper
    - group: zookeeper
    - mode: 644
    - template: jinja

oms_code_config:
  git.latest:
    - name: http://192.168.111.101:3000/ops/tv-oms-config.git
    - rev: master
    - user: tomcat
    - target: /data/www/webapps/config
    - unless: test -d /data/www/webapps/config

oms_code:
  git.latest:
    - name: http://192.168.111.101:3000/ops/oms_code.git
    - rev: master
    - user: tomcat
    - target: /usr/local/tomcat/webapps
    - unless: test -d /usr/local/tomcat/webapps

  cmd.run:
    - name: ln -s /data/www/webapps/config /usr/local/tomcat/webapps/config
    - unless: test -d /usr/local/tomcat/webapps/config


```

### 维护
* 由研发提供

### 监控
* 除系统基础服务，其它监控项需研发提供

### 排障
* 项目故障一般排查那些地方，由研发提供

### 调优
* 如项目由优化参数，由研发提供

### 安全
* 如项目开放在公网，有后台或特殊api接口，需研发提供做acl限制

### 备份
* 日志或其它需备份的，需研发提供

### 代码发布
* php代码只取master分支
* java 代码默认取build分析，多个平台多个分支发布需提前商定发布分支，如电视fun-build && aws-build
* 所有代码必须使用code.funshion.com代码仓库，商业产品部使用gitlib.funshion.com, 所有需要自动化发布的必须给ops用户添加权限
* 发布邮件格式如下

```python
应用市场后台需要更新：
项目名：tv_banana_admin
版本号：9b370ff874
分支：aws-build
war包地址：http://code.funshion.com/Brazil/tv_banana_admin/src/aws-build
war包名称：ROOT.war
```









