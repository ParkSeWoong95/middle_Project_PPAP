import cx_Oracle
import mybatis_mapper2sql
from mylog import MyLog

class MyDaoMembers:
    def __init__(self):
        self.conn = cx_Oracle.connect('team5/java@192.168.41.5:1521/xe')
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mybatis_members.xml')[0]   
        
    def members_select_list(self):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql)
        list = []
        for record in rs:
            list.append({'mem_carnum':record[0],'mem_name':record[1],'mem_email':record[2],'mem_tel':record[3],'mem_pw':record[4],'mem_ticket_yn':record[5],'mem_exit_yn':record[6],'mem_black_yn':record[7],'sign_date':record[8],'signout_date':record[9],'mem_yn':record[10]})
        return list
    
    def members_select(self, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(mem_carnum, ))
        list = []
        for record in rs:
            list.append({'mem_carnum':record[0],'mem_name':record[1],'mem_email':record[2],'mem_tel':record[3],'mem_pw':record[4],'mem_ticket_yn':record[5],'mem_exit_yn':record[6],'mem_black_yn':record[7],'sign_date':record[8],'signout_date':record[9],'mem_yn':record[10]})
        return list
    
    def members_find_list(self, mem_name, mem_email):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "find_list")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(mem_name, mem_email))
        list = []
        for record in rs:
            list.append({'mem_carnum':record[0],'mem_name':record[1],'mem_email':record[2],'mem_tel':record[3],'mem_pw':record[4],'mem_ticket_yn':record[5],'mem_exit_yn':record[6],'mem_black_yn':record[7],'sign_date':record[8],'signout_date':record[9],'mem_yn':record[10]})
        return list
    
    def members_login(self,mem_carnum, mem_pw): #select 기능도 있음.
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_login")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum, mem_pw))
        list = []
        for record in rs:
            list.append({'mem_carnum':record[0],'mem_name':record[1],'mem_email':record[2],'mem_tel':record[3],'mem_pw':record[4],'mem_ticket_yn':record[5],'mem_exit_yn':record[6],'mem_black_yn':record[7],'sign_date':record[8],'signout_date':record[9],'mem_yn':record[10]})
        return list
    
    def members_insert(self, mem_carnum, mem_name, mem_email, mem_tel, mem_pw, mem_yn):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum, mem_name, mem_email, mem_tel, mem_pw, mem_yn))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_update(self, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_myp_update(self,mem_carnum, mem_name, mem_email, mem_tel, mem_pw):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "mp_update")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql,(mem_name, mem_email, mem_tel, mem_pw, mem_carnum))
        print('ㅎㅇ',sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_update_pw(self,mem_carnum, mem_pw): #비밀번호변경
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_pw")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_pw, mem_carnum))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_update_tow(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_tow")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum, ))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_update_buy_yn(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "buy_yn_update")
        MyLog().getLogger().debug(sql)
        print('111111')
        self.cs.execute(sql, (mem_carnum,))
        print(sql)
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_update_yn(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "yn_update")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum, ))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_delete(self,mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def members_update_mgr(self, mem_carnum, mem_name, mem_email, mem_tel, mem_pw, mem_ticket_yn, mem_black_yn, mem_yn):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "update_mgr")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum, mem_name, mem_email, mem_tel, mem_pw, mem_ticket_yn, mem_black_yn, mem_yn))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def members_delete_mgr(self, mem_carnum):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete_mgr")
        MyLog().getLogger().debug(sql)
        rs = self.cs.execute(sql, (mem_carnum,))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
    
    def __del__(self): 
        self.cs.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    dao = MyDaoMembers()
#     cnt = dao.members_insert(1, '지윤', 1, 1, 1, 'y')
#     cnt = dao.members_login('1', 1)
    email = dao.members_login("12바1245","1111")
    print(email)

    
    
    