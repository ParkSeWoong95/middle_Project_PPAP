import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog


class MyDaoBfree:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_bfree.xml')[0]   
    
    def bfree_select_list(self, search):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(search,))
        list = []
        for record in rs:
            list.append({'bfree_seq':record[0], 'bfree_title':record[1], 'bfree_content':record[2], 'bfree_filename':record[3], 'bfree_filepath':record[4], 'bfree_hit':record[5], 
                         'bfree_rpseq':record[6], 'in_date':record[7], 'in_user_id':record[8], 'up_date':record[9], 'up_user_id':record[10], 'mem_carnum':record[11], 'mem_name':record[12]})
        return list
    
    def bfree_select(self, bfree_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(bfree_seq,))
        obj = None
        for record in rs:
            obj = {'bfree_seq':record[0], 'bfree_title':record[1], 'bfree_content':record[2], 'bfree_filename':record[3], 'bfree_filepath':record[4], 'bfree_hit':record[5], 
                         'bfree_rpseq':record[6], 'in_date':record[7], 'in_user_id':record[8], 'up_date':record[9], 'up_user_id':record[10], 'mem_carnum':record[11], 'mem_name':record[12]}
        return obj
    
    def bfree_insert(self, bfree_title, bfree_content, bfree_filename, bfree_filepath, in_user_id, up_user_id, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bfree_title, bfree_content, bfree_filename, bfree_filepath, in_user_id, up_user_id, mem_carnum))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bfree_update(self, bfree_seq, bfree_title, bfree_content, bfree_filename, bfree_filepath, up_user_id, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bfree_title, bfree_content, bfree_filename, bfree_filepath, up_user_id, bfree_seq, mem_carnum))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bfree_update_hitup(self, bfree_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_hitup")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bfree_seq,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def bfree_delete(self, bfree_seq, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bfree_seq, mem_carnum))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bfree_delete_file(self, bfree_seq, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete_file")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bfree_seq, mem_carnum))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
if __name__ == "__main__":
    dao = MyDaoBfree()
#     list = dao.Bfree_insert(4, "안녕", "hello", '','','','', '', '', '', '', "32가5029")
#     list = dao.Bfree_delete(4, "32가5029")
    
    print(list)
    
