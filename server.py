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
      global tag, imageSets, image_queue, totLayer
      tag = request.form['tag']
      totLayer = int(request.form['layer'])
      func = request.form["func"]
      if func == 'Random Expand':
         imageSets = utils.fullExpand(tag, totLayer)
      elif func == 'Most Frequent':
         imageSets = utils.mostFrequent(tag, totLayer)
      else:
         imageSets = utils.tagIncluded(tag, totLayer)
      image_queue = imageSets[currLayer]
   return redirect("/pics")

@app.route('/pics')
def pics():
   global image_queue
   if len(image_queue) == 0:
      return redirect("/results")
   pic = image_queue.pop()
   return render_template('rate_pics.html', tag=tag, pic=pic, 
      layer=currLayer, left=len(image_queue))

@app.route('/rate', methods=['GET', 'POST'])
def rate():
   global zero_pics, one_pics, two_pics
   if request.method == 'POST':
      value = request.form["rate"]
      if value == '0':
         zero_pics += 1
      elif value == '1':
         one_pics += 1
      else:
         two_pics += 1
   return redirect("/pics")

@app.route('/results')
def results():
   return render_template('results.html', zero=zero_pics, one=one_pics, 
      two=two_pics, layer=currLayer)

@app.route('/finished')
def finished():
   global zero_pics, one_pics, two_pics, currLayer, image_queue
   zero_pics = 0
   one_pics = 0
   two_pics = 0
   currLayer += 1
   if currLayer == totLayer:
      return render_template('finished.html')
   else:
      image_queue = imageSets[currLayer]
      return redirect('/pics')



if __name__ == '__main__':
   app.run(debug=True)