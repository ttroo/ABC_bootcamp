# from urllib import request
from flask import Flask, render_template, request

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

if __name__ == '__main__':
    app.run(debug=True, port=80)

# 수정했으면 Run 해야 함!