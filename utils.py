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

# Function to return images and there tags
def getMedia(tag):
   url = 'https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s' % (tag, access_token)
   media = json.load(urllib2.urlopen(url))["data"]
   
   images = dict()
   for i in media:
      if i["link"] not in images:
         images[i["link"]] = Image(i)
   return images

def getPhotoUrl(url):
   html = urllib2.urlopen(url).read()
   parts = html.partition("<meta property=\"og:image\" content=\"")[2].partition(".jpg")
   image_url = parts[0] + parts[1]
   return image_url

def getUrls(images):
   return [getPhotoUrl(images[i].url) for i in images]

def printImages(images, count):
   c = 0
   for i in images:
      if c == count:
         break
      print images[i].toString()
      c += 1

# Take random tags and requery
def fullExpand(tag, steps):
   masterset = dict()
   imagesets = [dict()] * (steps+1)

   masterset = getMedia(tag)
   imagesets[0] = copy.deepcopy(masterset)

   for i in range(0, steps):
      thislayer = dict()
      counter = dict(combineTags(imagesets[i-1]))

      for i in range(0, 20):
         tag = random.choice(counter.keys())
         newimages = getMedia(tag)

         for key in newimages:       
            if key not in masterset:
               masterset[key] = newimages[key]
               thislayer[key] = newimages[key]

      imagesets[i] = thislayer
   return imagesets

def main(args):
   if len(args) < 1:
      sys.exit()
   if args[0] == "media":
      printImages(getMedia(args[1]), 20)
   if args[0] == "url":
      print getUrls(getMedia(args[1]))

if __name__ == '__main__':
   main(sys.argv[1:])