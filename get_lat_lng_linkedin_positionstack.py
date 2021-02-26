import pandas as pd
import http.client, urllib.parse
import json
from time import sleep

API_KEY = 'put positionstack api key here'
conn = http.client.HTTPConnection('api.positionstack.com')


# reading company name from csv to dataframe
places_name = pd.read_csv('csv/Automotive.csv', usecols=["Name"])



# getting the company lat & lng for each company name in the csv file
for index, row in places_name.iterrows():
    sleep(1)
    try:
        query = str(row['Name'])
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
        print('LONGITUDE: ' + str(lng) + '\nLATITUDE: ' + str(lat) + '\n')
    except TypeError:
        print('\nType error happened at '+str(query)+' is not found!\n')
    except IndexError:
        print('\nAn indexError happened at '+str(query)+'\n')
    except KeyError:
        print('\nKeyError happened at '+str(query)+'\n')

    places_name.to_csv('Automotive_geo.csv', index=False)
