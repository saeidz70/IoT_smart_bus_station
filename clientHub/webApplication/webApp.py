from flask import Flask, render_template, request
from dataProvider import DataProvider

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)