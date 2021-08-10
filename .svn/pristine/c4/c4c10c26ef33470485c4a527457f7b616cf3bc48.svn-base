import cx_Oracle
import mybatis_mapper2sql

class MyDaoTicket:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_ticket.xml')[0]   
    
    def ticket_select_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'ticket_seq':record[0],'ticket_sdate':record[1],'ticket_edate':record[2],'mem_carnum':record[3],'prod_code':record[4],'refund_yn':record[5],'parkinfo_seq':record[6]})
        return list
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
