
1. 仅限admin组用户的权限：
    修改项目 http://127.0.0.1:8000/assets/server/type/edit/9/


2. 仅限jumeiconfig组用户权限：
    审核推送配置文件申请 http://127.0.0.1:8000/auto/approve/

配置推送流程描述:
一般用户，首先要分配所属项目，并且该用户属于"jumeiops"组

我们的权限分配：
我们现有［jumeiops,admin,］



#说明:
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

删除用户
user.absent
xushuangs:
  user.absent



jobs操作
running Returns the data of all running jobs that are found in the proc directory.
find_job Returns specific data about a certain job based on job id.
signal_job Allows for a given jid to be sent a signal.
term_job Sends a termination signal (SIGTERM, 15) to the process controlling the specified job.
kill_job Sends a kill signal (SIGKILL, 9) to the process controlling the specified job.


schemamigration southtut --initial
migrate assets 0004
有model部分修改
python manage.py schemamigration assets --auto


