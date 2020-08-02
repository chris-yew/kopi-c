from bs4 import BeautifulSoup 
import gensim
import requests
import re
from gensim.summarization import summarize
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

class vulcan:
    def __init__ (self,url):
        self.url=url
        self.links=[]
        self.story=[]
        self.stories=[]
        self.pstories=[]
        self.summaries=[]
        self.time_stamp=[]
        self.database=[]
        self.date_str=[]
        self.product=[]

    
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
            time=soup.find_all(class_="timestamp timeago")
            for j in time:
                self.date_str.append(j["title"])
            self.story.append(soup.find_all(attrs={'class' : 'entry mx-3 mx-md-5'})) 
        
        for i in self.story:
            for j in i:
                self.pstories.append(j.text)
        
        for i in self.date_str:
            date = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
            timestamp = datetime.timestamp(date)
            self.time_stamp.append(timestamp) 

        for i in self.pstories:
            res=""
            for p in i:
                res+=str(p)
            res=re.sub(r"\n","",res)
            res=re.sub(r"Image Credit:","",res)
            sep="Featured Image Credit"
            rest=res.split(sep,1)[0]
            self.stories.append(striphtml(rest))
        return self.stories
        
    def extract(self):
        stories=self.scrap()
        for i in stories:
            self.summaries.append(summarize(i,ratio=0.2))
        return self.summaries 

    def update_to_excel(self):
        summaries=self.extract()
        scope= ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds=ServiceAccountCredentials.from_json_keyfile_name('vulcan_secret.json', scope)
        client = gspread.authorize(creds)
        sheet=client.open("vulcan").sheet1
        latest=self.time_stamp[0]
        if latest>int(sheet.cell(12,1).value):
            for i in range(len(self.links)):
                self.database.append([self.time_stamp[i],self.links[i],self.summaries[i]])

            for i in self.database:
                sheet.insert_row(i)
        print("done")

    def news_highlight(self):
        scope= ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds=ServiceAccountCredentials.from_json_keyfile_name('vulcan_secret.json', scope)
        client = gspread.authorize(creds)
        sheet=client.open("vulcan").sheet1 
        for i in range(1,13):
            self.product.append(sheet.cell(i,3).value)
        return self.product      
        
test=vulcan("https://vulcanpost.com/category/news/")
test.update_to_excel()



        

    






