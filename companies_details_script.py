"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 01-02-21
    * description:This script logs in to linked-in then redirect to each company page and extract its data.
"""
import os
from pathlib import Path
from selenium import webdriver
from time import sleep
import bs4 as bs4
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import copy
import csv
from random import randint as rand

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('detach', True)
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.__str__() + '/chrome_driver/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)  # , options=option

# get the linked in link
browser.get('https://www.linkedin.com/')
sleep(1)
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

# read the url from file into a list
companies_links_file_path = Path(os.getcwd().replace('\\', '/'))
companies_links_file_path = companies_links_file_path.__str__() + '/Commercial_Real_Estate_links.txt'
companies_links_file = open(companies_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/temp.csv'

data = {'Name': 'null', 'Location': 'null', 'Overview': 'null', 'Phone': 'null', 'Industry': 'null', 'Company Size': 'null',
        'Website': 'null', 'Headquarter': 'null', 'Type': 'null', 'Founded': 'null', 'Linked In URL': 'null',
        'Address_0': 'null', 'Latitude_0': 'null', 'Longitude_0': 'null', 'City_0': 'null',
        'Location_description_0': 'null',
        'Address_1': 'null', 'Latitude_1': 'null', 'Longitude_1': 'null', 'City_1': 'null',
        'Location_description_1': 'null',
        'Address_2': 'null', 'Latitude_2': 'null', 'Longitude_2': 'null', 'City_2': 'null',
        'Location_description_2': 'null',
        'Address_3': 'null', 'Latitude_3': 'null', 'Longitude_3': 'null', 'City_3': 'null',
        'Location_description_3': 'null',
        'Address_4': 'null', 'Latitude_4': 'null', 'Longitude_4': 'null', 'City_4': 'null',
        'Location_description_4': 'null',
        'Address_5': 'null', 'Latitude_5': 'null', 'Longitude_5': 'null', 'City_5': 'null',
        'Location_description_5': 'null', 'Country': 'null'}

companies_data_all = []

# Get each company link
for link in companies_links_file:
    # go to about page directly
    linked_in_url = str(link.strip())
    about_page = linked_in_url + '/about/'
    browser.get(about_page)
    sleep(rand(1, 7))
    page_source_ = browser.page_source
    # print(page_source_)
    # print('\n\n\n\n\n\n')
    soup = bs4.BeautifulSoup(page_source_, 'lxml')
    sleep(0.5)


    # Save the linked in url
    data['Linked In URL'] = linked_in_url

    # Save company name
    h1_tag = soup.find('h1', {'class': 'org-top-card-summary__title'})
    if h1_tag:
        name = h1_tag.get_text().strip()
        data['Name'] = name
        print('NAME: ', str(name))
    else:
        data['Name'] = 'null'
        print('NAME: ', str(data['Name']))

    # Overview XPATH '//h4[contains(text(),"Overview")]/following-sibling::p[1]'
    # overview = soup.find('p')#, class_='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal'
    try:
        data['Overview'] = soup.find('h4', text=re.compile('Overview', re.IGNORECASE)).find_next_sibling('p').get_text().strip().replace('\n', '')
        print('OVERVIEW: ', str(data['Overview']))
    except TimeoutException:
        data['Overview'] = 'null'
        print('Overview not found!')
    except AttributeError:
        data['Overview'] = 'null'
        print('attrE Overview not found!')

    # Website
    try:
        WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//dd/a[starts-with(@href,"http")]')))
        data['Website'] = browser.find_element_by_xpath('//dd/a[starts-with(@href,"http")]').text.strip()
        print('WEBSITE: ', str(data['Website']))
    except TimeoutException:
        print('Website not found!')
        data['Website'] = 'null'

    # Phone
    try:
        WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//dd/a[starts-with(@href,"tel")]')))
        data['Phone'] = str(browser.find_element_by_xpath('//dd/a[starts-with(@href,"tel")]').get_property('href').replace('tel:', ''))
        print('PHONE: ', data['Phone'])
    except TimeoutException:
        print('Phone not found!')
        data['Phone'] = 'null'

    # Industry
    try:
        WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section > dl > dd:nth-child(6)')))
        industry = browser.find_element_by_css_selector('section > dl > dd:nth-child(6)').text.strip()
        if 'Education' in industry:
            data['Industry'] = industry
        elif 'Education' in browser.find_element_by_css_selector('section > dl > dd:nth-child(4)').text:
            data['Industry'] = browser.find_element_by_css_selector('section > dl > dd:nth-child(4)').text.strip()
        print('INDUSTRY: ', str(data['Industry']))
    except TimeoutException:
        print('Industry Exception')
        data['Industry'] = 'null'

    # Company Size
    try:
        data['Company Size'] = soup.find('dd',
                                         class_='org-about-company-module__company-size-definition-text').get_text().strip()
        print('COMPANY SIZE: ', str(data['Company Size']))
    except TimeoutException:
        print('company size not found!')
        data['Company Size'] = 'null'
    except AttributeError:
        print('company size not found!')
        data['Company Size'] = 'null'

    # Headquarters
    try:
        data['Headquarter'] = soup.find('dt', text=re.compile('Headquarters', re.IGNORECASE)).find_next(
            'dd').get_text().strip()
        print('HEADQUARTERS: ', str(data['Headquarter']))
    except TimeoutException:
        print('Headquarters not found!')
        data['Headquarter'] = 'null'
    except AttributeError:
        print('Headquarters not found!')
        data['Headquarter'] = 'null'
    # Type
    try:
        data['Type'] = soup.find('dt', text=re.compile('Type', re.IGNORECASE)).find_next(
            'dd').get_text().strip()
        print('TYPE: ', str(data['Type']))
    except TimeoutException:
        print('Type not found!')
        data['Type'] = 'null'
    except AttributeError:
        print('Type not found!')
        data['Type'] = 'null'

    # Founded
    try:
        data['Founded'] = soup.find('dt', text=re.compile('Founded', re.IGNORECASE)).find_next(
            'dd').get_text().strip()
        print('FOUNDED: ', str(data['Founded']))
    except TimeoutException:
        print('Founded not found!')
        data['Founded'] = 'null'
    except AttributeError:
        print('Founded not found!')
        data['Founded'] = 'null'

    # Location
    try:
        data['Location'] = soup.find('p', class_='t-14 t-black--light t-normal break-words').get_text().strip()
        print('LOCATION: ', str(data['Location']))
    except TimeoutException:
        print('Single Location not found!')
        data['Location'] = 'null'
    except AttributeError:
        print('Single Location not found!')
        data['Location'] = 'null'

    # # Taking the map json request from <code> tag and extract the location info from it
    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//code[contains(.,"latitude")]')))
        # pure json string
        map_json_string = browser.find_element_by_xpath('//code[contains(.,"latitude")]').get_attribute(
            'textContent').strip()
        # map_json_string = ''
        # for item in soup.find_all('code'):
        #     if 'latitude' not in item.text:
        #         continue
        #     map_json_string = item.text.strip()
        # print(map_json_string)
        # convert to list
        json_list = json.loads(map_json_string)
        # location list

        try:
            location_list = json_list['data']['elements'][0]['groupedLocations']
        except KeyError:
            location_list = []
            print('code not found!')
        '''
            city_name = location_list[0]['localizedName']
            location_description = location_list[0]['locations'][0]['description']
            street = location_list[0]['locations'][0]['line1']
            city = location_list[0]['locations'][0]['city']
            geographic_area = location_list[0]['locations'][0]['geographicArea']
            postcode = location_list[0]['locations'][0]['postalCode']
            country = location_list[0]['locations'][0]['country']
            json_headquarters = location_list[0]['locations'][0]['headquarter']
            lat = location_list[0]['latLong']['latitude']
            lng = location_list[0]['latLong']['longitude']
        '''

        for index, location in enumerate(location_list):
            if index < 4:
                data['Address_' + str(index)] = 'null'
                data['Latitude_' + str(index)] = 'null'
                data['Longitude_' + str(index)] = 'null'
                data['City_' + str(index)] = 'null'
                data['Location_description_' + str(index)] = 'null'
                data['Country'] = 'null'
                try:
                    try:
                        city_name = location_list[index]['localizedName']
                    except KeyError:
                        city_name = 'null'
                    try:
                        location_description = location_list[index]['locations'][0]['description']
                    except KeyError:
                        location_description = 'null'
                    try:
                        street = location_list[index]['locations'][0]['line1']
                    except KeyError:
                        street = 'null'
                    try:
                        city = location_list[index]['locations'][0]['city']
                    except KeyError:
                        city = 'null'
                    try:
                        geographic_area = location_list[index]['locations'][0]['geographicArea']
                    except KeyError:
                        geographic_area = 'null'
                    try:
                        postcode = location_list[index]['locations'][0]['postalCode']
                    except KeyError:
                        postcode = 'null'
                    try:
                        country = location_list[index]['locations'][0]['country']
                    except KeyError:
                        country = 'null'
                    try:
                        json_headquarters = location_list[index]['locations'][0]['headquarter']
                    except KeyError:
                        json_headquarters = 'null'
                    try:
                        lat = location_list[index]['latLong']['latitude']
                        lng = location_list[index]['latLong']['longitude']
                    except KeyError:
                        lat = 'null'
                        lng = 'null'
                    address = str(street) + ', ' + str(city) + ', ' + str(geographic_area) + ', ' + str(
                        postcode) + ', ' + str(country)
                    data['Address_' + str(index)] = address
                    data['Latitude_' + str(index)] = lat
                    data['Longitude_' + str(index)] = lng
                    data['City_' + str(index)] = city
                    data['Location_description_' + str(index)] = location_description
                    data['Country'] = country
                    print('ADDRESS' + str(index) + ': ', str(data['Address_' + str(index)]))
                    print('LNG' + str(index) + ': ', str(data['Longitude_' + str(index)]))
                    print('LAT' + str(index) + ': ', str(data['Latitude_' + str(index)]))
                except IndexError:
                    print('index error happened')
    except AttributeError:
        print('Attr: Code tag not found!')
    except NoSuchElementException:
        print('NoElement: Code tag not found!')
    except TimeoutException:
        print('code timeout!')
        for index in range(0, 5):
            data['Address_' + str(index)] = 'null'
            data['Latitude_' + str(index)] = 'null'
            data['Longitude_' + str(index)] = 'null'
            data['City_' + str(index)] = 'null'
            data['Location_description_' + str(index)] = 'null'
            data['Country'] = 'null'

    # Tabulate the data
    companies_data_all.append(copy.deepcopy(data))
    desired_order_list = ['Name', 'Location', 'Overview', 'Phone', 'Industry', 'Company Size', 'Website',
                          'Headquarter', 'Type', 'Founded', 'Linked In URL',
                          'Address_0', 'Latitude_0', 'Longitude_0', 'City_0', 'Location_description_0',
                          'Address_1', 'Latitude_1', 'Longitude_1', 'City_1', 'Location_description_1',
                          'Address_2', 'Latitude_2', 'Longitude_2', 'City_2', 'Location_description_2',
                          'Address_3', 'Latitude_3', 'Longitude_3', 'City_3', 'Location_description_3',
                          'Address_4', 'Latitude_4', 'Longitude_4', 'City_4', 'Location_description_4',
                          'Address_5', 'Latitude_5', 'Longitude_5', 'City_5', 'Location_description_5',
                          'Country']

    companies_dict_keys = set().union(*(d.keys() for d in companies_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, companies_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(companies_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('csv/Commercial_Real_Estate.csv', 'w',
                                                               encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)
