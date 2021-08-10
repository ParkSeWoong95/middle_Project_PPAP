import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog
from _ast import If

class MyDaoSales:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_sales.xml')[0]   
    
    def sales_select_book(self,year):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_book")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (year,))
        list = []
        for record in rs:
            print('record',record)
            list.append({'user':record[0],'m1':record[1],'m2':record[2],'m3':record[3],'m4':record[4],'m5':record[5],'m6':record[6],'m7':record[7],'m8':record[8],'m9':record[9],'m10':record[10],'m11':record[11],'m12':record[12]})
        return list
    
    def sales_select_ticket(self,year):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_ticket")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (year,))
        list = []
        for record in rs:
            list.append({'user':record[0],'m1':record[1],'m2':record[2],'m3':record[3],'m4':record[4],'m5':record[5],'m6':record[6],'m7':record[7],'m8':record[8],'m9':record[9],'m10':record[10],'m11':record[11],'m12':record[12]})
        return list   
    
    def sales_select_book_circle(self,year):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_book_circle")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (year,))
        list = []
        for record in rs:
            list.append({'name':record[0],'price':record[1],'cnt':record[2]})
        return list  
    
    def sales_select_ticket_circle(self,year):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_ticket_circle")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (year,))
        list = []
        for record in rs:
            list.append({'name':record[0],'price':record[1],'cnt':record[2]})
        return list  
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
if __name__ == '__main__':
    year = '%'
    print(year)

    list1 = MyDaoSales().sales_select_book_circle(year)
    list2 = MyDaoSales().sales_select_ticket_circle(year)
    val = list(list1[0].values())
    val2 = []
    for n,v in enumerate(list2) :
        val2 += (list2[n].values())
        
    print(val)
    print(val2)
    
