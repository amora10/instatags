from collections import Counter
import json
import urllib2
import sys

# Login Credentials
access_token = "1014426274.1677ed0.a695406addfa4f2c8de879708912e5a0"
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

# Function to return images and there tags
def getMedia(tag):
   url = 'https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s' % (tag, access_token)
   media = json.load(urllib2.urlopen(url))["data"]
   
   images = dict()
   for i in media:
      if i["link"] not in images:
         images[i["link"]] = Image(i)
   return images

def combineTags(images):
   counter = Counter()
   for i in images:
      for t in images[i].tags:
         counter[t] += 1
   print counter.most_common(3)
   return counter


def fullExpand(tag):
   pass

def mostFrequent(tag, images):
   pass

def tagIncluded(tag):
   pass

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
      images = getMedia(query)
      printImages(images, 3)
      counts = combineTags(images)
   else:
      sys.exit()


if __name__ == '__main__':
   main(sys.argv[1:])