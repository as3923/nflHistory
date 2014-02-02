import requests
import urllib2
from json import load
import csv
import pprint

# HTTP/API access information
url = 'http://fantasysports.yahooapis.com/fantasy/v2/'
data = urllib2.urlopen(url).read()

ykey = 'dj0yJmk9eUY4azYzVXZMQ0RwJmQ9WVdrOU1sUlJlRkJMTldVbWNHbzlNVFF4TmpjNU9ETTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD05Mg--'
ysecret = 'f0e5927e10ae2381dc68a7003715c5603fde6297'



# u is a file-like object
print(data)


## Make request and load information
#url = 'http://api.espn.com/v1/sports/football/nfl/athletes?apikey='
#key = 'zw9869tkrn5qdby48vb7nefe'
#nfl = urlopen(url+key)
#
#jsonO = load(nfl)
#
#for athlete in jsonO['sports']['leagues']['athletes']:
#    print jsonO['displayName']
#
## Export to CSV
##csvfile = csv.writer(open("all.csv", "w"))
#
## print(jsonO)