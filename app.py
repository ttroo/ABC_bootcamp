# from urllib import request

from flask import Flask, render_template, request, redirect
import os
import dbconn as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/test/<username>')
def test(username):
    print(username)
    return render_template('test_result.html', name=username)

@app.route('/methodin')
def methodin():
    return render_template('inputform.html')

@app.route('/methodout', methods=['GET', 'POST']) # 기본 값은, methods=['GET']
def methodout():
    if request.method == 'POST':
        print('POST')
        data = request.form
    else:
        print('GET')
        data = request.args
    return render_template('method.html', data1 = data, data2 = request.method)

@app.route('/fileupload', methods=['GET', 'POST'])
def fileupload():
    if request.method == 'GET':
        return render_template('fileinput.html')
    else:
        f = request.files['formFile'] # key 값이기때문에 대괄호를 사용해야 함 ! 
        path = os.path.dirname(__file__) + '/upload/' + f.filename
        print(path)
        f.save(path)
        print('저장성공 >_<')
        return redirect('/')

@app.route('/bloglist', methods=['GET'])
def bloglist():
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = '''select * from blog'''
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    return render_template('bloglist.html', data = rows)


if __name__ == '__main__':
    app.run(debug=True, port=80)

# 수정했으면 Run 해야 함!