

def getPhotoUrl(url):
   import urllib2
   html = urllib2.urlopen(url).read()
   parts = html.partition("<meta property=\"og:image\" content=\"")[2].partition(".jpg")
   image_url = parts[0] + parts[1]
   print image_url

def main():
   pass

if __name__ == '__main__':
   main()