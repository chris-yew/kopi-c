## web scraping ##
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

## summarize ##
import gensim
from gensim.summarization import summarize
from gensim.summarization import keywords

## dataframe ##
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#obtain the url of the site that we want to scrapt
url = 'https://vulcanpost.com/category/news/'
page = requests.get(url)

#store date#
date_str=[]

#stores timestamp#
time_stamp=[]

#store the articles 
articles =[]

# stores the weblink
links = []

#stores the results
results = []

#stores inital stories
story=[]

#stores the polluted stories
pstories=[]

#stores the final stories
stories=[]

#stores summarized stories
summaries=[]

#update spreadsheet"
database=[]

soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.p)
news_headlines = soup.find_all('div',class_ = 'article-excerpt')
web_links = soup.find_all('a',class_ = 'article-list-item')


# loop the headlines and append the headlines
for i in news_headlines:
    #print(i.find('p').text)
    articles.append(i.find('p').text)

for i in web_links:
    #print(i['href'])
    links.append('https://vulcanpost.com/'+ i['href'])

for i in links:
    page=requests.get(i)
    soup=BeautifulSoup(page.content,'html.parser')
    time=soup.find_all(class_="timestamp timeago")
    for j in time:
        date_str.append(j["title"])
    story.append(soup.find_all(attrs={'class' : 'entry mx-3 mx-md-5'})) 

for i in story:
    for j in i:
            pstories.append(j.text)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

for i in date_str:
    date = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
    timestamp = datetime.timestamp(date)
    time_stamp.append(timestamp)

for i in pstories:
    res=""
    for p in i:
        res+=str(p)
    res=re.sub(r"\n","",res)
    res=re.sub(r"Image Credit:","",res)
    sep="Featured Image Credit"
    rest=res.split(sep,1)[0]
    stories.append(striphtml(rest))

# traverse through every news article which is the links to the articles
# for every article, find the tag that contains the story and scrape 
# append results into array

#for j in range(len(articles)):
#    results.append((time_stamp[j],articles[j],links[j],stories[j]))
#print(results)

for i in stories:
    summaries.append(summarize(i,ratio=0.2))

## spreadsheet ##
scope= ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds=ServiceAccountCredentials.from_json_keyfile_name('vulcan_secret.json', scope)
client = gspread.authorize(creds)

sheet=client.open("vulcan").sheet1


for i in range(len(links)):
    database.append([time_stamp[i],links[i],summaries[i]])

for i in database:
    sheet.insert_row(i)


