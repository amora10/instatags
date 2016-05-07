from __future__ import print_function # In python 2.7
import os
import sys
import utils
from flask import Flask, request, render_template, redirect, url_for, send_from_directory

app = Flask(__name__)

tag = None
image_queue = None
imageSets = None
currLayer = 0
totLayer = 0
zero_pics = 0
one_pics = 0
two_pics = 0

@app.route('/')
def start_page():
   return render_template('start_page.html')

@app.route('/insertTag', methods=['POST'])
def insert():
   if request.method == 'POST':
      global tag, zero_pics, one_pics, two_pics
      tag = request.form['tag']
      totLayer = request.form['layer']
      tag = text
      zero_pics = 0
      one_pics = 0
      two_pics = 0
   return redirect("/pics")

@app.route('/pics')
def pics():
   global image_queue, imageSets
   if imageSets == None:
      imageSets = utils.fullExpand(tag, totLayer)
      image_queue = utils.getUrls(imageSets[currLayer])
   if image_queue == None:
      return redirect("/results")
   pic = image_queue.pop()
   print(pic, file=sys.stderr)
   return render_template('rate_pics.html', tag=tag, pic=pic)

@app.route('/rate', methods=['GET', 'POST'])
def rate():
   global zero_pics, one_pics, two_pics
   if request.method == 'POST':
      value = request.form["rate"]
      print(value, file=sys.stderr)
      if value == '0':
         zero_pics += 1
      elif value == '1':
         one_pics += 1
      else:
         two_pics += 1
   return redirect("/pics")

@app.route('/results')
def results():
   return render_template('results.html', zero=zero_pics, one=one_pics, two=two_pics)

@app.route('/finished')
def finished():
   global zero_pics, one_pics, two_pics, layer
   zero_pics = 0
   one_pics = 0
   two_pics = 0
   layer += 1
   if currLayer == totLayer:
      return render_template('finished.html')
   else:
      image_queue = imageSets[layer]
      return redirect('/pics')



if __name__ == '__main__':
   app.run()