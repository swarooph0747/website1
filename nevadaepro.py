##https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true
import requests
from bs4 import BeautifulSoup
from utilities import *
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import asyncio


class NevadaPro:
    def __init__(self):
        self.main_content = []
        self.domain = 'https://nevadaepro.com'
        self.main_url = 'https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml'
        self.headers = headers
        self.cookies = cookies
        self.payload = data

    
    async def main_page(self,pagn=False):
            
            url = 'https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true'
            data = requests.get(url) 
            soup = BeautifulSoup(data.content)
            facet = soup.find('input',attrs={'name':'javax.faces.ViewState'})['value']
            content = soup.find('div',attrs={'id':'advSearchResults'})
            try:
                self.max_rows = int(content.find('span',attrs={'class':'ui-paginator-current'}).text.split('of')[-1].strip())
            except:
                self.max_rows = 100
            table = content.find('table').find('tbody')
            thead = content.find('table').find('thead')
            self.rem_list = ['Alternate Id','Contract/Blanket #','Bid Holder List','Awarded Vendor(s)']
            self.heads = []
            for i in thead.findAll('th'):
                self.heads.append(i.find('span',attrs={'class':'ui-column-title'}).text)
            tasks = []
            body = []
            for i in table.findAll('tr'):
                for j in i.findAll('td'):
                    collection = dict()
                    if i.findAll('td').index(j) == 0:
                        ind_url = self.domain+j.find('a')['href']
                        task1 = asyncio.create_task(self.individual_url(ind_url))
                        tasks.append(task1)
                        task2 = asyncio.create_task(self.file_downloader(ind_url))
                        tasks.append(task2)
                    body.append(j.text)
                collection = {k:v for k,v in zip(self.heads,body)}
                removed = [collection.pop(key) for key in self.rem_list]
                self.main_content.append( collection)
                body.clear()
            await asyncio.gather(*tasks)
            page =1
            filepath = 'Pages/page{}.json'.format(page)
            await write_json(self.main_content,filepath)
            self.main_content.clear()
            
            self.cookies = dict(data.cookies)
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
            soup = BeautifulSoup(data.content)
            tags = soup.findAll('td')

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
            filepath = 'Pages/page{}.json'.format(page)
            await write_json(self.main_content,filepath)
            page += 1
            self.main_content.clear()
            rows += 25
            self.payload['bidSearchResultsForm:bidResultId_first'] = str(rows)            
              
    async def individual_url(self,url):

        data = requests.get(url)
        soup = await BeautifulSoup(data.content)
        title = [i.text.replace('\n','').strip() for i in soup.findAll('td',attrs={'class':'t-head-01','valign':'top'})]
        value = [i.text.replace('\n','').strip() for i in soup.findAll('td',attrs={'class':'tableText-01','valign':'top'})[:title.index('Bill-to Address:')+1]]

        output = {k:v for k,v in zip(title,value)}
        name = output['Bid Number:'].strip()
        filepath = 'Bid_numbers/{}/{}.json'.format(name,name)
        await write_json(self.main_content,filepath)
        

    async def file_downloader(self,url):
        entry = re.search(r'docId=(.*?)&external',url).group(1)
        path = f'D:\webscraper\website1\Bid_numbers\{entry}'
        prefs = {'download.default_directory':path}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs',prefs)
        driver = webdriver.Chrome(options=options)
        driver.get(f'https://nevadaepro.com/bso/external/bidDetail.sdo?docId={entry}&external=true&parentUrl=close')
        attachments = await driver.find_element(By.XPATH,"//tr/td[contains(text(),'File Attachments:')]/parent::node()/td[2]")
        files = await attachments.find_elements(By.TAG_NAME,'a')
        if len(files)> 0:
            for i in files:
                i.click()
                time.sleep(2)
        driver.close()
        # driver.quit()


runner = NevadaPro()
async_runner = asyncio.get_event_loop()
async_runner.run_until_complete(runner.main_page())
# runner.main_page()#pagn=True(optional)
# runner.file_downloader()