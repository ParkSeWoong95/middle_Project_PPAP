import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoBsug:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_bsug.xml')[0]
        
    def bsug_select_list(self, search):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (search, ))
        list = []
        for record in rs:
            list.append({'bsug_seq':record[0],'bsug_title':record[1],'bsug_content':record[2],'bsug_filename':record[3],'bsug_filepath':record[4],'bsug_hit':record[5],  'in_date':record[6],'in_user_id':record[7],'up_date':record[8]})
        return list
   
    def bsug_select(self,bsug_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (bsug_seq,) )
        obj = None
        for record in rs:
            obj = {'bsug_seq':record[0],'bsug_title':record[1],'bsug_content':record[2],'bsug_filename':record[3],'bsug_filepath':record[4],'bsug_hit':record[5],  'in_date':record[6],'in_user_id':record[7],'up_date':record[8],'mem_carnum':record[9],'in_user_id':record[10]}
        return obj
    
    
    def bsug_insert(self,bsug_seq, bsug_title, bsug_content, bsug_filename, bsug_filepath, bsug_hit, in_user_id,  mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bsug_title, bsug_content, bsug_filename, bsug_filepath, in_user_id ,mem_carnum))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

        
    def bsug_update(self,bsug_seq, bsug_title, bsug_content, bsug_filename, bsug_filepath):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bsug_title, bsug_content, bsug_filename, bsug_filepath, bsug_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bsug_hit(self,bsug_hit):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "hits")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bsug_hit,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bsug_del_img(self,bsug_seq, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "del_img")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (mem_carnum, bsug_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    
    def bsug_delete(self,bsug_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bsug_seq,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
       
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
        
        
if __name__ == "__main__":
    dao = MyDaoBsug()

    
    
    