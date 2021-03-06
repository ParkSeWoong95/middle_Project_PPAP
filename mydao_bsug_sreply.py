import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog


class MyDao_Bsug_Sreply:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_bsug_sreply.xml')[0]
        
    def bsug_select(self,bsug_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (bsug_seq,))
        list = []
        print(sql);
        for record in rs:
            print(record)
            list.append({'r_seq':record[0],'bsug_seq':record[1],'cmt':record[2],'in_date':record[3],'in_user_id':record[4],'up_date':record[5], 'up_user_id':record[6],'in_user_name':record[7]})
        return list
    
    
    
    def bsug_insert(self, bsug_seq, cmt, in_user_id, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bsug_seq, cmt, in_user_id, up_user_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

        
    def bsug_update(self, cmt, up_user_id,r_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (cmt, up_user_id, r_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    
    def bsug_delete(self,r_seq,bsug_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (r_seq, bsug_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bsug_delete_all(self,bsug_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete_all")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bsug_seq,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    dao = MyDao_Bsug_Sreply()
#     cnt = dao.myinsert('1','??????','?????????', '?????????')
#     cnt = dao.myupdate('???????????????', '??????', '1')
#     cnt = dao.mydelete('1')

    
    
    