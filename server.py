import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello_name(name=None, pic=None):
   return render_template('hello.html', name=name, pic="https://scontent-ord1-1.cdninstagram.com/t51.2885-15/e35/13150963_603120863177545_6030527_n.jpg")

@app.route('/rate', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      do_the_login()
   else:
      show_the_login_form()

if __name__ == '__main__':
   app.run()