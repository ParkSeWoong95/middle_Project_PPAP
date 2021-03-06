import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoBook:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_book.xml')[0]   
    
    def book_select_list_book(self, book_date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list_book")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(book_date,))
        list = []
        for record in rs:
            list.append({'book_seq':record[0],'book_buydate':record[1],'book_date':record[2],'book_cel_yn':record[3],
                         'mem_carnum':record[4],'parkinfo_seq':record[5],'prod_code':record[6]})
        return list
    
    def book_select_list_book_nu(self, mem_carnum,book_rnd):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list_book_nu")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(mem_carnum,book_rnd))
        list = []
        for record in rs:
            list.append({'book_seq':record[0],'book_buydate':record[1],'book_date':record[2],'book_cel_yn':record[3],
                         'mem_carnum':record[4],'parkinfo_seq':record[5],'book_rnd':record[6],'tid':record[7]})
        return list
    
    def book_select_list(self, date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (date, ))
        list = []
        for record in rs:
            list.append({'book_seq':record[0],'book_buydate':record[1],'book_date':record[2],'book_cel_yn':record[3],
                         'mem_carnum':record[4],'parkinfo_seq':record[5],'prod_code':record[6], 
                         'mem_name':record[7], 'mem_tel':record[8], 'book_state':record[9]})
        return list
    
    def book_select(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum,))
        list = []
        for record in rs:
            list.append({'book_seq':record[0],'book_buydate':record[1],'book_date':record[2],'book_cel_yn':record[3],'mem_carnum':record[4],'parkinfo_seq':record[5],'prod_code':record[6],'tid':record[7],'prod_price':record[8]})
        return list 
    
    def book_select_history(self,mem_carnum, date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_his")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum, date))
        list = []
        for record in rs:
            list.append({'book_seq':record[0],'book_buydate':record[1],'book_date':record[2],'book_cel_yn':record[3],'mem_carnum':record[4],'parkinfo_seq':record[5],'prod_code':record[6],'tid':record[7],'prod_price':record[8]})
        return list       
    
    def book_insert(self, book_date, book_cel_yn, mem_carnum, parkinfo_seq, prod_code, book_rnd, tid):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
        self.cs.execute(sql,(book_date, book_cel_yn, mem_carnum, parkinfo_seq, prod_code, book_rnd, tid))
        MyLog().getLogger().debug(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def book_update(self,mem_carnum, book_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update')
        self.cs.execute(sql,(mem_carnum, book_seq))
        print('sql',sql)
        MyLog().getLogger().debug(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def book_delete(self,mem_carnum,book_date):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete')
        self.cs.execute(sql,(mem_carnum,book_date))
        MyLog().getLogger().debug(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        

    
    
    