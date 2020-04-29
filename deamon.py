#!/usr/local/bin/python3
import os
import datetime
import xgcondb

#连接字符串请视情况而定，输入自己本地的数据库服务器IP地址、端口等
conn=xgcondb.connect(host="127.0.0.1",port="5138",database="SYSTEM",user="SYSDBA", password="SYSDBA");
cur = conn.cursor()

#设置commit为False
conn.autocommit(False)

#执行不带参SQL、DDL语句
cur.execute("select count(*) from all_tables where table_name='TEST_DML';")
row = cur.fetchone()
if row[0] == 1:
	cur.execute("drop table test_dml;")
cur.execute("create table test_dml(col1 int, col2 boolean, col3 varchar, \
col4 datetime, col5 double, col6 numeric(13,6));")
cur.execute("insert into test_dml values(1,False,'xugu','2020-04-09 16:57:32',3.1415,123456.789);")
cur.execute("insert into test_dml values(2,True,'xugu','2020-04-09 16:58:32',3.1415,123456.789);")
cur.executemany("insert into test_dml values(3,True,'xugu','2020-04-09 16:59:32',3.1415,123456.789);")
sql = "insert into test_dml values(4,False,'xugu','2020-04-09 17:00:32',3.1415,123456.789);"
cur.executemany(sql)

#执行带参数SQL语句
sql1 = "insert into test_dml values(?,?,?,?,?,?);"
cur.setinputtype((xgcondb.XG_C_INTEGER,xgcondb.XG_C_BOOL,xgcondb.XG_C_CHAR, \
xgcondb.XG_C_DATETIME,xgcondb.XG_C_DOUBLE,xgcondb.XG_C_NUMERIC))	#设置参数数据类型

#dateime、time、date有两种传参方式，分别为字符串类型和各自对象类型
t_datetime = datetime.datetime.now()
cur.execute(sql1,(5,True,'xugu',t_datetime,3.1415,123456.789))			#指定为datetime对象类型，则参数应该为datetime对象
cur.cleartype()
cur.setinputtype((xgcondb.XG_C_INTEGER,xgcondb.XG_C_BOOL,xgcondb.XG_C_CHAR, \
xgcondb.XG_C_CHAR,xgcondb.XG_C_DOUBLE,xgcondb.XG_C_NUMERIC))		#重新设置参数数据类型

cur.execute(sql1,[6,True,'xugu','2020-04-09 17:01:32',3.1415,123456.789])	#指定为字符串类型，则参数应该为字符串
cur.execute(sql1,(7,True,'xugu','2020-04-09 17:02:32',3.1415,123456.789))
cur.executemany(sql1,(8,False,'xugu','2020-04-09 17:03:32',3.1415,123456.789))
cur.executemany(sql1,[9,False,'xugu','2020-04-09 17:04:32',3.1415,123456.789])
cur.executemany(sql1,([10,False,'xugu','2020-04-09 17:05:32',3.1415,123456.789],[11,False,'xugu','2020-04-09 17:06:32',3.1415,123456.789]))
cur.executemany(sql1,[(12,False,'xugu','2020-04-09 17:07:32',3.1415,123456.789),(13,False,'xugu','2020-04-09 17:08:32',3.1415,123456.789)])

#批量插入
t_list_1 = []
t_list_2 = []
i = 14
while i <= 5000:
	t_list_1.append(i)
	t_list_2.append('xugu'+str(i))
	i = i + 1
cur.cleartype()
cur.setinputtype((xgcondb.XG_C_INTEGER,xgcondb.XG_C_CHAR))
cur.executebatch("insert into test_dml(col1,col3) values(?,?);",(t_list_1,t_list_2))

#commit提交
conn.commit()
conn.autocommit(True)

#获取表信息
cur.execute("select * from test_dml;")
row = cur.description
print("create table info:")
for index in row:
	print(index)
row = cur.rowcount
print("")
print("'select * from test_dml' is the number of rows in the result set(rowcount)",row)

#其他dml语句操作
cur.execute("select count(*) from test_dml where col5 is null;")
row = cur.fetchone()
print("")
print("The number of rows that were empty before update col5:",row[0])
cur.execute("update test_dml set col5=3.1415 where col5 is null;")
cur.execute("select count(*) from test_dml where col5 is null;")
row = cur.fetchone()
print("The number of rows where update col5 is empty:",row[0])

cur.execute("select count(*) from test_dml;")
row = cur.fetchone()
print("")
print("Number of rows of data before delete:",row[0])
cur.execute("delete from test_dml where col4 is null;")
cur.execute("select count(*) from test_dml;")
row = cur.fetchone()
print("Number of rows after delete:",row[0])

#fetchmany
cur.execute("select * from test_dml;")
cur.arraysize = 5
row = cur.fetchmany()
print("")
print("fetchmany:")
for index in row:
	print(index)
row = cur.fetchmany(size=4)
for index in row:
	print(index)

#fetchall
cur.execute("select * from test_dml;")
row = cur.fetchall()
print("")
print("fetchall:")
for index in row:
	print(index)

#多结果集
print("Examples of multiple result sets: select count(*) from test_dml;select * from test_dml;")
cur.execute("select count(*) from test_dml; select * from test_dml;")
row = cur.fetchone()
print("")
print("The first result set:",row)
cur.nextset()
row = cur.fetchall()
print("The second result set:",row)

#大对象导入
cur.execute("select count(*) from all_tables where table_name='TEST_LOB';")
row = cur.fetchone()
if row[0] == 1:
        cur.execute("drop table test_lob;")
cur.execute("create table test_lob(col1 int, col2 clob, col3 blob);")

clob_fp = open("./xg_lob/test_clob.txt","r")
blob_fp = open("./xg_lob/test_blob.jpg","rb")
clob_buf = clob_fp.read()
blob_buf = blob_fp.read()
cur.cleartype()
cur.setinputtype((xgcondb.XG_C_INTEGER,xgcondb.XG_C_CLOB,xgcondb.XG_C_BLOB))
cur.execute("insert into test_lob values(?,?,?);",(1,clob_buf,blob_buf))
cur.execute("select len(col2),len(col3) from test_lob where col1=1;")
row = cur.fetchone()
print("")
print("CLOB length is",row[0])
print("BLOB length is",row[1])

#大对象导出
cur.execute("select * from test_lob;")
row = cur.fetchone()
clob_fd = open("./xg_lob/getClob.txt","w+")
blob_fd = open("./xg_lob/getBlob.jpg","wb+")
clob_fd.write(row[1])
blob_fd.write(row[2])
if len(clob_buf)==len(row[1]) and len(blob_buf)==len(row[2]):
	print("")
	print("The large object was successfully exported with the same length of data")

#执行存储过程
cur.execute("select count(*) from all_tables where table_name='TEST_EXEC';")
row = cur.fetchone()
if row[0] == 0:
        cur.execute("create table test_exec(col1 int, col2 varchar, col3 numeric(13,6));")
else:
        cur.execute("truncate table test_exec;")
#无参数存储过程
cur.execute("CREATE OR REPLACE PROCEDURE exec_proc_test1() IS \
DECLARE \
str VARCHAR; \
BEGIN \
        FOR i IN 1..100 LOOP \
                str:='insert into test_exec(col1,col2) values('||i||',''aa'||i||''')'; \
                EXECUTE IMMEDIATE str; \
        END LOOP; \
END;");
row = cur.callproc("exec_proc_test1")
print("")
print("Execute the parameterless stored procedure to return the result set:",row)

#input参数存储过程
cur.execute("truncate table test_exec;")
cur.execute("CREATE OR REPLACE PROCEDURE exec_proc_test1(d1 int, d2 varchar, d3 numeric(13,6)) IS \
DECLARE \
str VARCHAR; \
BEGIN \
        FOR i IN 1..d1 LOOP \
                str:='insert into test_exec values('||i||',''aa'||i||''','||d3||')'; \
                EXECUTE IMMEDIATE str; \
        END LOOP; \
END;");
cur.cleartype()
cur.setinputtype((xgcondb.XG_C_INTEGER,xgcondb.XG_C_CHAR,xgcondb.XG_C_NUMERIC))
row = cur.callproc("exec_proc_test1",(50,'xugu','2020.0410'),(1,1,1))
print("")
print("The collection of parameters when the input parameter stored procedure is executed: [50, 'xugu', 2020.041]")
print("Execute the input type parameter stored procedure to return the result collection: ",row)

#output参数存储过程
cur.execute("truncate table test_exec;")
cur.execute("CREATE OR REPLACE PROCEDURE exec_proc_test1(d1 int,d2 out int,d3 out numeric(13,6)) IS \
DECLARE \
str VARCHAR; \
BEGIN \
        FOR i IN 1..d1 LOOP \
                str:='insert into test_exec(col1,col2) values('||i||',''aa'||i||''')'; \
                EXECUTE IMMEDIATE str; \
        END LOOP; \
        select count(*) into d2 from test_exec; \
        d2:=d2+d1; \
        d3:=123456.789; \
END;");
cur.cleartype()
cur.setinputtype((xgcondb.XG_C_INTEGER,xgcondb.XG_C_INTEGER,xgcondb.XG_C_NUMERIC))
row = cur.callproc("exec_proc_test1",(50,1,'2020.041'),(1,2,2))
print("")
print("The set of parameters when the output parameter stored procedure is executed:  [50, 1, 2020.041]")
print("Execute the output parameter stored procedure to return the result collection:",row)

#执行存储函数
cur.execute("truncate table test_exec;")
cur.execute("CREATE OR REPLACE function exec_func_test1(d1 int) return varchar IS \
DECLARE \
str VARCHAR; \
val varchar;\
val1 varchar;\
BEGIN \
        FOR i IN 1..d1 LOOP \
                str:='insert into test_exec(col1,col2) values('||i||',''aa'||i||''')'; \
                EXECUTE IMMEDIATE str; \
        END LOOP; \
        val1:='hello world!';\
        val:=val1+'good everybody!';\
        return val;\
END;")
cur.cleartype()
cur.setinputtype((xgcondb.XG_C_INTEGER,xgcondb.XG_C_CHAR))
row = cur.callfunc("exec_func_test1",(50,),(1,))
print("")
print("A collection of arguments when a stored function is executed:  [50]")
print("The collection of arguments returned by the execution store function:",row)

#删除表格
cur.cleartype()
cur.close()
conn.close()
