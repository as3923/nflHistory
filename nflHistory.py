#-----------------------------------------------------------------------
#
#  NFL.COM WEB SCRAPER for HISTORICAL PLAYER STATISTICS
#
#-----------------------------------------------------------------------
#  
#  Written for Python 3.3
#  Gets all the player webpages from NFL.com and records a player's 
#  career stats to a csv file.  Currently only looks at 5 positions.
#
#  Improvements for next time:
#   - Significantly speed up code
#      - Reduce number of loops
#      - Explore asynchronous methods to speed up scrape time
#   - Find public API for more complete and clean data
#   - Read old CSVs and only append updated information
#      - Currently replaces old file each time it is executed
#   - Record data for all positions
#   - Clean up code
#   - Reorganize to do statistical analysis in Python rather than R
#      - Perhaps design positions as objects to eliminate export needs
#         - Methods for common statistical predictions
#
#-----------------------------------------------------------------------

import urllib3
import bs4
import string
import csv
import re
import datetime
# import os

#======================
# Initialized variables
#======================
startTime = datetime.datetime.now()
queued = []
crawled = []
pList = ['QB','RB','WR','TE','K']
dom = 'www.nfl.com'
year = 2013
seasons = range(year-19,year+1)
seasons = [str(x) for x in seasons]

#======================
# Setup and open connection
#======================
pool = urllib3.connectionpool.HTTPConnectionPool(dom,maxsize=1)

#======================
# Dictionary for creating headers in csv file
#======================
statsDict = {}
statsDict['QB'] = ['NAME','SEASON','TEAM','G','GS','Comp','Att','Pct','Yds','Avg','TD','Int','Sck','SckY','Rate','Att','RuYds','RuAvg','RuTD','FUM','Lost']
statsDict['RB'] = ['NAME','SEASON','TEAM','G','GS','Att','RuYds','RuAvg','RuLng','RuTD','Rec','Yds','Avg','Lng','TD','FUM','Lost']
statsDict['WR'] = ['NAME','SEASON','TEAM','G','GS','Rec','Yds','Avg','Lng','TD','Att','RuYds','RuAvg','RuLng','RuTD','FUM','Lost']
statsDict['TE'] = ['NAME','SEASON','TEAM','G','GS','Rec','Yds','Avg','Lng','TD','Att','RuYds','RuAvg','RuLng','RuTD','FUM','Lost']
statsDict['K'] = ['NAME','SEASON','TEAM','G','GS','FGB','LNG','FGA','FGM','PCT','XPM','PCT','XPB','KO','AVG1','TB','RET','AVG2']
noStatsElim = 'This player does not have any statistics...'

#======================
# Create new CSVs
#  - QB, RB, WR, TE, K
#======================
for x in pList:
    # if not os.path.exists(x+'.csv'):
    newF = open(x+'.csv', 'w')
    fil = csv.DictWriter(newF, statsDict[x], lineterminator='\n')
    fil.writeheader()
    newF.close()

#======================
# Clean up single season stats for a player
#======================
def singleSeason(single):
    '''
    Takes in a row<tr> of career stats for a specific player
    Missing numbers are converted to NaN
    Returns the data as a list
    '''
    stats = []
    for x in range(len(single.find_all('td'))):
        singSeason = single.find_all('td')[x]
        if x == 1:
            singSeason = singSeason.a.string
        else:
            singSeason = re.sub('\s+','',str(singSeason.string))
            if singSeason == '--':
                singSeason = float('NaN')
        stats.append(singSeason)
    return stats

#======================
# Write statistics to CSV
# Finds statistics from the 'Career Stats' table
#======================
def pSorter(position,name,soup):
    '''
    Takes in the player's position, their name, and the 'soup'
	Checks each row<tr> to see if it contains stats
    Writes the data to the correct csv file
    Returns nothing
    '''
    cfile = open(position+'.csv', 'a', newline='')
    fd = csv.writer(cfile)
    career = soup.find_all('table')[1].find_all('tr')
    for x in range(len(career)):
        year = career[x].find('td')
        if year.string in seasons:
            single = year.find_parent('tr')
            stats = singleSeason(single)
            fd.writerow([name]+stats)
    cfile.close()
    return

#======================
# Page loader
# If list page, then add all player and page links to queued
# If player page, then grab data and write to CSV
#======================
def loader(url):
    '''
    Takes in a partial URL. 
    If URL is appropriate, append it to the queued list.
    Otherwise execute function to add player statistics to appropriate csv file.
    Returns nothing
    '''
    doc = pool.request('GET',url)
    soup = bs4.BeautifulSoup(doc.data)
    title = soup.title.string
    if title == 'NFL Players':
        links = soup.find(id='searchResults').find_all('a')
        for x in links:
            if str(x)[10] == 'p':
                newUrl = x.get('href')
                if newUrl not in crawled and newUrl not in queued:
                    queued.append(newUrl)
        return
    else: 
        blankQ = soup.find('table', { 'class' : 'data-table1' }).find_all('td')[1].string
        if noStatsElim in blankQ:
            return
        position = soup('span', { 'class' : 'player-number' })[0].string
        position = position.split(' ')
        if position[-1] in pList:
            name = soup('span', { 'class' : 'player-name' })[0].string.rstrip()
            pSorter(position[-1],name,soup)
        return

#======================
# Initial list of pages to crawl
#======================
for letter in string.ascii_uppercase:
    search_url = '/players/search?category=lastName&playerType=current&d-447263-p=1&filter='+letter
    queued.append(search_url)

#======================
# List of bad pages to skip
#======================
# bad = ['/player/weslyesaunders/2495224/profile','http://www.nfl.com/player/evanrodriguez/2532991/profile']
# crawled += bad

#======================
# Work through list of pages in 'queued'
# Add crawled pages to 'crawled'
#======================
errors = 0
while len(queued) > 0:
    current = queued.pop()
    if current not in crawled:
        # scrape page for necessary data
        print(current)
        try:
            loader(current)
        except Exception as e:
            errors += 1
            print(e)
            continue
    crawled.append(current)
    # if len(crawled) == 20:
    #     break
print('Number of crawled pages: ' + str(len(crawled)))
print('Number of errors: ' + str(errors))
print('Elapsed time: ' + str(datetime.datetime.now() - startTime))

#-----------------------------------------------------------------------
#======================
# Tests for bugs during scripting
#======================
# test1
# loader('/player/emmanuelsanders/497322/profile')

# test2
# tq = queued[:]
# for x in tq:
#     print(x)
#     loader(x)

# test3
# loader('http://www.nfl.com/player/matmcbriar/2505268/profile')