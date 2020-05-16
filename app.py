import pafy
import requests
from bs4 import BeautifulSoup

def topic_format(topic):
    split = topic.split(" ")
    joined = "+".join(split)
    return joined

def ReturnVideos(topic, maxmins):
    maxtime = maxmins*60

    url = "https://www.youtube.com/results?search_query="+topic_format(topic)

    rawsite = requests.get(url)
    soup = BeautifulSoup(rawsite.text, features="html.parser")

    all_urls = [link.get('href') for link in soup.find_all('a')]
    watch_urls = ["http://www.youtube.com"+url for url in all_urls if ("/watch?v=" in url)][::2]

    recommendations = []

    for i in range(len(watch_urls)-1):
        video = pafy.new(watch_urls[i],basic=False)
        if video.length <= maxtime:
            recommendations.append(video.title+" | "+video.duration+" | "+watch_urls[i])

    return ("<br/>".join(recommendations))