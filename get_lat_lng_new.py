import pandas as pd
import http.client, urllib.parse
import json
from time import sleep

API_KEY = 'positionstack api key here'
conn = http.client.HTTPConnection('api.positionstack.com')
# url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='

# reading company name from csv to dataframe
places_name = pd.read_csv('csv/T2 Data Manipulation_Subrbs, Regions and Cities.csv', usecols=["SA2 name", "S/T name"])



# getting the company lat & lng for each company name in the csv file
for index, row in places_name.iterrows():
    sleep(1)
    try:
        city_ = str(row['SA2 name'])
        city = str(city_.split(', ')[0].strip())
        state = str(row['S/T name'])
        query = city + ', ' + state
        params = urllib.parse.urlencode({
            'access_key': API_KEY,
            'query': query
        })
        conn.request('GET', '/v1/forward?{}'.format(params))
        response = conn.getresponse()
        data = response.read()
        jsonData = json.loads(data.decode('utf-8'))['data']
        lat = jsonData[0]['latitude']
        lng = jsonData[0]['longitude']
        places_name.loc[int(index), 'Latitude'] = lat
        places_name.loc[int(index), 'Longitude'] = lng
        print('LONGITUDE: ' + str(lng) + '\nLATITUDE: ' + str(lat) + '\n\n')
    except TypeError:
        print('\nType error happened at '+str(query)+' is not found!\n')
    except IndexError:
        print('\nAn indexError happened at '+str(query)+'\n')
    except KeyError:
        print('\nKeyError happened at '+str(query)+'\n')


    # try:
    #     city_ = str(row['SA2 name'])
    #     city = str(city_.split(', ')[0].strip())
    #     state = str(row['S/T name'])
    #     query = city + ', ' + state
    #     # print(query)
    #     response = re.get(url + query + '&key=' + API_KEY)
    #     if response.status_code == 200:
    #         data = response.json()
    #         if data.get("results", []):
    #             formatted_address = response.json()['results'][0]['formatted_address']
    #             lng = response.json()['results'][0]['geometry']['location']['lng']
    #             lat = response.json()['results'][0]['geometry']['location']['lat']
    #             place_id = response.json()['results'][0]['place_id']
    #             print('LONGITUDE: ' + str(lng) + '\nLATITUDE: ' + str(lat) + '\nPLACE ID: ' + str(place_id) + '\nADDRESS: '
    #                   + str(formatted_address) + '\n\n')
    #             places_name.loc[int(index), 'Address_0'] = formatted_address
    #             places_name.loc[int(index), 'Latitude_0'] = lat
    #             places_name.loc[int(index), 'Longitude_0'] = lng
    #             places_name.loc[int(index), 'place_id'] = place_id # I just take it but I'm not using it in the main file
    #         else:
    #             print("the json string was empty")
    #             print(data)
    #     else:
    #         print("the status code returned NOT OK")
    # except TypeError:
    #     print('\nType error happened at '+str(query)+' is not found!\n')
    # except IndexError:
    #     print('\nAn indexError happened at '+str(query)+'\n')
    # except KeyError:
    #     print('\nKeyError happened at '+str(query)+'\n')
    #
    # save places id to csv file
    places_name.to_csv('T2 Data Manipulation_Subrbs, Regions and Cities_geo.csv', index=False)
