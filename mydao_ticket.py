import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoTicket:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_ticket.xml')[0]   
    
    def ticket_select_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'ticket_seq':record[0],'ticket_sdate':record[1],'ticket_edate':record[2],'mem_carnum':record[3],'prod_code':record[4]})
        return list
    
    def ticket_select(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum,))
        list = []
        for record in rs:
            list.append({'ticket_seq':record[0],'ticket_sdate':record[1],'ticket_edate':record[2],'mem_carnum':record[3],'prod_code':record[4],'refund_yn':record[5],'prod_name':record[6],'prod_price':record[7],'parkinfo_seq':record[8]})
        return list   
    
    def ticket_select_date(self,mem_carnum, date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_date")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum, date ))
        list = []
        for record in rs:
            list.append({'ticket_seq':record[0],'ticket_sdate':record[1],'ticket_edate':record[2],'mem_carnum':record[3],'prod_code':record[4],'refund_yn':record[5],'prod_name':record[6],'prod_price':record[7],'parkinfo_seq':record[8]})
        return list   


    def ticket_refund_select(self,ticket_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_refund")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (ticket_seq,))
        list = []
        for record in rs:
            list.append({'ticket_seq':record[0],'ticket_sdate':record[1],'ticket_edate':record[2],'mem_carnum':record[3],'prod_code':record[4],'tid':record[5],'prod_name':record[6],'prod_price':record[7],'parkinfo_seq':record[8]})
        return list    
    
    def ticket_insert(self, adddate, mem_carnum, prod_code, tid, parkinfo_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
        self.cs.execute(sql,(adddate, mem_carnum, prod_code, tid, parkinfo_seq))
        print(sql)
        MyLog().getLogger().debug(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def ticket_refund_update(self, tid):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (tid,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def ticket_refund_update_render1(self, date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_render1")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (date,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    def ticket_refund_update_render2(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_render2")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    def ticket_refund_update_render3(self, date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_render3")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (date,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    print(1)
    dao = MyDaoTicket();
    print(2)
#     cnt = dao.ticket_insert('32가5029', '1')
#     print(cnt)
    list = dao.ticket_select_list()
    print(list)
    
    
    