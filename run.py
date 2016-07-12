from lxml import html
from bs4 import BeautifulSoup
from six.moves.html_parser import HTMLParser
from collections import defaultdict
import requests
import argparse

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
        feeds = FeedApi(content, markup)
        data = feeds.getFeeds()

        return data

    def getMarkup(self, content_type):
        if 'xml' in content_type:
            markup = 'xml'
        elif 'html' in content_type:
            markup = 'html'

        return markup

class FeedApi:
    # Class to handle Feeds
    def __init__(self, data, markup):
        self.obj = BeautifulSoup(data, markup)
        self.html_parser = HTMLParser()

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
                'title': self.html_parser.unescape( item.title.string ),
                'link': item.find("link").string,
                'comments_link': item.find("comments"),
                'publication_date': item.find('pubDate').text,
                'author': self.html_parser.unescape( item.find('creator').text )
            }
            data.append(new_item)

        return data

class FeedToDB:
    def __init__(self, feeds, save_file):
        self.feeds = feeds
        self.save_file = save_file
        # self.dbms = type

    def setupDB(self):
        # into
        print "\n====== Database Configuration ======\n"

        # setup type
        db_type = raw_input("Please select database type: ")
        accepted_dbs = ['mysql', 'mongodb']

        if db_type in accepted_dbs:
            print("Yea I am an accepted db " + db_type)
        else:
            # add proper error handling
            print("I am not an accepted db")

    def saveToFile(self):
        return


    # connect to database (future use allow setting of differnet types)
    # for now connect to mongodb database type=mongodb
    # setup feed model
    # write to db
    # def

# Top Level parser
parser = argparse.ArgumentParser(prog='RSS-Crawler')

# group arguments for mutually exclusive
group_1 = parser.add_mutually_exclusive_group(required=True)
group_1.add_argument('-url', action="store", type=str)
group_1.add_argument('-file', action="store", type=str)

group_2 = parser.add_mutually_exclusive_group(required=True)
group_2.add_argument('-database', action="store_true", default=False)
group_2.add_argument('-export', action="store_false", default=False)

args = parser.parse_args()

if not any(vars(args).values()):
    # no arguments passed
    pass
elif args.url:
    # option url passed
    crawler = Crawler(args.url)
    output = crawler.crawl()

    if args.database:
        obj = FeedToDB(output, True)
        obj.setupDB()

    # for now just output to console

    # print(output)
elif args.file:
    # read from file
    # todo: future development
    pass
