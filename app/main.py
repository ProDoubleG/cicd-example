from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # templates 폴더 내의 index.html을 보여줌
    return render_template('index.html')

@app.route('/core')
def core_function():
    return "Success"

@app.route('/legacy')
def legacy_feature():
    return "Response A"

if __name__ == '__main__':
    # 5000번 포트에서 실행, 외부 접속 허용(0.0.0.0)
    app.run(host='0.0.0.0', port=5000)