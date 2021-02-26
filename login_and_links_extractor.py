"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 01-02-21
    * description:This script logs in to linked-in then redirect to search filter for education industry companies and
    * extract its links.
"""
import os
from pathlib import Path
from selenium import webdriver
from time import sleep
import bs4 as bs4

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.__str__() + '/chrome_driver/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)


# get the linked in link
browser.get('https://www.linkedin.com/')

# get login information from text file
with open('login.txt', 'r') as log_in_file:
    credentials = log_in_file.readlines()
    email = str(credentials[0].strip())
    password = str(credentials[1].strip())

# find  the login fields
username_field = browser.find_element_by_id('session_key')
password_field = browser.find_element_by_id('session_password')

# fill in the login fields
username_field.send_keys(email)
password_field.send_keys(password)
sleep(0.5)
# hit enter
password_field.submit()
sleep(0.5)

# _redirecting to the search filter (Companies, LOCATION: Australia, INDUSTRY: {Education Management, Higher Education})_


url = 'https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22101452733%22%5D&industry=%5B%22128%22%5D&origin=FACETED_SEARCH'


# creating the pages links
pages = set()
i = 1
while i <= 71:
    curl_url = url + '&page=' + str(i)
    pages.add(curl_url)
    i += 1

# iterating through each page and get the companies links
links_list = []
for page in pages:
    browser.get(page)
    sleep(0.5)
    each_page = browser.page_source
    soup = bs4.BeautifulSoup(each_page, 'lxml')
    links_container = soup.find_all('span', class_='entity-result__title-text t-16')
    if links_container:
        for a in links_container:
            link = a.find('a', class_='app-aware-link', href=True)
            links_list.append(link['href'])
    print(links_list)

# save the links to text file
companies_links_file_path = os.getcwd().replace('\\', '/') + '/Commercial_Real_Estate_links.txt'
with open(companies_links_file_path, 'w') as companies_links_file:
    for i in links_list:
        if i is not None and i != "" and i != "\n":
            if i == links_list[-1]:
                companies_links_file.write(i.strip())
            else:
                companies_links_file.write(i.strip() + '\n')