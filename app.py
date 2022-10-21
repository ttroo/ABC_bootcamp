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

### blog

@app.route('/bloglist', methods=['GET'])
def bloglist():
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = '''select * from blog'''
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    return render_template('bloglist.html', data = rows)

@app.route('/blogform', methods=['GET', 'POST'])
def blogform():
    if request.method == 'GET':
        return render_template('blogform.html')
    else: # 글을 DB에 저장
        f = request.files['formFile']
        path = os.path.dirname(__file__) + '/static/blog/img/' + f.filename
        print(path)
        f.save(path)
        print('저장성공 >_<')
        print(request.form)
        conn = db.dbconn()
        cursor = conn.cursor()
        sql = '''insert into blog values(?,?,?)'''
        data = [request.form['title'], request.form['content'], '/static/blog/img/' + f.filename]
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        return redirect('/bloglist')

@app.route('/blog/<int:id>')
def blogcontent(id):
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = '''select * from blog where id = ?'''
    cursor.execute(sql, id)
    rows = cursor.fetchone()
    conn.close()
    return render_template('blog_content.html', data = rows)

@app.route('/blogdelete/<int:id>')
def blogdelete(id):
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = '''delete blog where id = ?'''
    cursor.execute(sql, id)
    conn.commit()
    conn.close()
    return redirect('/bloglist')

### like

@app.route('/likelist', methods=['GET'])
def likelist():
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = '''select * from [like]'''
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    return render_template('likelist.html', data = rows)

@app.route('/likeform', methods=['GET', 'POST'])
def likeform():
    if request.method == 'GET':
        return render_template('likeform.html')
    else: # 글을 DB에 저장
        f = request.files['formFile']
        path = os.path.dirname(__file__) + '/static/like/img/' + f.filename
        print(path)
        f.save(path)
        print('저장성공 >_<')
        print(request.form)
        conn = db.dbconn()
        cursor = conn.cursor()
        sql = '''insert into [like] values(?,?,?,?)'''
        data = [request.form['title'], request.form['content'],  request.form['howlike'], '/static/like/img/' + f.filename]
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        return redirect('/likelist')

@app.route('/like/<int:id>')
def likecontent(id):
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = '''select * from [like] where id = ?'''
    cursor.execute(sql, id)
    rows = cursor.fetchone()
    conn.close()
    return render_template('like_content.html', data = rows)

@app.route('/likedelete/<int:id>')
def likedelete(id):
    conn = db.dbconn()
    cursor = conn.cursor()
    sql = '''delete [like] where id = ?'''
    cursor.execute(sql, id)
    conn.commit()
    conn.close()
    return redirect('/likelist')

###

if __name__ == '__main__':
    app.run(debug=True, port=80)

# 수정했으면 Run 해야 함!