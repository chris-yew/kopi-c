from bs4 import BeautifulSoup 
import gensim
import requests
import re
from gensim.summarization import summarize

class vulcan:
    def __init__ (self,url):
        self.url=url
        self.links=[]
        self.stories=[]
        self.pstories=[]
        self.summaries=[]

    
    def scrap(self):
        page=requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        web_links = soup.find_all('a',class_ = 'article-list-item')
        print(web_links)

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
        print(self.stories)
        return self.stories ## turn into html? ##

    def extract(self):
        stories=self.scrap()
        for i in stories:
            self.summaries.append(summarize(i,ratio=0.2))
        return self.summaries ## turn into html?##

test=vulcan("https://vulcanpost.com/category/news/")
result=test.scrap()
print(result)
        

    






