import urllib3
import bs4
import string
import csv
import re

dom = 'www.nfl.com'

pool = urllib3.connectionpool.HTTPConnectionPool(dom,maxsize=1)

def loader(url):
    doc = pool.request('GET',url)
    print(doc)
    soup = bs4.BeautifulSoup(doc)
    print(soup.prettify())