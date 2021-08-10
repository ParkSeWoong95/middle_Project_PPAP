import cx_Oracle
import mybatis_mapper2sql

class MyDaoBook:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_book.xml')[0]   
    
    def book_select_list_book(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list_book")
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'book_seq':record[0],'book_buydate':record[1],'book_date':record[2],'book_cel_yn':record[3],
                         'mem_carnum':record[4],'parkinfo_seq':record[5],'prod_code':record[6]})
        return list
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        

    
    
    