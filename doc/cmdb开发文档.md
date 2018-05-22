markdown语法
# Cmdb开发文档
## 文档作者
```
cmdb爱好者：祁成、宋绪双
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
| django_admin_log                  |	
| django_content_type               |   #django模型
| django_migrations                 |	#数据库变更操作记录
| django_session                    |	#session信息记录(新增权限会写入session中)
| gitCode                           |	#git代码记录
| incident                          |
| monitor_monitorhttp               |	#监控http数据的表记录
| monitor_monitorhttplog            |	#监控http数据的日志记录
| monitor_monitormysql              |	#监控mysql数据的表记录
| project_swan                      |
| project_swan_node                 |	#
| project_swan_push_user            |	#项目推送用户
| push_system                       |	#代码推送相关
| salt_ui_operationlog              |	#
| salt_ui_salt_api_log              |	#salt的api日志记录
| salt_ui_salt_conf                 |	#salt配置文件记录
| salt_ui_salt_mode_name            |
| salt_ui_setuplog                  |	#salt的安装记录
| swan_apply                        |
| swan_swanlog                      |	
| users_customuser                  |	#cmdb用户信息表
| users_customuser_groups           |	#cmdb用户组信息表
| users_customuser_user_permissions |	#用户表与权限对应关系表
| users_department_mode             |	#部门信息表
| users_departmentgroup             | 	#部门组信息
| users_server_auth                 |	#用户对应服务权限表
```


## 环境说明
## Django的MTV模型
## 克隆并配置部署代码
# 资产管理
# 自动化运维
# 业务监控
# 故障管理
# 日志审计
# 权限系统




