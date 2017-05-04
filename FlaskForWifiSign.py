from flask import Flask,flash,render_template,request
from MongodbConn import MongoPipeline

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
    ids = conn.getIds('info', {'name': name, 'date': date})
    _id = next(ids, None)
    sign_info = []
    while _id:
        # print(_id)
        sign_info.append(_id)
        _id = next(ids, None)
    print(sign_info)
    return render_template('query.html',sign_info = sign_info)

@app.route('/rigister',methods={'POST'})
def rigister():
    form = request.form
    name = form.get('name')
    mac  = form.get('mac')
    student_id = form.get('student_id')
    class_number = form.get('class_number')
    conn = MongoPipeline()
    conn.open_connection('qiandao_mac_name')
    student_info = {}
    student_info['name'] = name
    student_info['mac']  = mac
    student_info['studentid'] = student_id
    student_info['class_num'] = class_number
    student_info['_id'] = mac
    conn.process_item(student_info,'info')
    flash('注册成功！')
    return render_template('register.html')

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
