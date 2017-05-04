from flask import Flask,flash,render_template,request
from MongodbConn import MongoPipeline
from TheStudent import student

app = Flask(__name__)
app.secret_key = "You can't guess it!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query',methods={'POST'})
def query():
    form = request.form
    name = form.get('name')
    date = form.get('date')
    conn = MongoPipeline()
    conn.open_connection('qiandao_last_info')
    student_sign_infos = conn.getIds('info', {'name': name, 'date': date})
    student_sign_info = next(student_sign_infos, None)
    #储存给前端页面的签到信息
    sign_info = []
    if student_sign_info == None:
        flash('对不起，没有该学生签到信息，请确认后，重新输入！')
        return render_template('query.html')
    else :
        while student_sign_info:
            # print(_id)
            sign_info.append(student_sign_info)
            student_sign_info = next(student_sign_infos, None)
        print(sign_info)
        return render_template('query.html',sign_info = sign_info)

#注册新同学
@app.route('/rigister',methods={'POST'})
def rigister():
    form = request.form
    name = form.get('name')
    mac  = form.get('mac')
    student_id = form.get('student_id')
    class_number = form.get('class_number')
    register_student = student(name,mac,student_id,class_number)
    judge_mac = register_student.query_database('mac',mac)
    judge_name = register_student.query_database('name',name)
    if judge_mac == True:
        flash('mac地址与数据库中信息冲突，请确认后，重新输入！')
        return render_template('register.html')
    elif judge_name == True:
        flash('姓名与数据库中信息冲突，请确认后，重新输入！')
        return render_template('register.html')
    else:
        register_student.save()
        flash('注册成功！')
        return render_template('register.html')
#修改mac地址
@app.route('/modify_information',methods={'POST'})
def modify_information():
    form = request.form
    name = form.get('name')
    mac  = form.get('mac')
    conn = MongoPipeline()
    conn.open_connection('qiandao_mac_name')
    judge_insert_update = conn.getIds('info',{'name':name})
    result_insert_update = next(judge_insert_update,None)
    if result_insert_update == None:
        flash('无此学生！请确认后，重新输入！')
    else:
        _id = result_insert_update['_id']
        conn.update_item({'_id':_id},{"$set":{'mac':mac}},'info')
        flash('修改成功！')
    return render_template('modify_information.html')


@app.route('/query_info')
def query_info():
    return render_template('query.html')

@app.route('/register_info')
def register_info():
    return render_template('register.html')

@app.route('/modify_information_info')
def modify_information_info():
    return render_template('modify_information.html')

if __name__ == '__main__':
    app.run(debug=True)
