from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
#search_section
######################
# Stage 1.
# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\where\you\download\the\chromedriver.exe')
driver = webdriver.Chrome()

years = list(range(2017,2016,-1))
halfone = [str(i) + '-01-01&to=' + str(i) + '-06-01' for i in years]
halftwo = [str(i) + '-06-01&to=' + str(i) + '-12-31' for i in years]
dates = []
for i in range(0,len(halfone),1):
    dates.append(halftwo[i])
    dates.append(halfone[i])

web_start = 'https://www.riaa.com/gold-platinum/?tab_active=default-award&ar=&ti=&lab=&genre=&format=&date_option=certification&from='
web_end = '&award=&type=&category=&adv=SEARCH#search_section'
websites = [web_start + date + web_end for date in dates]



for web in websites:
	print('Loading website for year ' + web[120:130])
	driver.get(web)
	time.sleep(7)
	csvname = ('riaa_' + web[120:130] + '.csv')
	print("STAGE 1: Clicking down to specified number")
	index = 1
	x = 'LOAD MORE RESULTS'
	while x == 'LOAD MORE RESULTS':
		time.sleep(1)
		try:
			print("Click Down Number:" + str(index))
			index = index + 1
			button = driver.find_element_by_xpath('.//span[@style="margin-right: 0px;"]')
			driver.execute_script("arguments[0].click();", button)
			x = driver.find_element_by_xpath('//div[@class="text-center loadmore-gnp"]/a').text
		except Exception as e:
			print(e)
			driver.close()
			break
######################
# Stage 2.
	print('*' * 20)
	print("STAGE 2: Gathering data from tables")

	# Initialize csv writing for original tabs
	csv_file1 = open(csvname, 'w')
	writer1 = csv.writer(csv_file1)
	writer1.writerow(['Artist', 'Title', 'Certification_Date', 'Label', 'Format_Type', 'Release_Date', 'Group_Type', 'Media_Type', 'Number_of_Units', 'Genre'])

	# Gather information from the original tabs and write to csv
	time.sleep(3)
	entries2 = driver.find_elements_by_xpath('//table[@id="search-award-table"]/tbody/tr[@class="table_award_row"]')
	print('Number of entires: ' + str(len(entries2)))
	for entry2 in entries2:

		artist = entry2.find_element_by_xpath('.//td[2]').text
		title = entry2.find_element_by_xpath('.//td[3]').text
		certification_date = entry2.find_element_by_xpath('.//td[4]').text
		label = entry2.find_element_by_xpath('.//td[5]').text
		format_type = entry2.find_element_by_xpath('.//td[6]').text.splitlines()[0]

		exp_button = entry2.find_element_by_xpath('.//td[6]/div/a')
		driver.execute_script("arguments[0].click();", exp_button)
		time.sleep(1)
		num = (2 * (entries2.index(entry2) + 1)) + 1
		tab_xpath = '//table[@id="search-award-table"]/tbody/tr[' + str(num) + ']/td[@colspan="10"]'
		entries3 = driver.find_elements_by_xpath(tab_xpath)
		print('tab:' + str(len(entries3)))
		if (len(entries3) == 0):
			print('Error... zero occured in year' + web[120:130] + 'at the tab' + str(entries2.index(entry2)))
			break
		else:
			for entry3 in entries3:
				release_date = entry3.find_element_by_xpath('.//td[1]').text
				group_type = entry3.find_element_by_xpath('.//td[3]').text
				media_type = entry3.find_element_by_xpath('.//td[4]').text
				genre = entry3.find_element_by_xpath('.//td[6]').text
				past_certifications = entry3.find_elements_by_xpath('.//td[2]')
				print('cert:' + str(len(past_certifications)))
				if (len(past_certifications) == 0):
					print('Error... zero occured in year' + web[120:130] + 'at the tab' + str(entries2.index(entry2)))
					break
				else:
					for cert in past_certifications:
						temp_cert = cert.text.split(' | ')
						writer1.writerow([artist, title, temp_cert[1], label, format_type, release_date, group_type, media_type, temp_cert[0], genre])
