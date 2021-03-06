from datetime import datetime
import os, requests
import random
import string
import json

import cx_Oracle
from flask import Flask, render_template, jsonify, request, session, escape, redirect, send_file
from werkzeug.utils import secure_filename

from mydao_admins import MyDaoAdmins
from mydao_bfree import MyDaoBfree
from mydao_bnotice import MyDaoBnotice
from mydao_bsug import MyDaoBsug
from mydao_bsug_sreply import MyDao_Bsug_Sreply
from mydao_members import MyDaoMembers
from mydao_prod import MyDaoProd
from mydao_ticket import MyDaoTicket
from mydao_nticket import MyDaoNticket
from mydao_bfree_reply import MyDao_Bfree_reply
from mydao_tow import MyDaoTow
from mydao_book import MyDaoBook

from mymail import MyMail
from mydao_parkinfo import MyDaoParkinfo
from calendar import prweek
from mydao_sales import MyDaoSales


app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = "ABCDEFG"
DIR_UPLOAD = "V:/"

# Session ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def getSession():
    mem_carnum = ""
    
    try:
        mem_carnum = str(escape(session["mem_carnum"]))
    except:
        pass
    
    if mem_carnum == "" :
        return False,mem_carnum
    else :
        return True,mem_carnum
# RENDERING ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/login")
def login_render():
    return render_template('login.html')

@app.route("/logout")
def logout_render():
    session.clear()
    return redirect("main")

# 회원가입 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
@app.route('/join.ajax', methods=['POST'])
def join_ajax():
    mem_name = request.form["mem_name"]
    email = request.form["email"]
    mem_tel = request.form["mem_tel"]
    carnum = request.form["carnum"]
    pwd = request.form["pwd"]
    
    cnt = MyDaoMembers().members_insert(carnum, mem_name, email, mem_tel, pwd, 'y')
     
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"
 
    return jsonify(msg = msg)

@app.route('/dupl.ajax', methods=['POST'])
def dupl_ajax():
    carnum = request.form["carnum"]
    
    list = MyDaoMembers().members_select(carnum)

    msg = ""
    if len(list) == 1:
        msg = "ng"
    else:
        msg = "ok"

    return jsonify(msg = msg)

@app.route('/mail_check.ajax', methods=['POST'])
def mail_check_ajax():
    email = request.form["email"]
    
    _LENGTH = 8 # 8자리  
    
    # 숫자 + 대소문자
    string_pool = string.ascii_letters + string.digits # 랜덤한 문자열 생성
     
    result = "" 
    for i in range(_LENGTH) : 
        result += random.choice(string_pool) # 랜덤한 문자열 하나 선택 
    
    content = "이메일 확인 인증키를 입력해주세요.\n\n"
    content += "인증키 : "+result 
    
    MyMail().mysendmail(email, "PPAP 이메일 인증", content)

    msg = "ok"
    return jsonify(msg = msg, rnd_check = result)

#차량번호, 비밀번호 찾기ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
@app.route('/find.ajax', methods=['POST'])
def find_ajax():
    mem_name = request.form["mem_name"]
    email = request.form["email"]
    
    list = MyDaoMembers().members_find_list(mem_name, email)
    
    msg = ""
    if len(list) > 0:
        content_member = ""
        cnt = 0
        for idx, member in enumerate(list) :
            if member["mem_name"] == mem_name and member["mem_email"] == email :
                content_member += str(idx+1)+". "+ member["mem_carnum"] + "\n"
                cnt += 1
        
        print("cnt : "+str(cnt))
        
        if cnt == 0 :
            msg = "ng"
            return jsonify(msg = msg)
        
        msg = "ok"
        content = mem_name+"님의 이름과 입력해주신 이메일로 가입된 차량번호입니다.\n\n"+content_member
        MyMail().mysendmail(email, "PPAP 차량번호 찾기 안내메일", content)
        
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route('/find_pw.ajax', methods=['POST'])
def find_pw_ajax():
    carnum = request.form["carnum"]
    mem_name = request.form["mem_name"]
    email = request.form["email"]
    
    list = MyDaoMembers().members_select(carnum)
    
    msg = ""
    if len(list) > 0:
        cnt = 0
        for member in list :
            if member["mem_name"] == mem_name and member["mem_email"] == email :
                cnt += 1
        
        if cnt == 0 :
            msg = "ng"
            return jsonify(msg = msg)
        
        _LENGTH = 8 # 8자리  
        
        # 숫자 + 대소문자
        string_pool = string.ascii_letters + string.digits # 랜덤한 문자열 생성
         
        tmp_pwd = "" 
        for i in range(_LENGTH) : 
            tmp_pwd += random.choice(string_pool) # 랜덤한 문자열 하나 선택 
        
        pw_cnt = MyDaoMembers().members_update_pw(carnum, tmp_pwd)
        
        if pw_cnt == 0 :
            msg = "ng"
            return jsonify(msg = msg)
         
        msg = "ok"
        content = mem_name+"님의 ["+carnum+"] 차량 임시비밀번호는 '"+tmp_pwd+"' 입니다.\n로그인 후 비밀번호를 바꿔주세요."
        MyMail().mysendmail(email, "PPAP 임시비밀번호 발급 안내", content)
        
    else:
        msg = "ng"

    return jsonify(msg = msg)


# 비회원 로그인ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/")
@app.route("/main")
def main_render():
    flag_ses, mem_carnum = getSession()
    
    return render_template('main.html')

# 게시판 메인ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/b_notice")
def b_notice_render():
    search = request.args.get("search")
    flag_ses, mem_carnum = getSession()
    
    searchlist = MyDaoBnotice().bnotice_search_list(mem_carnum, search)
    return render_template('board/b_notice.html', searchlist=searchlist)

@app.route("/b_free")
def b_free_render():
    search = request.args.get("search")
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    
    list = MyDaoBfree().bfree_select_list(search)
    return render_template('board/b_free.html', list=list)

@app.route("/b_sug")
def b_sug_render():
    search = request.args.get("search")
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")  
    
    list = MyDaoBsug().bsug_select_list(search)
    return render_template('board/b_sug.html', list=list)
# 건의사항 제거

# 게시글 상세보기 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/b_notice_detail")
def b_notice_detail_render():
    bnotice_seq = request.args.get("bnotice_seq")
    
    cnt = MyDaoBnotice().bnotice_hit(bnotice_seq)
    obj = MyDaoBnotice().bnotice_select(bnotice_seq)
    
    return render_template('board/b_notice_detail.html', obj=obj, cnt=cnt)

@app.route("/b_free_detail")
def b_free_detail_render():
    bfree_seq = request.args.get("bfree_seq")
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    
    cnt = MyDaoBfree().bfree_update_hitup(bfree_seq)
    free = MyDaoBfree().bfree_select(bfree_seq)
    print(free)
    if not(str(free['bfree_filepath']).endswith("gif") or str(free['bfree_filepath']).endswith("jpg") or str(free['bfree_filepath']).endswith("jfif") or str(free['bfree_filepath']).endswith("jpeg") or str(free['bfree_filepath']).endswith("png"))  :
        free['bfree_filepath'] = ""
    
    return render_template('board/b_free_detail.html', free=free)

@app.route("/b_sug_detail")
def b_sug_detail_render():
    bsug_seq = request.args.get('bsug_seq')
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    
    cnt = MyDaoBsug().bsug_hit(bsug_seq)
    obj = MyDaoBsug().bsug_select(bsug_seq)
    return render_template('board/b_sug_detail.html', sug=obj, enumerate=enumerate)

@app.route('/b_sug_file_del.ajax', methods=['POST'])
def b_sug_file_del_ajax():
    bsug_seq = request.form["bsug_seq"]
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    
    
    cnt = MyDaoBsug().bsug_del_img(bsug_seq, mem_carnum)
    
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"
    return jsonify(msg = msg)

################### sug 댓글 구현 ####################
@app.route('/b_sug_reply_add.ajax', methods=['POST'])
def b_sug_reply_add_ajax():
    
    bsug_seq = request.form["bsug_seq"]
    cmt = request.form["cmt"]
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")    

    in_user_id = mem_carnum
    up_user_id = mem_carnum
    
    cnt = MyDao_Bsug_Sreply().bsug_insert(bsug_seq, cmt, in_user_id, up_user_id)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route("/b_sug_reply_list.ajax", methods=['POST'])
def b_sug_reply_list_ajax():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")  
      
    bsug_seq = request.form["bsug_seq"]
    
    list = MyDao_Bsug_Sreply().bsug_select(bsug_seq)
    return jsonify(list=list)

@app.route('/b_sug_reply_del.ajax', methods=['POST'])
def b_sug_reply_del_ajax():
    r_seq = request.form["r_seq"]
    bsug_seq = request.form["bsug_seq"]
    flag_ses,user_id=getSession()
    if not flag_ses :
        return redirect("login")
    cnt = MyDao_Bsug_Sreply().bsug_delete(r_seq, bsug_seq)
    msg = ""
    if cnt > 0 :
        msg = "ok"
    else :
        msg = "ng"
    return jsonify(msg = msg)


#####################################################################
# 게시글 작성 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/b_notice_add")
def b_notice_add_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 
    return render_template('board/b_notice_add.html')

@app.route("/b_free_add")
def b_free_add_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    return render_template('board/b_free_add.html')

@app.route("/b_sug_add")
def b_sug_add_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")   
    return render_template('board/b_sug_add.html')

@app.route("/b_notice_addact", methods=['POST'])
def b_notice_addact_render():
    title       = request.form["title"]
    content     = request.form["content"]
    display_yn     = request.form["display_yn"]
    in_user_id = str(session["mem_carnum"])
    mem_carnum = str(session["mem_carnum"])
    file = request.files['file']
    attach_path_temp = secure_filename(file.filename)
    attach_file_temp = str(datetime.today().strftime("%Y%m%d%H%M%S")) + "_" + attach_path_temp
    file.save(os.path.join(DIR_UPLOAD, attach_file_temp))
    
    b_notice_filename   = attach_file_temp
    b_notice_filepath   = DIR_UPLOAD
    
    if file :
        b_notice_filepath = b_notice_filepath
        b_notice_filename = b_notice_filename
    else :
        b_notice_filepath = ""
        b_notice_filename = ""
    
    print('-----------------')
    print(b_notice_filepath)    
    print(b_notice_filename)  
    print('-----------------')
    
    cnt = MyDaoBnotice().bnotice_insert(title, content, b_notice_filename, b_notice_filepath, in_user_id, display_yn)
    return render_template('board/b_notice_addact.html', cnt=cnt)

@app.route("/b_free_addact", methods=['POST'])
def b_free_addact_render():
    bfree_title       = request.form["title"]
    bfree_content     = request.form["content"]
    in_user_id = str(session["mem_carnum"])
    up_user_id = str(session["mem_carnum"])
    mem_carnum = str(session["mem_carnum"])
    file = request.files['file']
    attach_file_temp = secure_filename(file.filename)
    attach_path_temp = str(datetime.today().strftime("%Y%m%d%H%M%S")) + "_" + attach_file_temp
    file.save(os.path.join(DIR_UPLOAD, attach_path_temp))
    
    bfree_filename = ""
    bfree_filepath = ""
    if file :
        bfree_filename = attach_path_temp
        bfree_filepath = attach_file_temp
        print("file O")
    else :
        print("file X")
        
    cnt = MyDaoBfree().bfree_insert(bfree_title, bfree_content, bfree_filename, bfree_filepath, in_user_id, up_user_id, mem_carnum)
    
    return render_template('board/b_free_addact.html',cnt=cnt)

@app.route("/b_sug_addact", methods=['POST'])
def b_sug_addact_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")  
     
    bsug_title       = request.form["bsug_title"]
    bsug_content     = request.form["bsug_content"]
    
    file = request.files['file']
    attach_file_temp = secure_filename(file.filename)
    attach_path_temp = str(datetime.today().strftime("%Y%m%d%H%M%S")) + "_" + attach_file_temp
    file.save(os.path.join(DIR_UPLOAD, attach_path_temp))
    
    bsug_filename = ""
    bsug_filepath = ""
    if file :
        bsug_filename = attach_file_temp
        bsug_filepath = attach_path_temp
        print("file O")
    else :
        print("file X")
      
    cnt = MyDaoBsug().bsug_insert('', bsug_title, bsug_content, bsug_filename, bsug_filepath, '',  mem_carnum,  mem_carnum)

    return render_template('board/b_sug_addact.html')

# 리플작성 ---------------------------------
@app.route('/reply_add.ajax', methods=['POST', 'Get'])
def reply_add_ajax():
    bfree_seq = request.form["bfree_seq"]
    cmt = request.form["cmt"]
    flag_ses, mem_carnum=getSession()
    in_user_id = mem_carnum
    up_user_id = mem_carnum
    
    cnt = MyDao_Bfree_reply().bfree_reply_insert(bfree_seq, cmt, in_user_id, up_user_id)
    msg = ""
    if cnt > 0 :
        msg = "ok"
    else :
        msg = "ng"
    return jsonify(msg = msg)

@app.route('/reply_list.ajax', methods=['POST'])
def reply_list_ajax():
    bfree_seq = request.form["bfree_seq"]
    list = MyDao_Bfree_reply().bfree_reply_select(bfree_seq)
    return jsonify(list = list)

@app.route('/reply_bad.ajax', methods=['POST'])
def reply_bad_ajax():
    bfree_seq = request.form["bfree_seq"]
    r_seq = request.form["r_seq"]
    cnt = MyDao_Bfree_reply().bfree_reply_upbad(r_seq, bfree_seq)
    msg = ""
    if cnt > 0 :
        msg = "ok"
    else :
        msg = "ng"
    return jsonify(msg = msg)

@app.route('/reply_good.ajax', methods=['POST'])
def reply_good_ajax():
    bfree_seq = request.form["bfree_seq"]
    r_seq = request.form["r_seq"]
    flag_ses, user_id = getSession()
    if not flag_ses :
        return redirect("login")
    cnt = MyDao_Bfree_reply().bfree_reply_upgood(r_seq, bfree_seq)
    msg = ""
    if cnt > 0 :
        msg = "ok"
    else :
        msg = "ng"
    return jsonify(msg = msg)

@app.route('/reply_del.ajax', methods=['POST'])
def reply_del_ajax():
    r_seq = request.form["r_seq"]
    bfree_seq = request.form["bfree_seq"]
    flag_ses, user_id = getSession()
    if not flag_ses :
        return redirect("login")
    cnt = MyDao_Bfree_reply().bfree_reply_delete(r_seq, bfree_seq)
    msg = ""
    if cnt > 0 :
        msg = "ok"
    else :
        msg = "ng"
    return jsonify(msg = msg)

# 게시물 수정 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/b_notice_mod")
def b_notice_mod_render():
    b_notice_seq = request.args.get('b_notice_seq')
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses :
        return redirect("login")
    
    obj = MyDaoBnotice().bnotice_select(b_notice_seq)
    return render_template('board/b_notice_mod.html', obj=obj)

@app.route("/b_notice_modact", methods=['POST', 'Get'])
def b_notice_modact_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses :
        return redirect("login")
    
    b_notice_seq            = request.form['b_notice_seq']
    b_notice_title          = request.form['b_notice_title']
    b_notice_content        = request.form['b_notice_content']
    b_notice_diplay_yn      = request.form['b_notice_diplay_yn']
    b_notice_filename       = request.form['b_notice_filename']
    b_notice_filepath       = request.form['b_notice_filepath']
    file                    = request.files['file']
    
    if file:
        attach_file_temp    = secure_filename(file.filename) # 파일 이름만 뽑아서 
        attach_file_temp    = str(datetime.today().strftime("%Y%m%d%H%M%S")) + "_" + attach_file_temp # 앞 뒤에 있을 떄 차이?
        file.save(os.path.join(DIR_UPLOAD, attach_file_temp))
        b_notice_filename   = attach_file_temp
        b_notice_filepath   = DIR_UPLOAD
        print("file O")
    
    cnt = MyDaoBnotice().bnotice_update(b_notice_seq, b_notice_title, b_notice_content, b_notice_filepath, b_notice_filename, b_notice_diplay_yn)
    return render_template('board/b_notice_modact.html', cnt=cnt)

@app.route("/download_img")
def download_render_img():
    path = request.args.get('path')
    file = request.args.get('file')
    return send_file(path +'/'+ file)

@app.route("/b_free_mod")
def b_free_mod_render():
    bfree_seq = request.args.get("bfree_seq")
    flag_ses, user_id = getSession()
    if not flag_ses :
        return redirect("login")
    free = MyDaoBfree().bfree_select(bfree_seq)
    return render_template('board/b_free_mod.html', free=free)

@app.route("/b_free_modact", methods=['POST', 'Get'])
def b_free_modact_render():
    bfree_seq = request.form["bfree_seq"]
    bfree_title = request.form["title"]
    bfree_content = request.form["content"]
    file = request.files['file']
    attach_file_temp = secure_filename(file.filename)
    attach_path_temp = str(datetime.today().strftime("%Y%m%d%H%M%S")) + "_" + attach_file_temp # 앞 뒤에 있을 떄 차이?
    file.save(os.path.join(DIR_UPLOAD, attach_path_temp))
    bfree_filepath= "null"
    bfree_filename= "null"
    print("path",request.form["filepath"])
    print("name",request.form["filename"])
    if file:
        bfree_filename = attach_path_temp
        bfree_filepath = attach_file_temp
        print("file 0")
    else :
        bfree_filename= request.form["filename"]
        bfree_filepath= request.form["filepath"]
        print("FILE X")
        
    if bfree_filename == 'None' :
        bfree_filepath= ""
        bfree_filename= ""
    flag_ses,mem_carnum=getSession()
    up_user_id = str(session["mem_carnum"])
    if not flag_ses :
        return redirect("login")
    print("path",bfree_filepath)
    print("name",bfree_filename)
    cnt = MyDaoBfree().bfree_update(bfree_seq, bfree_title, bfree_content, bfree_filename, bfree_filepath, up_user_id, mem_carnum)
    return render_template('board/b_free_modact.html', cnt=cnt, bfree_seq=bfree_seq)

#건의 사항 수정 리스트 가져오기
@app.route("/b_sug_mod")
def b_sug_mod_render():
    bsug_seq = request.args.get('bsug_seq')
    print(bsug_seq)
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")    

    obj = MyDaoBsug().bsug_select(bsug_seq)
    return render_template('board/b_sug_mod.html', sug=obj,enumerate=enumerate)

#건의사항수정
@app.route("/b_sug_modact", methods=['POST'])
def b_sug_modact_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")

    bsug_seq           = request.form["bsug_seq"]
    bsug_title         = request.form["bsug_title"]
    bsug_content       = request.form["bsug_content"]
    attach_file_old    = request.form["bsug_filename"]
    attach_path_old    = request.form["bsug_filepath"]
    
    if attach_file_old == 'None' :
        attach_file_old = ""
        attach_path_old = ""
    
    file = request.files['file']        
    attach_file_temp = secure_filename(file.filename)
    attach_path_temp = str(datetime.today().strftime("%Y%m%d%H%M%S")) +"_"+ attach_file_temp  
    file.save(os.path.join(DIR_UPLOAD, attach_path_temp))
    
    bsug_filename = ""
    bsug_filepath = ""
    if file :
        print("__attach_path_temp",attach_path_temp)
        print("__attach_file_temp",attach_file_temp)
        bsug_filename = attach_file_temp
        bsug_filepath = attach_path_temp 
        print("file O")
    else:
        bsug_filename = attach_file_old
        bsug_filepath = attach_path_old 
        print("file X")
    
    cnt = MyDaoBsug().bsug_update(bsug_seq, bsug_title, bsug_content, bsug_filename, bsug_filepath)
    
    return render_template('board/b_sug_modact.html', cnt=cnt, bsug_seq=bsug_seq, enumerate=enumerate)


# 게시물 삭제 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/b_notice_delact")
def b_notice_delact_render():
    b_notice_seq        = request.args.get('b_notice_seq')
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses :
        return redirect("login")
    cnt = MyDaoBnotice().bnotice_delete(b_notice_seq)

    return render_template('board/b_notice_delact.html', cnt=cnt)

@app.route("/b_free_del")
def b_free_del_render():
    bfree_seq = request.args.get("bfree_seq")
    flag_ses,mem_carnum=getSession()
    if not flag_ses :
        return redirect("login")
    cnt = MyDaoBfree().bfree_delete(bfree_seq, mem_carnum)
    return render_template('board/b_free_del.html',cnt=cnt)

@app.route("/b_free_del.ajax", methods=['POST', 'Get'])
def b_free_del_ajax():
    bfree_seq = request.form["bfree_seq"]
    flag_ses,mem_carnum=getSession()
    if not flag_ses :
        return redirect("login")
    print(bfree_seq,mem_carnum)
    cnt = MyDaoBfree().bfree_delete_file(bfree_seq, mem_carnum)
    msg = ""
    if cnt == 1 :
        msg = "ok"
    else :
        msg = "ng"
    print(cnt)
    return jsonify(msg=msg)

#건의 사항
@app.route("/b_sug_delact")
def b_sug_delact_render():
    bsug_seq = request.args.get('bsug_seq')

    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")    
    cnt = MyDaoBsug().bsug_delete(bsug_seq)
    redel = MyDao_Bsug_Sreply().bsug_delete_all(bsug_seq)
    print(redel)
    return render_template('board/b_sug_delact.html',bsug_seq=bsug_seq, cnt=cnt,enumerate=enumerate)
# 게시물 삭제 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/download")
def download_render():
    attach_path = request.args.get('filename')
    attach_file = request.args.get('filepath')
    filename = DIR_UPLOAD+'/'+attach_path
    return send_file(filename,
                mimetype='image/png',
                attachment_filename=attach_file,
                as_attachment=True)

# 견인차량 게시판 관련 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/b_tow")
def b_tow_render():
    return render_template('board/b_tow.html')

@app.route('/search_tow.ajax', methods=['POST'])
def search_tow_ajax():
    carnum = request.form["carnum"]
    
    list = MyDaoTow().tow_select(carnum)
    
    print(list)
    
    msg = ""
    if len(list) >= 1 :
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg, list=list)

# INTROㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/intro")
def intro_render():
    return render_template('intro.html')

@app.route("/intro_road")
def intro_road_render():
    return render_template('intro_road.html')

# 예약 및 예약취소 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/u_book")
def u_book_render():
    flag_ses, mem_carnum = getSession()
    
    list = MyDaoMembers().members_select(mem_carnum)
    mem_ticket_yn = list[0]['mem_ticket_yn']
    return render_template('u_book.html', mem_ticket_yn = mem_ticket_yn)

@app.route("/u_book.ajax", methods=['POST'])
def u_book_render_ajax():
    book_date = request.form["book_date"]
    print(book_date)
    list = MyDaoBook().book_select_list_book(book_date)
    lists = MyDaoParkinfo().parkinfo_select_uselist()
    print(1,list)
    print(2,lists)
    
    
    return jsonify(list=list, lists=lists)

@app.route("/k_buy_api_book")
def k_buy_api_book_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 
    
    date      = request.args.get("date")
    parkinfo_seq    = request.args.get("parkinfo_seq")
    prod_code = "20001"
    obj = MyDaoProd().prod_select(prod_code)
    prod_price = str(obj['prod_price'])
    prod_name = obj['prod_name']
    return render_template('k_pay/k_buy_api_book.html', prod_code=prod_code, date=date, prod_price=prod_price, prod_name=prod_name, mem_carnum=mem_carnum, parkinfo_seq=parkinfo_seq)

@app.route("/k_buy_api_book_nu")
def k_buy_api_book_nu_render():
    book_date      = request.args.get("date")
    parkinfo_seq    = request.args.get("parkinfo_seq")
    mem_carnum    = request.args.get("mem_carnum")
    mem_name    = request.args.get("mem_name")
    mem_tel    = request.args.get("mem_tel")
    mem_email    = request.args.get("mem_email")
    rnd    = request.args.get("tid")
    prod_code = "20001"
    mem_tel = mem_tel.replace('-','')
    
    print(parkinfo_seq)
    print(rnd)
    obj = MyDaoProd().prod_select(prod_code)
    
    prod_price = str(obj['prod_price'])
    prod_name = obj['prod_name']
    return render_template('k_pay/k_buy_api_book_nu.html',rnd=rnd, mem_name=mem_name, mem_tel=mem_tel, mem_email=mem_email, prod_code=prod_code, book_date=book_date, prod_price=prod_price, prod_name=prod_name, mem_carnum=mem_carnum,parkinfo_seq=parkinfo_seq)

@app.route("/nu_email.ajax", methods=['POST'])
def nu_email_ajax():
    mem_name = request.form["mem_name"]
    rnd_result = request.form["rnd_result"]
    mem_email = request.form["mem_email"]
    print(mem_name, rnd_result, mem_email)
    
    content = mem_name+"님. "+rnd_result+" 인증번호를 홈페이지에 입력해주세요. \n\n"
    MyMail().mysendmail(mem_email, "비회원 예약인증 메일", content)
    msg = "ok"

    return jsonify(msg = msg)

@app.route("/nu_book")
def nu_book_render():
    return render_template('nu_book.html')

@app.route("/u_book_cel")
def u_book_cel_render():
    flag_ses, mem_carnum = getSession()
    list = MyDaoBook().book_select(mem_carnum)
    print(list)
    if not flag_ses:
        return redirect("login") 
    return render_template('u_book_cel.html',list=list,enumerate=enumerate)

@app.route("/u_book_cel.ajax", methods=['POST'])
def u_book_cel_ajax():
    book_seq = request.form["book_seq"]
    mem_carnum = request.form["mem_carnum"]
    cnt = MyDaoBook().book_update(mem_carnum, book_seq)
    msg = ""
    if cnt == 1 :
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route("/nu_book_cel.ajax", methods=['POST'])
def nu_book_cel_ajax():
    mem_carnum = request.form["mem_carnum"]
    book_rnd = request.form["book_rnd"]
    obj = MyDaoBook().book_select_list_book_nu(mem_carnum, book_rnd)
    cnt_len = len(obj)
    print(obj)
    print(cnt_len)
    book_cel_yn = obj[0]['book_cel_yn']
    print(book_cel_yn)
    msg = ""
    if cnt_len == 1 :
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg, obj=obj, book_cel_yn=book_cel_yn)

@app.route("/nu_book_cel")
def nu_book_cel_render():
    return render_template('nu_book_cel.html')

# 정기권관련 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/ticket")
def ticket_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 
    
    list = MyDaoTicket().ticket_select(mem_carnum)

    return render_template('ticket_refund.html', enumerate=enumerate, list=list)

@app.route("/ticket_buy")
def ticket_buy_render():
    date = datetime.today().strftime("%Y%m%d")
    print(date)
    MyDaoTicket().ticket_refund_update_render1(date)
    MyDaoTicket().ticket_refund_update_render2()
    MyDaoTicket().ticket_refund_update_render3(date)
    list = MyDaoParkinfo().parkinfo_select_list()
    print(list)
    return render_template('ticket_buy.html',list=list)

@app.route("/k_buy_api_ticket")
def k_buy_api_ticket_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 
    
    prod_code      = request.args.get("prod_code")
    parkinfo_seq    = request.args.get("parkifo_seq")
    
    obj = MyDaoProd().prod_select(prod_code)
    prod_price = str(obj['prod_price'])
    prod_name = obj['prod_name']
    return render_template('k_pay/k_buy_api.html', prod_code=prod_code, prod_price=prod_price, prod_name=prod_name, mem_carnum=mem_carnum, parkinfo_seq=parkinfo_seq)

@app.route("/ticket_exam")
def ticket_buy_exam():
    bsug_seq = request.args.get('bsug_seq')

    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")    
    
    list = MyDaoProd().prod_select_pay()
    
    return render_template('ticket_buy(exam).html', list=list)

@app.route("/ticket_refund")
def ticket_refund_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 
    
    list = MyDaoTicket().ticket_select(mem_carnum)

    return render_template('ticket_refund.html', enumerate=enumerate, list=list)


# 관리자페이지 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
@app.route("/ad_book_now")
def ad_book_now_render():
    date = request.args.get('date', '')
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    
    list = MyDaoBook().book_select_list(date)
    return render_template('admin/ad_book_now.html', list=list)

@app.route("/ad_price_mod")
def ad_price_mod_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")  
    list = MyDaoProd().prod_select_list() 
    return render_template('admin/ad_price_mod.html', list=list)

@app.route("/ad_price_mod_ins", methods=['POST'])
def ad_price_mod_ins():
    ad_price_mod_insdcode = request.form["ad_price_mod_insdcode"]
    ad_price_mod_insname = request.form["ad_price_mod_insname"]
    ad_price_mod_insprice = request.form["ad_price_mod_insprice"]
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")  
    
    print(ad_price_mod_insdcode)
    cnt = MyDaoProd().prod_insert(ad_price_mod_insdcode, ad_price_mod_insname, ad_price_mod_insprice)
      
    return "<script>location.href='ad_price_mod'</script>"

@app.route("/ad_price_mod_upd.ajax", methods=['POST'])
def ad_price_mod_upd_ajax():
    prod_code = request.form["prod_code"]
    prod_price = request.form["prod_price"]
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")  
    cnt = MyDaoProd().prod_update(prod_code, prod_price)
    
    print(prod_code)
    print(prod_price)
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route('/ad_price_mod_del.ajax', methods=['POST'])
def ad_price_mod_del_ajax():
    prod_code = request.form["prod_code"]

    cnt = MyDaoProd().prod_delete(prod_code)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route("/ad_sales")
def ad_sales_render():
    year='%'
    list1 = MyDaoSales().sales_select_book_circle(year)
    list2 = MyDaoSales().sales_select_ticket_circle(year)
    
    val = list(list1[0].values())
    sum = val[2]
    for n,v in enumerate(list2) :
        temp = list(list2[n].values())
        sum += temp[1]
        
    return render_template('admin/ad_sales.html',sum=sum)

@app.route("/sales.ajax", methods=['POST'])
def sales_ajax():
    year = request.form["year"]
    
    if year == '전체' :
        year='%'
    else :
        year = year[2:]   
        
    list1 = MyDaoSales().sales_select_book(year)
    list2 = MyDaoSales().sales_select_ticket(year)
    
    val = list(list1[0].values())
    val2 = list(list2[0].values())
    book = []
    if len(list1) != 1 :
        book = list(list1[1].values())
        book.pop(0)
        for n,v in enumerate(book) :
            if str(v)=='None' :
                book[n] = 0;
    val.pop(0)
    val2.pop(0)
    
    for n,v in enumerate(val) :
        if str(v)=='None' :
            val[n] = 0;
            
    
    
    for n,v in enumerate(val2) :
        if str(v)=='None' :
            val2[n] = 0;
    
    tic = []
    for n,v in enumerate(val) :
        tic.append(v+val2[n])
    
    return jsonify(book=book,tic=tic)

@app.route("/sales_two.ajax", methods=['POST'])
def sales_two_ajax():
    year = request.form["year"]
    kind = request.form["kind"]
    print(year)
    if year == '전체' :
        year='%'
    else :
        year = year[2:]   
        
    print(year)

    list1 = MyDaoSales().sales_select_book_circle(year)
    list2 = MyDaoSales().sales_select_ticket_circle(year)
    print(list1)
    print(list2)
    val = list(list1[0].values())
    val2 = []
    if kind=='건수' :
        val.pop(2)
        for n,v in enumerate(list2) :
            temp = list(list2[n].values())
            temp.pop(1)
            val2 += temp
    else :
        val.pop(1)
        for n,v in enumerate(list2) :
            temp = list(list2[n].values())
            temp.pop(2)
            val2 += temp
    print(val)
    print(val2)
    return jsonify(val=val,val2=val2)

@app.route("/ad_user_mgr")
def ad_user_mgr_render():
    flag_ses, user_id = getSession()
    if not flag_ses:
        return redirect("login")    
    list = MyDaoMembers().members_select_list()
    return render_template('admin/ad_user_mgr.html', list=list)

@app.route("/ad_user_mgr_upd.ajax", methods=['POST'])
def ad_user_mgr_upd_ajax():
    mem_carnum = request.form["mem_carnum"]
    mem_name = request.form["mem_name"]
    mem_email = request.form["mem_email"]
    mem_tel = request.form["mem_tel"]
    mem_pw = request.form["mem_pw"]
    
    mem_ticket_yn = request.form["mem_ticket_yn"]
    mem_black_yn = request.form["mem_black_yn"]
    mem_yn = request.form["mem_yn"]
    
    cnt = MyDaoMembers().members_update_mgr(mem_name, mem_email, mem_tel, mem_pw, mem_ticket_yn, mem_black_yn, mem_yn, mem_carnum)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route("/ad_tow_mgr")
def ad_tow_mgr_render():
    date = request.args.get('date', '')
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    list = MyDaoTow().tow_select_list(date)
    return render_template('admin/ad_tow_mgr.html', list=list)

# 유저페이지 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/u_mypage")
def u_mypage_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")
    list = MyDaoMembers().members_select(mem_carnum)
    return render_template('mypage/u_mypage.html', list=list ,mem_carnum = mem_carnum)


@app.route("/u_info_mod")
def u_info_mod_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")    
    list = MyDaoMembers().members_select(mem_carnum)
    print()
    return render_template('mypage/u_info_mod.html', list=list)

@app.route('/u_info_mod_upd.ajax', methods=['POST'])
def u_info_mod_upd_ajxa():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")    
    mem_carnum = request.form["mem_carnum"]
    mem_name = request.form["mem_name"]
    mem_email = request.form["mem_email"]
    mem_tel = request.form["mem_tel"]
    mem_pw = request.form["mem_pw"]
  
    cnt = MyDaoMembers().members_myp_update(mem_carnum, mem_name, mem_email, mem_tel, mem_pw)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
    else:
        msg = "ng"

    return jsonify(msg = msg)

@app.route('/u_info_mod_del')
def u_info_del():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")   

    cnt = MyDaoMembers().members_update(mem_carnum)
    
    msg = ""
    if cnt == 1:
        msg = "ok"
        session.clear()
    else:
        msg = "ng"

    return render_template('main.html')



@app.route("/u_history")
def u_history_render():
    date = request.args.get("date")
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 
    
    list = MyDaoTicket().ticket_select_date(mem_carnum, date)
    return render_template('mypage/u_history.html', list=list)

@app.route("/u_book_history")
def u_book_history_render():
    date = request.args.get("date")
    
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 
    
    list = MyDaoBook().book_select_history(mem_carnum, date)
    return render_template('mypage/u_book_history.html', list=list)


@app.route("/u_find_id")
def u_find_id_render():
    return render_template('mypage/u_find_id.html')

# kakako pay ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
@app.route("/k_buy_api", methods=['POST' , 'GET'])
def k_buy_api_mypage_render():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login") 

    prod_code      = request.form["prod_code"]
    prod_price     = request.form["prod_price"]
    prod_name      = request.form["prod_name"]
    
    return render_template('k_pay/k_buy_api.html', prod_code=prod_code, prod_price=prod_price, prod_name=prod_name, mem_carnum=mem_carnum)

@app.route("/k_buy_cancel")
def k_buy_cancel_render():
    ticket_seq = request.args.get("ticket_seq")
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login.html") 
    
    list = MyDaoTicket().ticket_refund_select(ticket_seq)
    return render_template('k_pay/k_buy_cancel.html', list=list)

@app.route("/paymethod.ajax", methods=['POST'])
def paymethod():
    partner_order_id = request.form["partner_order_id"]
    partner_user_id = request.form["partner_user_id"]
    item_name = request.form["item_name"]
    total_amount = request.form["total_amount"]
    parkinfo_seq = request.form["parkinfo_seq"]
    date = request.form["date"]

        
    print("페이먼트",parkinfo_seq)
    obj_pay = {    'partner_order_id':partner_order_id,
                'partner_user_id' : partner_user_id,
                'item_name' : item_name,
                'total_amount':int(total_amount),
                'parkinfo_seq':parkinfo_seq,
                'date':date,
                'tib':''
                }
    
    print(obj_pay)
    
    URL = 'https://kapi.kakao.com/v1/payment/ready'
    headers = {
        'Authorization': "KakaoAK " + "5f599b07861b536e87d144af54847380",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    params = {
        "cid": "TC0ONETIME", 
        "partner_order_id": partner_order_id,  
        "partner_user_id": partner_user_id,  
        "item_name": item_name, 
        "quantity": 1,              
        "total_amount": total_amount,
        "tax_free_amount": 0,  
        "vat_amount" : 200,
        "approval_url": "http://192.168.41.42:5005/success",
        "cancel_url": "http://192.168.41.42:5005/cancel",
        "fail_url": "http://192.168.41.42:5005/fail"

    }
    
    res = requests.post(URL, headers=headers, params=params)
    str_tid = res.json()['tid']  # 결제 승인시 사용할 tid를 세션에 저장
    print(res.json())
    obj_pay['tib'] = str_tid
    session['buy'] = obj_pay
    return jsonify({'next_url': res.json()['next_redirect_pc_url']})

@app.route("/paymethod_book_nu.ajax", methods=['POST'])
def paymethod_book_nu():
    partner_order_id = request.form["partner_order_id"]
    partner_user_id = request.form["partner_user_id"]
    item_name = request.form["item_name"]
    total_amount = request.form["total_amount"]
    parkinfo_seq = request.form["parkinfo_seq"]
    date = request.form["date"]
    mem_name    = request.form["mem_name"]
    mem_tel    = request.form["mem_tel"]
    mem_email    = request.form["mem_email"]
    rnd    = request.form["rnd"]
    print(date)
    obj_pay = {'partner_order_id':partner_order_id,
                    'partner_user_id' : partner_user_id,
                    'item_name' : item_name,
                    'total_amount':int(total_amount),
                    'parkinfo_seq':parkinfo_seq,
                    'date':date,
                    'mem_name':mem_name,
                    'mem_tel':mem_tel,
                    'mem_email':mem_email,
                    'rnd':rnd,
                    'tid':'',
                    }

    
    print(obj_pay)
    
    URL = 'https://kapi.kakao.com/v1/payment/ready'
    headers = {
        'Authorization': "KakaoAK " + "5f599b07861b536e87d144af54847380",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    params = {
        "cid": "TC0ONETIME", 
        "partner_order_id": partner_order_id,  
        "partner_user_id": partner_user_id,  
        "item_name": item_name, 
        "quantity": 1,              
        "total_amount": total_amount,
        "tax_free_amount": 0,  
        "vat_amount" : 200,
        "approval_url": "http://192.168.41.42:5005/success_book_nu",
        "cancel_url": "http://192.168.41.42:5005/k_buy_cancel_nu",
        "fail_url": "http://192.168.41.42:5005/k_payfail"

    }
    
    res = requests.post(URL, headers=headers, params=params)
    str_tid = res.json()['tid']  # 결제 승인시 사용할 tid를 세션에 저장
    print( res.json())
    
    obj_pay['tib'] = str_tid
    session['buy'] = obj_pay
    print(obj_pay)
    print("1초")
    session['buy'] = obj_pay
    return jsonify({'next_url': res.json()['next_redirect_pc_url']})
    

# AJAX ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ카카오 ajax ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
@app.route("/success", methods=['POST', 'GET'])
def sucess():
    obj_pay = session['buy']
    
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "5f599b07861b536e87d144af54847380",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",  # 테스트용 코드
        "tid":obj_pay['tib'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id":obj_pay['partner_order_id'],  # 주문번호
        "partner_user_id": obj_pay['partner_user_id'],  # 유저 아이디
        "pg_token": request.args.get("pg_token"),  # 쿼리 스트링으로 받은 pg토큰
    }

    
    res = requests.post(URL, headers=headers, params=params).json()
    context = {
        'res': res,
        'amount':obj_pay['total_amount'], 
    }
    mem_carnum = str(obj_pay['partner_user_id'])
    prod_code = str(obj_pay['partner_order_id'])
    parkinfo_seq = str(obj_pay['parkinfo_seq'])
    tid = str(obj_pay['tib'])
    date = str(obj_pay['date'])
    book_rnd = 'x'

    adddate = 0;
    if prod_code == '10001':
        adddate = 30
    elif prod_code == '10002':
        adddate = 90
    elif prod_code == '10003':
        adddate = 365
    else:
        adddate = 1
    
    if prod_code == '20001':
        cnt = MyDaoBook().book_insert(date, 'n', mem_carnum, parkinfo_seq, prod_code, book_rnd, tid)
        cnt2 = MyDaoParkinfo().parkinfo_update('n', 'n', 'n',parkinfo_seq)
    else:
        cnt = MyDaoTicket().ticket_insert(adddate, mem_carnum, prod_code, tid, parkinfo_seq)
        cnt2 = MyDaoParkinfo().parkinfo_update('y', 'n', 'y',parkinfo_seq)
        memyn = MyDaoMembers().members_update_buy_yn(mem_carnum)
        print(memyn)
    print(cnt)
    print(cnt2,"cnt2")
    
    return render_template('k_pay/success.html', context=context, res=res)

@app.route("/success_book_nu", methods=['POST', 'GET'])
def sucess_book_nu():
    obj_pay = session['buy']
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "5f599b07861b536e87d144af54847380",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",  # 테스트용 코드
        "tid":obj_pay['tib'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id":obj_pay['partner_order_id'],  # 주문번호
        "partner_user_id":obj_pay['partner_user_id'],  # 유저 아이디
        "pg_token": request.args.get("pg_token"),  # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params).json()
    context = {
        'res': res,
        'amount':obj_pay['total_amount'], 
    }
    mem_carnum = str(obj_pay['partner_user_id'])
    prod_code = str(obj_pay['partner_order_id'])
    parkinfo_seq = str(obj_pay['parkinfo_seq'])
    date = str(obj_pay['date'])
    mem_name = str(obj_pay['mem_name'])
    mem_email = str(obj_pay['mem_email'])
    mem_tel = str(obj_pay['mem_tel'])
    rnd = str(obj_pay['rnd'])
    tid = str(obj_pay['tib'])

    print('rnd',rnd)

    
    list_mem = MyDaoMembers().members_select(mem_carnum)
    cnt_mems = len(list_mem)
    print(cnt_mems,"cnt_memsv")
    if cnt_mems == 0 :
        cnt_x = MyDaoMembers().members_insert(mem_carnum, mem_name, mem_email, mem_tel, "", "n")
        print(cnt_x,"cnt_x")

    cnt_book = MyDaoBook().book_insert(date, "n", mem_carnum, parkinfo_seq, prod_code, rnd, tid)
    print("결제여기다")
    print(cnt_book,"cnt_book")
        
    
    return render_template('k_pay/success.html', context=context, res=res)


@app.route('/cancel', methods = ['POST']) 
def cancel():
    flag_ses, mem_carnum = getSession()
    if not flag_ses:
        return redirect("login")  
     
    print("cancel!!!!")
    tid = request.form["tid"]
    prod_price = request.form["prod_price"]
    parkinfo_seq = request.form["parkinfo_seq"]
    print(prod_price)
    
    URL = 'https://kapi.kakao.com/v1/payment/cancel'
    print(URL)
    headers = {
        "Authorization": "KakaoAK " + "5f599b07861b536e87d144af54847380", 
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    print(headers)
    params = {
        "cid": "TC0ONETIME",
        "tid" : tid,
        "cancel_amount":prod_price,
        "cancel_tax_free_amount":'0'
        }
    res = requests.post(URL, headers=headers, params=params).json()
    
    context = {
        'res': res,
    }
   
    tyn = MyDaoTicket().ticket_select(mem_carnum)
    for i in tyn:
        if 'n' == i['refund_yn']:
            cnt = MyDaoTicket().ticket_refund_update(tid)
        else :
            cnt = MyDaoTicket().ticket_refund_update(tid)
            parkcan = MyDaoParkinfo().parkinfo_update_refund(parkinfo_seq)
            memyn = MyDaoMembers().members_update_yn(mem_carnum)
        
    print(cnt)
    print(parkcan)
    msg = ""
    
    if cnt == 1 :
        msg = "ok"
    else :
        msg = "ng"
    print(cnt)
    return jsonify(msg=msg)


@app.route('/k_buy_cancel_nu.ajax', methods = ['POST']) 
def k_buy_cancel_nu():
    book_seq = request.form["book_seq"]
    mem_carnum = request.form["mem_carnum"]
    parkinfo_seq = request.form["parkinfo_seq"]
    tid = request.form["tid"]
    prod_price = request.form["prod_price"]
    
    URL = 'https://kapi.kakao.com/v1/payment/cancel'
    headers = {
        "Authorization": "KakaoAK " + "5f599b07861b536e87d144af54847380", 
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",
        "tid" : tid,
        "cancel_amount":prod_price,
        "cancel_tax_free_amount":'0'
        }
    res = requests.post(URL, headers=headers, params=params).json()
    
    context = {
        'res': res,
    }
    print("DB")
    cnt = MyDaoBook().book_update(mem_carnum, book_seq)
    parkcan = MyDaoParkinfo().parkinfo_update_refund(parkinfo_seq)
    print(cnt)
    print(parkcan)
    msg = ""
    
    if cnt == 1 :
        msg = "ok"
    else :
        msg = "ng"
    print(cnt)
    return jsonify(msg=msg)



#  ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

#  ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 로그인 ajax ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route("/login.ajax", methods=['POST'])
def login_ajax():
    mem_carnum = request.form["mem_carnum"]
    mem_pw = request.form["mem_pw"]
    user_check = request.form["user_check"]
    
    flag_ses = getSession()
    if not flag_ses:
        return redirect("login")    
    
    list = MyDaoMembers().members_login(mem_carnum, mem_pw)
    msg = ""
    
    if len(list) == 1:
        if list[0]['mem_exit_yn'] == 'y' or list[0]['mem_exit_yn'] == 'Y' :
            msg = "exit"
            return jsonify(msg = msg, mem_carnum = mem_carnum)
    
        session["mem_carnum"] = list[0]['mem_carnum']
        session["mem_pw"] = list[0]['mem_pw']
        session["user_check"] = user_check
        msg = "ok"
    else:
        msg = "ng"
    
    return jsonify(msg = msg, mem_carnum = mem_carnum)

@app.route("/admin_login.ajax", methods=['POST'])
def admin_login_ajax():
    mem_carnum = request.form["mem_carnum"]
    mem_pw = request.form["mem_pw"]
    user_check = request.form["user_check"]
    
    flag_ses = getSession()
    if not flag_ses:
        return redirect("login")    
    
    list_admin = MyDaoAdmins().admin_select(mem_carnum, mem_pw)
    
    msg = ""
    if len(list_admin) == 1:
        session["mem_carnum"] = list_admin[0]['admin_id']
        session["mem_pw"] = list_admin[0]['admin_pw']
        session["user_check"] = user_check
        msg = "ok"
    else:
        msg = "ng"
    
    return jsonify(msg = msg, mem_carnum = mem_carnum)
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 관리자 ajax ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route('/addtow.ajax', methods=['POST'])
def addtow_ajax():
    carnum = request.form["carnum"]
    tow_reason = request.form["tow_reason"]
    tow_date = request.form["tow_date"]
    
    msg = ""
    try:
        cnt = MyDaoAdmins().admin_insert_tow(carnum, tow_reason, tow_date)
    except:
        msg = "-1"
        return jsonify(msg = msg)
    
    if cnt == 1:
        msg = "1"
        memInfo = MyDaoMembers().members_select(carnum)[0]
        email = memInfo["mem_email"]
        content = memInfo["mem_name"]+" 님의 '" +memInfo["mem_carnum"]+"' 차량이 견인되었습니다.\n"
        content += "자세한 내용은 홈페이지에서 확인 부탁드립니다.\n\n"
        content += "홈페이지 주소 : http://192.168.41.42:5005/b_tow"
        MyMail().mysendmail(email, "PPAP - 차량견인 알림", content)
    else:
        msg = "0"
        
    return jsonify(msg = msg)

@app.route('/img')
def img():
    file = request.args.get('file')
    return send_file(file)

@app.route('/ad_upbook.ajax', methods=['POST'])
def ad_upbook_ajax():
    book_seq = request.form["book_seq"]
    carnum = request.form["carnum"]
    book_date = request.form["book_date"]
    
    msg = ""
    cnt = MyDaoAdmins().admin_upBook(book_seq, carnum, book_date)
    
    if cnt == 1 :
        msg = "ok"
    else:
        msg = "ng"
        
    return jsonify(msg = msg)

@app.route('/ad_book_cel.ajax', methods=['POST'])
def ad_book_cel_ajax():
    book_seq = request.form["book_seq"]
    
    msg = ""
    
    cnt = MyDaoAdmins().admin_book_cel(book_seq)
     
    if cnt == 1 :
        msg = "ok"
    else:
        msg = "ng"
        
    return jsonify(msg = msg)

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 키오스크 관련 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
@app.route("/kiosk")
def kiosk_main_render():
    return render_template('kiosk/kiosk_main.html')

@app.route("/kiosk_members")
def kiosk_members_render():
    return render_template('kiosk/kiosk_members.html')


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
