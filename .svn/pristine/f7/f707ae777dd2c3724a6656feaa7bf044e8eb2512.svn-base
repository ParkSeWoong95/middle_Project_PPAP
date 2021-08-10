import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog


class MyDaoParkinfo:

    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_parkinfo.xml')[0]   
        
    def parkinfo_select_uselist(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_use_yn")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'parkinfo_seq':record[0]})
        return list
    #--------------예약 하나당 주차 하나이기 때문에 select---------------------------
            
    def parkinfo_select(self, parkinfo_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (parkinfo_seq,))
        list = []
        for record in rs:
            list.append({'parkinfo_seq':record[0], 'parkinfo_ticket_yn':record[1], 'parkinfo_book_yn':record[2], 'parkinfo_use_yn':record[3]})
        return list
            
    def parkinfo_select_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'parkinfo_seq':record[0], 'parkinfo_ticket_yn':record[1], 'parkinfo_book_yn':record[2], 'parkinfo_use_yn':record[3]})
        return list
    
    def parkinfo_update(self, parkinfo_ticket_yn, parkinfo_book_yn, parkinfo_use_yn,parkinfo_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (parkinfo_ticket_yn, parkinfo_book_yn, parkinfo_use_yn, parkinfo_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def parkinfo_update_refund(self,parkinfo_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_refund")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (parkinfo_seq,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.close()

        
if __name__ == "__main__":
    dao = MyDaoParkinfo()
#     list = dao.parkinfo_select("1")
#     list = dao.parkinfo_update(1,'n','n','n')
#     print(list)
    
