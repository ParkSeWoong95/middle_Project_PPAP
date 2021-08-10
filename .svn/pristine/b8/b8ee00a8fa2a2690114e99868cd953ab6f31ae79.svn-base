import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoTow:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_tow.xml')[0]   
    
    def tow_select_list(self, date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (date, ))
        list = []
        for record in rs:
            list.append({'tow_seq':record[0],'mem_carnum':record[1],'mem_name':record[2],'tow_date':record[3],'tow_reason':record[4],'mem_tel':record[5],'sign_date':record[6],'mem_black_yn':record[7]})
        return list
    
    def tow_select(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum,))
        list = []
        for record in rs:
            list.append({'tow_seq':record[0],'mem_carnum':record[1],'tow_date':record[2],'tow_reason':record[3]})
        return list    
    
    def tow_insert(self, tow_reason, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
        self.cs.execute(sql,(tow_reason, mem_carnum))
        MyLog().getLogger().debug(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    dao = MyDaoTow();
#     cnt = dao.ticket_insert('32가5029', '1')
#     print(cnt)
    list = dao.tow_select('123수1234')
    print(list)
    
    
    