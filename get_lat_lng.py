import pandas as pd
import requests as re

API_KEY = 'google api key here'

url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='

# reading company name from csv to dataframe
places_name = pd.read_csv('csv/Architecture_&_Planning.csv', usecols=["Name"])


# getting the company lat & lng for each company name in the csv file
for index, row in places_name.iterrows():
    try:
        query = str(row['Name'])
        # print(query)
        response = re.get(url + query + '&key=' + API_KEY)
        formatted_address = response.json()['results'][0]['formatted_address']
        lng = response.json()['results'][0]['geometry']['location']['lng']
        lat = response.json()['results'][0]['geometry']['location']['lat']
        place_id = response.json()['results'][0]['place_id']
        print('LONGITUDE: ' + str(lng) + '\nLATITUDE: ' + str(lat) + '\nPLACE ID: ' + str(place_id) + '\nADDRESS: '
              + str(formatted_address) + '\n\n')
        places_name.loc[int(index), 'Address_0'] = formatted_address
        places_name.loc[int(index), 'Latitude_0'] = lat
        places_name.loc[int(index), 'Longitude_0'] = lng
        places_name.loc[int(index), 'place_id'] = place_id # I just take it but I'm not using it in the main file
    except TypeError:
        print("\nType error happened at "+str(row['Name'])+" is not found!\n")
    except IndexError:
        print('\nAn indexError happened at '+str(row['Name'])+'\n')
    except KeyError:
        print('\nKeyError happened at '+str(row['Name'])+'\n')

    # save places id to csv file
    places_name.to_csv('Architecture_&_Planning_geo.csv', index=False)
