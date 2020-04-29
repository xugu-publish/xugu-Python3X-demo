#Python3.X连接虚谷数据库的驱动demo示例  

下载该项目后，保持整体目录结构不变，修改deamon.py中的连接字符串，然后通过Python3运行deamon.py脚本即可。  

#使用说明
(1) 先将libxugusql.so文件移动至/usr/lib64/目录下  
(2) 然后在脚本文件中import xgcondb  

#目录结构  
deamon.py	虚谷数据库Python3.X驱动接口demo脚本  
xg_lob		存放大对象文件  
xgcondb		存放虚谷数据库Python3.X驱动接口动态库和__init__.py配置文件  

#demo主要演示XuGuPython3.X的以下几点功能：  
(1)  通过连接字符串连接虚谷数据库；  
(2)  执行DDL、不带参数的DML语句；  
(3)  执行带参数的SQL语句，通过按位置绑定的方式；  
(4)  批量插入；  
(5)  commit、autocommit方法的使用；  
(6)  description属性获取表信息；  
(7)  提取select语句产生的结构集；  
(8)  执行多结果集语句并提取结果集；  
(9)  大对象的导入和导出；  
(10) 执行存储过程、存储函数，参数类型有input、output  

#注意  
(1) 建议使用python3.7或python3.4版本运行该deamon示例脚本；  
(2) 若用户实际环境与当前驱动环境不一致，会出现不可预计的问题；  
(3) 有问题请与xugu官方联系  
