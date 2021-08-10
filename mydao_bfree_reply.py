import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog


class MyDao_Bfree_reply:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_bfree_reply.xml')[0]
        
    def bfree_reply_select(self,bfree_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'select')
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(bfree_seq,))
        list = [] 
        
        for x in rs:
            list.append({'r_seq':x[0],'bfree_seq':x[1],'cmt':x[2],'in_date':x[3],'in_user_id':x[4],'up_date':x[5],'up_user_id':x[6],'in_user_name':x[7],'good':x[8],'bad':x[9]})
        return list
    
    def bfree_reply_insert(self,bfree_seq,cmt,in_user_id,up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'insert')
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(bfree_seq,bfree_seq,cmt,in_user_id,up_user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def bfree_reply_update(self,r_seq,bfree_seq,cmt,up_user_id,in_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'update')
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(cmt,in_user_id,r_seq,bfree_seq,up_user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bfree_reply_upgood(self,r_seq,bfree_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'good')
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(r_seq,bfree_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bfree_reply_upbad(self,r_seq,bfree_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'bad')
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(r_seq,bfree_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bfree_reply_delete(self,r_seq,bfree_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete')
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(r_seq,bfree_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bfree_reply_deleteAll(self,bfree_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, 'delete_all')
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql,(bfree_seq,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
