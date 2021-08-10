import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog


class MyDaoAdmins:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_admins.xml')[0]   
    
    def admin_select(self, admin_id, admin_pw):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (admin_id, admin_pw))
        list = []
        for record in rs:
            list.append({'admin_id':record[0], 'admin_pw':record[1], 'admin_name':record[2]})
        return list
    
    def select_tow(self, carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_tow")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (carnum, ))
        list = []
        for record in rs:
            list.append({'tow_seq':record[0], 'tow_date':record[1], 'tow_reason':record[2], 'mem_carnum':record[3]})
        return list
    
    def admin_insert_tow(self, carnum, tow_reason, tow_date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert_tow")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (tow_date, tow_reason, carnum))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def admin_upBook(self, book_seq, carnum, book_date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_book")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (book_date, carnum, book_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def admin_book_cel(self, book_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_book_cel")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (book_seq, ))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
if __name__ == "__main__":
    dao = MyDaoAdmins()
#     list = dao.admin_select('admin')
    cnt = dao.del_tow("123수1234")
    print(cnt)
    
