import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # templates 폴더 내의 index.html을 보여줌
    # 환경변수 'Page_Title'을 읽어오고, 없으면 기본값 'CICD Practice' 사용
    page_title = os.getenv("Page_Title", "CICD Practice")
    return render_template('index.html', title=page_title)

@app.route('/core')
def core_function():
    return "Success"

@app.route('/legacy')
def legacy_feature():
    return "Response A"

if __name__ == '__main__':
    # 5000번 포트에서 실행, 외부 접속 허용(0.0.0.0)
    app.run(host='0.0.0.0', port=5000)