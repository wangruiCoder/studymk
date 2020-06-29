import cx_Oracle
dsn = cx_Oracle.makedsn('10.10.196.218','1521','ORACLE2')
conn = cx_Oracle.connect('x5user','x5user',dsn)
c = conn.cursor()
str = c.var(cx_Oracle.CURSOR)
str2 = c.callproc('pack_pollutant.proc_pollutantdata',[str])
rs = str2[-1].fetchall()
print(rs)
c.close
conn.close



str = c.var(cx_Oracle.NUMBER)
str2=c.callproc('proc_s2_back',[str])
print(str2)