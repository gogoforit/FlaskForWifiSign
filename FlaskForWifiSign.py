from flask import Flask,flash,render_template,request
from MongodbConn import MongoPipeline

app = Flask(__name__)


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

@app.route('/query_info')
def query_info():
    return render_template('query.html')

if __name__ == '__main__':
    app.run(debug=True)
