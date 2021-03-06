# -*- coding: utf-8 -*-

import re
import urllib.request, urllib.error, urllib.parse
import codecs
import csv

VIDEO_LIST = ['youtube.com', 'vine.co', 'vimeo.com', 'dailymotion.com', 'metacafe.com']
IMAGE_LIST = ['instagram.com', 'flikr.com', 'pinterest.com', 'deviantart.com', 'imgur.com']
SHOP_LIST = ['amazon.co', 'ebay.com', 'ebay.to', 'etsy.com', 'newegg.com', 'rakuten.com', 'bonanza.com']
SNS_LIST = ['twitter.com', 'facebook.com', 'tumblr.com', 'reddit.com']

# Some sites forbid crawlers, need to alter user agent string to get around
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Firefox/3.0.7',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

# Use to unwrap a shortened URL
class HeadRequest(urllib.request.Request):
    def get_method(self):
        return "HEAD"

# def getURLs(tweet):
#     urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet)
#     for url in urls:
#         print getURLType(url)
    
def getURLType(url):
    isShortened = False
    host = re.findall('http[s]?://(?:[^@:/]*@)?([^:/]+)', url.lower())
    if len(host) > 0:
        
        # Look at the host name and see if the URL needs unwrapping
        hostName = host[0]
        if "." in hostName[-3:]:
            isShortened = True
        elif "tinyurl.com" in hostName:
            isShortened = True
        
        # Unwrap if necessary
        targetUrl = ""
        if isShortened:
            try:
                res = urllib.request.urlopen(HeadRequest(url))
                targetUrl = res.geturl()
            except:
                try:
                    global headers
                    res = urllib.request.urlopen(HeadRequest(url, None, headers))
                    targetUrl = res.geturl()
                except:
                    targetUrl = url
        else:
            targetUrl = url
        
        def isMedia(url):
            if "/photo/" in url: return True
            for host in IMAGE_LIST:
                if host in url:
                    return True
            for host in VIDEO_LIST:
                if host in url:
                    return True
            return False
        
        def isShop(url):
            for host in SHOP_LIST:
                if host in url:
                    return True
            return False
        
        def isSNS(url):
            for host in SNS_LIST:
                if host in url:
                    return True
            return False
        
        def isArticle(url):
            if ("/news/" in url) or (".news/" in url): return True
            ret = re.findall('/20[0-1][0-9]/[0-1][0-9]/', url)
            if len(ret) > 0:
                return True
            else:
                ret = re.findall('\/(\w+(-|_)\w+(-|_)\w+)', url)
                return len(ret) > 0
                
        # Get URL type
        if isMedia(targetUrl):
            return 'MEDIA'
        elif isShop(targetUrl):
            return 'SHOP'
        elif isArticle(targetUrl):
            return 'ARTICLE'
        elif isSNS(targetUrl):
            return 'SNS'
        else:
            return 'OTHERS'
        
    else:
        # Invalid URL
        return 'OTHERS'
  
# # Test the algorithm
# with open('data.csv', 'rb') as f:
#     reader = csv.reader(f, delimiter=',')
#     for i, row in enumerate(reader):
#         getURLs(row[0])
#     print 'Done.'
    