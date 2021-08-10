import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoNticket:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_nticket.xml')[0]   
        
    def nticket_select_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'nticket_seq':record[0],'nticket_indate':record[1],'nticket_outdate':record[2],'mem_carnum':record[3],'parkinfo_seq':record[4],'prod_code':record[5]})
        return list
    
    def nticket_select(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum,))
        list = []
        for record in rs:
            list.append({'nticket_seq':record[0],'nticket_indate':record[1],'nticket_outdate':record[2],'mem_carnum':record[3],'parkinfo_seq':record[4],'prod_code':record[5]})
        return list    
    
    def nticket_insert(self, mem_carnum, parkinfo_seq, prod_code):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
        self.cs.execute(sql,(mem_carnum, parkinfo_seq, prod_code))
        MyLog().getLogger().debug(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def nticket_update(self, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update')
        self.cs.execute(sql,(mem_carnum,))
        MyLog().getLogger().debug(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    dao = MyDaoNticket();
#     list = dao.nticket_insert('32가5029', '1', '1')
#     list = dao.nticket_update('32가5029')
#     list = dao.nticket_select_list()
    list = dao.nticket_select('32가5029')
    print(list)
    
    
    