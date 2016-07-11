from lxml import html
from bs4 import BeautifulSoup
from collections import defaultdict
import requests

class Crawler:
    def __init__(self, url):
        self.url = url

    def crawl(self):
        res = self.getRssUrl()
        return res

    def getRssUrl(self):
        # check if rss in url
        if '/rss' not in self.url:
            self.url = self.url + '/rss'

        # GET request from url
        page = requests.get(self.url)

        content = ''
        markup = ''

        # check request status
        if page.status_code == 200:
            # get content
            content = page.content
            # get markup
            markup = self.getMarkup( page.headers['content-type'] )
        elif page.status_code == 404:
            # no rss feed
            return

        # get feeds
        feeds = Feed(content, markup)
        data = feeds.getFeeds()

        return data

    def getMarkup(self, content_type):
        if 'xml' in content_type:
            markup = 'xml'
        elif 'html' in content_type:
            markup = 'html'

        return markup

class Feed:
    # Class to handle Feeds
    def __init__(self, data, markup):
        self.obj = BeautifulSoup(data, markup)

    def getFeeds(self):
        # instantiate
        feeds = {}

        # get title
        feeds['title'] = self.getTitle()
        # get link
        feeds['link'] = self.getLink()
        # get items
        feeds['items'] = self.setupItems()

        return feeds

    def getTitle(self):
        return self.obj.title.string

    def getLink(self):
        return self.obj.find('link').string

    def getItems(self):
        return self.obj.find_all('item')

    def setupItems(self):
        items = self.getItems()
        data = []

        for item in items:
            new_item = {
                'title': item.title.string,
                'link': item.find("link").string,
                'comments_link': item.find("comments"),
                'publication_date': item.find('pubDate').text
            }
            data.append(new_item)

        return data


crawler = Crawler("https://techcrunch.com")
crawler.crawl()
