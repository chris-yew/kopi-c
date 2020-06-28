## web scraping ##
from bs4 import BeautifulSoup
import requests
import re

## summarize ##
import gensim
from gensim.summarization import summarize



#obtain the url of the site that we want to scrapt
url = 'https://vulcanpost.com/category/news/'
page = requests.get(url)

#store the articles 
articles =[]

# stores the weblink
links = []

#stores the results
results = []

#stores the polluted stories
pstories=[]

#stores the final stories
stories=[]

#stores summarized stories
summaries=[]

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
    story=soup.find_all('p')
    pstories.append(story)

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

for i in pstories:
    res=""
    for p in i:
        res+=str(p)
    sep="Featured Image Credit"
    rest=res.split(sep,1)[0]
    stories.append(striphtml(rest))

# traverse through every news article which is the links to the articles
# for every article, find the tag that contains the story and scrape 
# append results into array



for j in range(len(articles)):
    results.append((articles[j],links[j],stories[j]))
#print(results)

for i in stories:
    summaries.append(summarize(i,ratio=0.2))















































