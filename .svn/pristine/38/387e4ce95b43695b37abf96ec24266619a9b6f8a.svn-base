import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoProd:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_prod.xml')[0]
        
    def prod_select_list(self,):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,)
        list = []
        for record in rs:
            list.append({'prod_code':record[0],'prod_dcode':record[1],'prod_name':record[2],'prod_price':record[3]})
        return list
    
    def prod_select(self,prod_code):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (prod_code,) )
        obj = None
        for record in rs:
            obj ={'prod_code':record[0],'prod_dcode':record[1],'prod_name':record[2],'prod_price':record[3]}
        return obj
    
    def prod_select_pay(self,):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_pay")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,)
        list = []
        for record in rs:
            list.append({'prod_code':record[0],'prod_dcode':record[1],'prod_name':record[2],'prod_price':record[3]})
        return list
    
    
    def prod_insert(self, prod_dcode, prod_name, prod_price):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "prod_insert")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (prod_name, prod_price, prod_dcode))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

    def prod_update(self, prod_code, prod_price):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "prod_update") 
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (prod_price, prod_code))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def prod_delete(self, prod_code):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "prod_delete")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (prod_code,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

if __name__ == "__main__":
    dao = MyDaoProd()
#     cnt = dao.prod_insert("4개월정기권", 250000, "정기권")
#     print(cnt)