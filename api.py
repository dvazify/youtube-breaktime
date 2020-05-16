import json
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import isodate

def topic_format(topic):
    split = topic.split(" ")
    joined = "+".join(split)
    return joined

class YTVideo(object):
    def __init__(self, videoid):
        self.videoid = videoid
        self.api_key = "AIzaSyBGpdnxh6B7yUH_LNkXDIEC7-A-nlQfJ4M"
        self.title = None
        self.creator = None
        self.duration = None
        self.content_details = None
        self.snippet = None
        self.generatedata()
        self.get_duration()
        self.gettitle()
    def generatedata(self): 
        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+self.videoid+"&key="+self.api_key+"&part=contentDetails"
        response = urlopen(searchUrl).read()
        self.content_details = json.loads(response.decode("utf-8"))
        snippeturl = "https://www.googleapis.com/youtube/v3/videos?id="+self.videoid+"&key="+self.api_key+"&part=snippet"
        snipresponse = urlopen(snippeturl).read()
        self.snippet = json.loads(snipresponse.decode("utf-8"))
    def get_duration(self):
        duration = self.content_details['items'][0]['contentDetails']['duration']
        self.duration = isodate.parse_duration(duration)
    def gettitle(self):
        title = self.snippet['items'][0]['snippet']['title']
        self.title=title

def ReturnVideos(topic,maxmins):
    maxtime = maxmins*60
    
    url = "https://www.youtube.com/results?search_query="+topic_format(topic)
    
    rawsite = requests.get(url)
    soup = BeautifulSoup(rawsite.text, features="html.parser")
    
    all_urls = [link.get('href') for link in soup.find_all('a')]
    watch_urls = [url[9:] for url in all_urls if ("/watch?v=" in url and "&list" not in url)][::2]
    
    videolist = []
    
    for i in watch_urls:
        video = YTVideo(i)
        if video.duration.total_seconds() <= maxtime:
            videolist.append(video)
    
    return (videolist)
    

    
    
