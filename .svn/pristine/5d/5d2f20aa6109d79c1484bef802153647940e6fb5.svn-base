import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoBnotice:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_bnotice.xml')[0]
        
    def bnotice_select_list(self, admin):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(admin,))
        list = []
        for record in rs:
            list.append({'bnotice_seq':record[0],'bnotice_title':record[1],'bnotice_content':record[2],'bnotice_filename':record[3],
                         'bnotice_filepath':record[4],'bnotice_hit':record[5], 'in_date':record[6], 'in_user_id':record[7], 'up_date':[8]})
        print("list는:",list)
        
        return list
    
    def bnotice_select(self, b_notice_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (b_notice_seq,) )
        obj = None
        for record in rs:
            obj = {'bnotice_seq':record[0],'bnotice_title':record[1],'bnotice_content':record[2],'bnotice_filename':record[3],
                   'bnotice_filepath':record[4],'bnotice_hit':record[5], 'in_date':record[6], 'in_user_id':record[7], 'up_date':[8],'display_yn':record[9]}
        return obj
    
    def bnotice_search_list(self, admin, search):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "search_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(search, admin))
        list = []
        for record in rs:
            list.append({'bnotice_seq':record[0],'bnotice_title':record[1],'bnotice_content':record[2],'bnotice_filename':record[3],
                         'bnotice_filepath':record[4],'bnotice_hit':record[5], 'in_date':record[6], 'in_user_id':record[7], 'up_date':[8]})
        return list
    
#     def select_list_admin(self,):
#         sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list_admin")
#         MyLog().getLogger().debug(sql)
#         rs = self.cs.execute(sql,)
#         list = []
#         for record in rs:
#             list.append({'bnotice_seq':record[0],'bnotice_title':record[1],'bnotice_content':record[2],'bnotice_filename':record[3],
#                          'bnotice_filepath':record[4],'bnotice_hit':record[5], 'in_date':record[6], 'in_user_id':record[7], 'up_date':[8]})
#         return list
        
    def bnotice_insert(self, bnotice_title, bnotice_content, bnotice_filename, bnotice_filepath, in_user_id, display_yn):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (bnotice_title, bnotice_content, bnotice_filename, bnotice_filepath, in_user_id, display_yn))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

        
    def bnotice_update(self, b_notice_seq, b_notice_title, b_notice_content, b_notice_filepath, b_notice_filename, display_yn):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (display_yn, b_notice_title, b_notice_content, b_notice_filepath, b_notice_filename, b_notice_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bnotice_delete(self, b_notice_seq):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (b_notice_seq,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bnotice_hit(self, b_notice_hit):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "hit_add")        
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (b_notice_hit,))   
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def bnotice_del_img(self,b_notice_seq, up_user_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "del_img")  
        MyLog().getLogger().debug(sql)
        self.cs.execute(sql, (up_user_id, b_notice_seq))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
if __name__ == "__main__":
    dao = MyDaoBnotice()
#     cnt = dao.bnotice_update(3, "주차장공지3", "오늘로써 주차장이 끝납니다. 이용해주셔서 감사합니다.", " ", " ", 'y')
#     print(cnt)

    
    
    