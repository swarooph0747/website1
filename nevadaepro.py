##https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true
import requests
from bs4 import BeautifulSoup
from utilities import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import asyncio


class NevadaPro:
    def __init__(self):
        self.main_content = []
        self.ind_content = []
        self.domain = 'https://nevadaepro.com'
        self.main_url = 'https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml'
        self.headers = headers
        self.cookies = cookies
        self.payload = data

    
    async def main_page(self,pagn=False):
            
            url = 'https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true'
            data = requests.get(url)
            try: 
                soup = BeautifulSoup(data.content)
            except:
                soup = ''
            try:
                facet = soup.find('input',attrs={'name':'javax.faces.ViewState'})['value']
            except:
                facet = ''
            try:
                content = soup.find('div',attrs={'id':'advSearchResults'})
            except:
                content = ''
            try:
                self.max_rows = int(content.find('span',attrs={'class':'ui-paginator-current'}).text.split('of')[-1].strip())
            except:
                self.max_rows = 0
            try:
                table = content.find('table').find('tbody')
            except:
                table = ''
            try:
                thead = content.find('table').find('thead')
            except:
                thead = ''
            self.rem_list = ['Alternate Id','Contract/Blanket #','Bid Holder List','Awarded Vendor(s)']
            self.heads = []
            if thead != '':
                for i in thead.findAll('th'):
                    self.heads.append(i.find('span',attrs={'class':'ui-column-title'}).text)
            tasks = []
            body = []
            if table !='':
                for i in table.findAll('tr'):
                    for j in i.findAll('td'):
                        collection = dict()
                        if i.findAll('td').index(j) == 0:
                            ind_url = self.domain+j.find('a')['href']
                            task1 = asyncio.create_task(self.individual_url(ind_url))
                            tasks.append(task1)
                            # task2 = asyncio.create_task(self.file_downloader(ind_url))
                            # tasks.append(task2)
                        body.append(j.text)
                    collection = {k:v for k,v in zip(self.heads,body)}
                    removed = [collection.pop(key) for key in self.rem_list]
                    self.main_content.append( collection)
                    body.clear()
                await asyncio.gather(*tasks)
                page =1
                filepath = 'Pages/page{}.json'.format(page)
                write_json(self.main_content,filepath)
                self.main_content.clear()
            
            self.cookies = dict(data.cookies)
            if facet != '':
                self.payload['javax.faces.ViewState'] = facet
            self.payload['_csrf'] = self.cookies['XSRF-TOKEN']
            if pagn:
                page += 1
                self.paginition(page)
            
    async def paginition(self,page):
        rows = 25
        tasks = []
        while rows < self.max_rows:
            count = 0
            collection =dict()
            data = requests.post(self.main_url,headers = self.headers,cookies=self.cookies,data=self.payload)
            try:
                soup = BeautifulSoup(data.content)
                tags = soup.findAll('td')
            except:
                tags = []
            if tags:
                while count < len(tags):
                    body = [i for i in soup.findAll('td')[count:count+10]]
                    body_text = [i.text for i in body]
                    href = body[0].find('a')['href']
                    ind_url = self.domain+ href
                    task1 = asyncio.create_task(self.individual_url(ind_url))
                    tasks.append(task1)
                    task2 = asyncio.create_task(self.file_downloader(ind_url))
                    tasks.append(task2)
                    collection = {k:v for k,v in zip(self.heads,body_text)}
                    removed = [collection.pop(key) for key in self.rem_list]
                    self.main_content.append( collection)
                    count += 10
                await asyncio.gather(*tasks)
                filepath = 'Pages/page{}.json'.format(page)
                write_json(self.main_content,filepath)
                page += 1
                self.main_content.clear()
                rows += 25
                self.payload['bidSearchResultsForm:bidResultId_first'] = str(rows)            
              
    async def individual_url(self,url):

        data = requests.get(url)
        soup = BeautifulSoup(data.content)
        try:
            title = [i.text.replace('\n','').replace('  ','').strip() for i in soup.findAll('td',attrs={'class':'t-head-01','valign':'top'})]
        except:
            title = []
        try:
            value = [i.text.replace('\n','').replace('  ','').strip() for i in soup.findAll('td',attrs={'class':'tableText-01','valign':'top'})[:title.index('Bill-to Address:')+1]]
        except:
            value = []

        output = {k:v for k,v in zip(title,value)}
        name = output['Bid Number:'].strip()
        filepath = 'Bid_numbers/{}/{}.json'.format(name,name)
        write_json(output,filepath)
        

    async def file_downloader(self,url):
        entry = re.search(r'docId=(.*?)&external',url).group(1)
        path = f'D:\webscraper\website1\Bid_numbers\{entry}'
        prefs = {'download.default_directory':path}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs',prefs)
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(f'https://nevadaepro.com/bso/external/bidDetail.sdo?docId={entry}&external=true&parentUrl=close')
            attachments = driver.find_element(By.XPATH,"//tr/td[contains(text(),'File Attachments:')]/parent::node()/td[2]")
            files = attachments.find_elements(By.TAG_NAME,'a')
        except:
            files = []
        if len(files)> 0:
            for i in files:
                i.click()
                time.sleep(2)
        driver.close()
        # driver.quit()


runner = NevadaPro()
async_runner = asyncio.get_event_loop()
async_runner.run_until_complete(runner.main_page())#pagn=True(optional)
# runner.main_page()#pagn=True(optional)
# runner.file_downloader()