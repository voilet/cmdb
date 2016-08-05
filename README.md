# Django CMDB and salt UI
* [Contributors](#contributors)
* [Install guideline](#install-guideline)
* [Project screenshots](#project-screenshots)

## Contributors
* 王墉 (halcyon) jumpserver开发者之一
* 张磊 (python开发大神，指点用了很多django优秀扩展)

## Install guideline:
* 需要python2.7环境
* 查看doc/help.txt
* 初始化数据
* doc/cmdb.sql

### Execute executes the sql code after installation
```
INSERT INTO `users_department_mode` VALUES (1,'运维部','',1001);

INSERT INTO `users_customuser` VALUES (1,'pbkdf2_sha256$15000$uM1f5HMxHOqE$zPzKtNJMheQe62Q592V5l0m60nq/5Vj4rgzlVf5nXYs=','2016-01-14 18:16:27',1,'voilet@qq.com','admin','','','','04j4wtqxhtzts642w783nfukepx0w5jc',NULL,1,0,'3eceb1e9-df90-38ed-9960-03183bc85cce',0,1,'2015-12-29 14:05:50',NULL);
```

### Login user and password
* user: admin
* password: Admin_147258

## Project screenshots
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb1.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb10.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb2.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb9.png)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb3.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb4.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb5.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb6.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb7.jpg)
![sec](http://blog.kukafei520.net/wp-content/uploads/2016/01/cmdb8.jpg)

