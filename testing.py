from collections import Counter
import json
import urllib2
import sys
import time
import copy
import random

# Login Credentials
#access_token = "1014426274.1677ed0.a695406addfa4f2c8de879708912e5a0"
access_token = "46903393.1677ed0.7519ea246e954c449952735286efa639"
client_id = "4f4b027e014540948cf8b6acbc88c2bb"
client_secret = "13e9e272df824a7895db6b9747f2ef31"

# Image class to store image urls and tags
class Image:
   def __init__(self, media):
      self.url = media["link"]
      self.tags = [i.encode('utf-8') for i in media["tags"]]

   def toString(self):
      print "Link: " + self.url
      print "Tags:",
      for t in self.tags:
         print t,

# Function to return tag counts 
def get(tag):
   url = 'https://api.instagram.com/v1/tags/search?q=%s&access_token=%s' % (tag, access_token)
   return json.load(urllib2.urlopen(url))

# Function to return images and their tags
def getMedia(tag):
   url = 'https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s' % (tag, access_token)
   media = json.load(urllib2.urlopen(url))["data"]
   
   images = dict()
   for i in media:
      if i["link"] not in images:
         images[i["link"]] = Image(i)
   return images

# Find most common tags
def combineTags(images):
   counter = Counter()
   for i in images:
      for t in images[i].tags:
         counter[t] += 1
   print counter.most_common(3)
   return counter

# Take random tags and requery
def fullExpand(tag, steps):
   masterset = dict()
   imagesets = [dict()] * (steps+1)

   layer = 0
   masterset = getMedia(tag)
   imagesets[0] = copy.deepcopy(masterset)

   while layer < steps:
      layer += 1
      thislayer = dict()

      # Extract tags from previous layer
      counter = combineTags(imagesets[layer-1])
      counter = dict(counter)

      # Search for new images with subset of those tags
      i=0
      while i < 20:
         i+=1
         print i
         tag = random.choice(counter.keys())
         newimages = getMedia(tag)

         # Add new images to current layer, if not in masterset
         for key in newimages:       
            if key not in masterset:
               masterset[key] = newimages[key]
               thislayer[key] = newimages[key]

      imagesets[layer] = thislayer
   return imagesets


# Look at top percent most freqent tags
def mostFrequent(tag, steps):
   masterset = dict()
   imagesets = [dict()] * (steps+1)

   layer = 0
   masterset = getMedia(tag)
   imagesets[0] = copy.deepcopy(masterset)

   while layer < steps:
      layer += 1
      thislayer = dict()

      # Extract tags from previous layer
      counter = combineTags(imagesets[layer-1])
      tags = counter.most_common(20)

      # Search for new images with 20 most frequent tags
      i = 0
      for tag in tags:
         i += 1
         newimages = getMedia(tag[0])

         # Add new images to current layer, if not in masterset
         for key in newimages:       
            if key not in masterset:
               masterset[key] = newimages[key]
               thislayer[key] = newimages[key]

      imagesets[layer] = thislayer
   return imagesets


# Take tags that contain original tag
def tagIncluded(tag, steps):
   masterset = dict()
   imagesets = [dict()] * (steps+1)

   layer = 0
   masterset = getMedia(tag)
   imagesets[0] = copy.deepcopy(masterset)

   while layer < steps:
      layer += 1
      thislayer = dict()

      # Extract tags from previous layer
      counter = combineTags(imagesets[layer-1])
      counter = dict(counter)
      newtags = []
      for key in counter:
         if str(tag) in str(key):
            print key
            newtags.append(key)

      # Search for new images with subset of those tags
      i = 0
      for tag in newtags:
         i += 1
         print i
         if i>20:
            break
         newimages = getMedia(tag)

         # Add new images to current layer, if not in masterset
         for key in newimages:       
            if key not in masterset:
               masterset[key] = newimages[key]
               thislayer[key] = newimages[key]

      imagesets[layer] = thislayer
   return imagesets

def printImages(images, count):
   c = 0
   for i in images:
      if c == count:
         break
      print images[i].toString()
      c += 1

def main(argv):
   if len(argv) > 0:
      query = argv[0]
      #images = getMedia(query)
      #printImages(images, 3)
      #counts = combineTags(images)
      layers = 3
      imagesets = tagIncluded(query, layers)
      i = 0
      while i <= layers:
         print i
         printImages(imagesets[i], 3)
         print len(imagesets[i])
         i+=1
   else:
      sys.exit()


if __name__ == '__main__':
   main(sys.argv[1:])