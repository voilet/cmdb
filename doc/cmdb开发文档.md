markdown语法
# Cmdb开发文档
## 文档作者
```
cmdb爱好者：祁成
```
## django访问流程
![sec](http://i2.51cto.com/images/blog/201806/01/dfa2851920c4c4e13f827814dc3a0237.jpg)

## 开发文档
```
引言	2
编写目的和范围	2
术语表	2
1部署说明	3
1.1 环境说明	3
1.2 Django的MTV模型	3
1.3 克隆部署代码	3
1.4 cmdb系统模块功能简介	6
```



# 部署说明
## cmdb系统模块功能简介
```
Accounts：用户权限管理、项目管理
	Api：用户所使用api模块
	Assets：资产管理系统模块
	Audit：日志审计功能模块
	Cmdb_auth: cmdb权限控制
	Config：项目发布模块
	DjangoUeditor：cmdb系统样式定义模块
	Static/md: 运维规范说明模块
	Finotify：可疑文件监控模块
	Malfunction：故障模块-对接监控系统
	Message：cmdb系统消息提示模块
	Monitor：业务监控之http与mysql监控模块
	Mysite：项目模块—settings.py为配置全局生效文件
	Pagination：分页模块
	Salt_ui: saltstack功能模块
	Scripts：内网ip使用率查看模块—salt收集资产模块
	Static：静态文件目录
	Swan：项目发布模块
	Templates: 前端页面使用模版文件
	Users：用户详情模块
	Utils：公用模版-根据项目查询项目授权的用户
```
列表
- MTV模型介绍
```
M:models 模型：主要用于数据库操作
T：template模版：主要用于前端渲染
V：View视图：主要用于后端逻辑实现
```
- 代码克隆
```
参考help.txt
```
- 系统管理
```
后续跟新
```
## 数据表说明
```
| AuthNode                          |
| AuthSudo                          |
| assets_conftemplate               |        
| assets_host                       |   #服务器信息表
| assets_host_business              |   #服务器与项目对应表
| assets_host_service               |	#服务器与服务对应表
| assets_hostrecord                 |	#cmdb用户操作主机记录
| assets_idc                        |	#idc机房信息表
| assets_iplist                     |   #ip列表
| assets_line                       |	#产品线数据表
| assets_project                    |	#服务与项目对应表
| assets_projectuser                |	项目所在的用户
| assets_service                    |   #服务信息表
| assets_zabbixrecord               |	#zabbix信息表
| audit_ssh_audit                   |   #日志审计-命令记录表
| auth_group                        |	#django默认的自动分组
| auth_group_permissions            |	#django默认的组权限
| auth_permission                   |	#django权限表
| cmdb_auth_auth_group              |	#django认证的组权限表
| cmdb_auth_auth_group_group_user   |   #用户关联表
| cmdb_auth_user_auth_cmdb          |	#权限表，为false就无权限
| django_admin_log                  |	#admin用户操作记录
| django_content_type               |   #django模型
| django_migrations                 |	#数据库变更操作记录
| django_session                    |	#session信息记录(新增权限会写入session中)
| gitCode                           |	#git代码记录
| incident                          |   #故障管理数据表
| monitor_monitorhttp               |	#监控http数据的表记录
| monitor_monitorhttplog            |	#监控http数据的日志记录
| monitor_monitormysql              |	#监控mysql数据的表记录
| project_swan                      |   #
| project_swan_node                 |	#
| project_swan_push_user            |	#项目推送用户
| push_system                       |	#代码推送相关
| salt_ui_operationlog              |	#
| salt_ui_salt_api_log              |	#salt的api日志记录
| salt_ui_salt_conf                 |	#salt配置文件记录
| salt_ui_salt_mode_name            |	#
| salt_ui_setuplog                  |	#salt的安装记录
| swan_apply                        |	#
| swan_swanlog                      |	#
| users_customuser                  |	#cmdb用户信息表
| users_customuser_groups           |	#cmdb用户组信息表
| users_customuser_user_permissions |	#用户表与权限对应关系表
| users_department_mode             |	#部门信息表
| users_departmentgroup             | 	#部门组信息
| users_server_auth                 |	#用户对应服务权限表
```




# 资产管理
## assets_host表结构设计
```
+-------------------+--------------+------+-----+---------+-------+
| Field             | Type         | Null | Key | Default | Extra |
+-------------------+--------------+------+-----+---------+-------+
| uuid              | char(32)     | NO   | PRI | NULL    |       |      #uuid
| node_name         | varchar(100) | YES  |     | NULL    |       |      #主机名
| eth1              | char(15)     | YES  |     | NULL    |       |      #eth1网卡ip
| eth2              | char(15)     | YES  |     | NULL    |       |	     #eth2网卡ip
| mac               | varchar(20)  | YES  |     | NULL    |       |      #MAC地址
| internal_ip       | char(15)     | YES  |     | NULL    |       |      #远程控制卡IP
| brand             | varchar(64)  | YES  |     | NULL    |       |      #服务器型号
| cpu               | varchar(64)  | YES  |     | NULL    |       |      #cpu型号描述
| hard_disk         | varchar(128) | YES  |     | NULL    |       |      #硬盘描述
| memory            | varchar(128) | YES  |     | NULL    |       |      #内存描述
| system            | varchar(32)  | YES  |     | NULL    |       |      #操作系统
| system_cpuarch    | varchar(32)  | YES  |     | NULL    |       |      #操作系统基于平台
| system_version    | varchar(8)   | YES  |     | NULL    |       |      #系统版本
| create_time       | datetime     | NO   |     | NULL    |       |      #记录创建的时间
| guarantee_date    | date         | YES  |     | NULL    |       |      #服务器过保到期时间
| cabinet           | varchar(32)  | YES  |     | NULL    |       |      #所属机柜
| server_cabinet_id | int(11)      | YES  |     | NULL    |       |      #机器所在机柜位置
| number            | varchar(32)  | YES  |     | NULL    |       |      #序列号
| editor            | longtext     | YES  |     | NULL    |       |   	 #机器备注
| status            | int(11)      | NO   |     | NULL    |       |      #服务器当前状态
| type              | int(11)      | NO   |     | NULL    |       |      #机器所属种类，实体机or虚拟机
| Services_Code     | varchar(16)  | YES  |     | NULL    |       |	     #快速服务编号
| env               | varchar(32)  | YES  |     | NULL    |       |	     #机器所属环境
| room_number       | varchar(32)  | YES  |     | NULL    |       |      #机器所在机房楼层房间号
| server_sn         | varchar(32)  | YES  |     | NULL    |       |      #服务器sn号
| switch_port       | varchar(12)  | YES  |     | NULL    |       |	     #对应交换机端口
| idle              | tinyint(1)   | NO   |     | NULL    |       |      #是否空闲—此字段无用
| idc_id            | char(32)     | YES  | MUL | NULL    |       |      #所对应机房id
| vm_id             | char(32)     | YES  | MUL | NULL    |       |      #所对应是否为虚拟机
```



## 自动化运维
## 业务监控
## 故障管理
```
完善中
```
### 对接监控系统
```
完善中
```
#### 运维故障管理知识库
```
+-------------------+--------------+------+-----+---------+-------+
| Field             | Type         | Null | Key | Default | Extra |
+-------------------+--------------+------+-----+---------+-------+
| uuid              | char(32)     | NO   | PRI | NULL    |       |
| title             | varchar(256) | NO   |     | NULL    |       |
| ip                | char(15)     | YES  |     | NULL    |       |
| url               | longtext     | YES  |     | NULL    |       |
| projectuser       | varchar(32)  | NO   |     | NULL    |       |
| closeuser         | varchar(32)  | YES  |     | NULL    |       |
| source            | int(11)      | NO   |     | NULL    |       |
| starttime         | datetime     | NO   |     | NULL    |       |
| scantime          | datetime     | YES  |     | NULL    |       |
| stoptime          | datetime     | YES  |     | NULL    |       |
| mailcomment       | longtext     | NO   |     | NULL    |       |
| status            | int(11)      | NO   |     | NULL    |       |
| classical         | tinyint(1)   | NO   |     | NULL    |       |
| grade             | int(11)      | YES  |     | NULL    |       |
| comment           | longtext     | NO   |     | NULL    |       |
| project_principal | varchar(32)  | YES  |     | NULL    |       |
| incident_user     | varchar(32)  | YES  |     | NULL    |       |
| createtime        | datetime     | NO   |     | NULL    |       |
+-------------------+--------------+------+-----+---------+-------+
```
## 日志审计
```
1当用户ssh登录服务器---
2通过全局路径会将操作命令存放到每个用户的目录隐藏文件audit.log中-
3并实时通过/usr/bin/fun_audit文件实时将记录audit.log内容取出。
4.并对fun_audit的/etc/audit.ini找到udpserver的ip和端口。
5.发送给udpserver端。
6.udpserver端接受到客户端传送过来的数据，进行数据的字典取相应的值赋值给变量。 
7.将相关数据组成一个大字典，通过发起一个post请求，将数据写入到通过api接口提交到mysql数据库中
8.通过模版渲染将数据取出展示到页面中。

```
# 权限系统
# 用户管理
## 用户信息表
```
+---------------+--------------+------+-----+---------+----------------+
|字段名   |数据类型 |允许非空| Key值 | 默认值| 自动递增      说明   |
+---------------+--------------+------+-----+---------+----------------+
| id            | int(11)      | NO   | PRI | NULL    | auto_increment |     #表id（自增）
| password      | varchar(128) | NO   |     | NULL    |                |     #用户加密密码
| last_login    | datetime     | NO   |     | NULL    |                |	 #最后登录时间
| is_superuser  | tinyint(1)   | NO   |     | NULL    |                |     #是否为超级管理员
| email         | varchar(254) | NO   | UNI | NULL    |                |	 #邮箱
| username      | varchar(30)  | NO   | UNI | NULL    |                |     #用户名
| first_name    | varchar(30)  | NO   |     | NULL    |                |     #姓
| last_name     | varchar(30)  | NO   |     | NULL    |                |     #名
| mobile        | varchar(30)  | NO   |     | NULL    |                |     #手机号
| session_key   | varchar(60)  | YES  |     | NULL    |                |     #session-key
| user_key      | longtext     | YES  |     | NULL    |                |     #user-key
| menu_status   | tinyint(1)   | NO   |     | NULL    |                |     #菜单展开收缩权限
| user_active   | tinyint(1)   | NO   |     | NULL    |                |     #用户状态
| uuid          | varchar(64)  | NO   | UNI | NULL    |                |     #uuid
| is_staff      | tinyint(1)   | NO   |     | NULL    |                |	 #是否在职
| is_active     | tinyint(1)   | NO   |     | NULL    |                |     #是否可登录
| date_joined   | datetime     | NO   |     | NULL    |                |     #加入时间
| department_id | int(11)      | YES  | MUL | NULL    |                |     #部门id
```



诚谢
> 感谢宋哥的默默付出，也感谢各位朋友一直以来对我们开源项目的支持。
