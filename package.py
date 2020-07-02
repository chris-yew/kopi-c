from bs4 import BeautifulSoup 
import gensim
import requests
import re

class vulcan:
    def __init__ (self,url):
        url=self.url
        self.links=[]
        self.stories=[]
        self.pstories=[]
        self.summaries=[]

    
    def scrap(self):
        page=requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        web_links = soup.find_all('a',class_ = 'article-list-item')

        def striphtml(data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)


        for i in web_links:
            self.links.append('https://vulcanpost.com/'+ i['href'])
        
        
        for i in self.links:
            page=requests.get(i)
            soup=BeautifulSoup(page.content,'html.parser')
            story=soup.find_all('p')
            self.pstories.append(story)

        for i in self.pstories:
            res=""
            for p in i:
                res+=str(p)
                sep="Featured Image Credit"
                rest=res.split(sep,1)[0]
                self.stories.append(striphtml(rest))

        

    def extract(self):

    





