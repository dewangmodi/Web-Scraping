import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
import os



class Scrapping:

	__driver = None
	__tickers = []
	__security = []
	__sleeptime = 5
	__go_headless = True
	
	
	




	def list_of_companies(self):
	    '''Gets the data in the form of list of tuples and also saves them in a csv file'''
	    link = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies?fbclid=IwAR2BxaUEjOht2ky9OUD3Aotf1hJ2YUyU4HGulBI52DRMr3Bharm8h7_7ADg'
	    outputfile = 'list_of_companies.csv'
	    page = requests.get(link)
	    soup = BeautifulSoup(page.content,'html.parser')
	    table = soup.find(id="constituents")
	    table_rows = table.find_all('tr')
	    self.tickers = []
	    self.security = []
	    for rows in table_rows[1:]:
	        self.tickers.append(rows.contents[1].get_text())
	        self.security.append(rows.contents[3].get_text())
	    
	    data_df = pd.DataFrame({'Tickers':self.tickers,'Security':self.security})
	    data_df.to_csv(outputfile, index=False)
	    


	def scrape_company(self,ticker):
		'''Scrape the data of company with given ticker and write key stats to ticker_key_stats_overview.csv and data to ticker_key_stats_data.csv'''
		link = 'https://stockrow.com/'+ticker
		self.driver.get(link)
		time.sleep(self.sleeptime)
		soup = BeautifulSoup(self.driver.page_source,'html.parser')
		key_stats_overview = soup.find('table',class_='keystats-overview')
		if key_stats_overview == None:
			return
		labels = key_stats_overview.find_all('div',class_='cell-label')
		labels = [i.get_text() for i in labels]
		values = key_stats_overview.find_all('div',class_='cell-value')
		values = [i.get_text() for i in values]
		data_df = pd.DataFrame({'Labels':labels,'Values':values})
		data_df.to_csv(ticker+'_key_stats_overview.csv',index=False)

		key_stats_data = soup.find('table',class_='keystats-data')
		if key_stats_data == None:
			return

		rows = key_stats_data.find_all('tr')
		headers = rows[0].find_all('th')
		headers = [i.get_text() for i in headers]
		headers[0] = 'Captions'
		writer = open(ticker+'_key_stats_data.csv','w')
		for i in range(len(headers)-1):
			writer.write(headers[i]+',')
		writer.write(headers[i+1])
		
		for i in rows[1 :]:
			writer.write('\n')
			j = i.find_all('span')
			if len(j)==0:				#handle empty rows
				continue

			for k in range(len(j)-1):
				writer.write(j[k].get_text()+',')

#			print(j)
#			print(len(j))

			writer.write(j[len(j)-1].get_text())

		writer.close()





	def scrape_all_companies(self):
#		print('hi here')

#		print(self.tickers)
		
		if len(self.tickers)==0:
	#		print('here')
			self.list_of_companies()

		for symbol in self.tickers:
	#		print('here')
			print(symbol)
			self.scrape_company(symbol)

	def __init__(self,tickers=[],security=[],sleeptime=5,go_headless=True):
		self.tickers = tickers
		self.security = security
		self.sleeptime = sleeptime
		self.go_headless = go_headless
		options = Options()
		options.headless = go_headless
		self.driver = webdriver.Firefox(options=options, executable_path=os.getcwd()+'/geckodriver')



















        
        
    
    
    
    