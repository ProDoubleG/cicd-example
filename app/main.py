import os
import time
from flask import Flask, render_template

app = Flask(__name__)
core_response = "Success"
APP_VERSION = str(time.time())

@app.route('/')
def home():
    # Get index,html in app/templates
    # Read 'Page_Title' or  use 'CICD Practice' as default title
    page_title = os.getenv("Page_Title", "CICD Practice")
    return render_template('index.html', title=page_title)

@app.route('/version')
def get_version():
    return APP_VERSION

@app.route('/core')
def core_function():
    return core_response

@app.route('/legacy')
def legacy_feature():
    return "Response A"

# [Scenario] Uncomment one block at a time.
# Don't forget to uncomment the commented codelines in app/templates.index.html and tests/ci_tesst.py

############ [Scenario A] ############
# @app.route('/new-feature')
# def new_feature():
#     return "Fail", 500
######################################

############ [Scenario B] ############
# @app.route('/new-feature')
# def new_feature():
#     global core_response
#     core_response = "Fail"
#     return "Response B"
######################################

############ [Scenario C] ############
# @app.route('/new-feature')
# def new_feature():
#     return "Response B"
######################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)