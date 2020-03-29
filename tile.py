import requests
import json


if __name__ == "__main__":
  response = requests.get("https://api.covid19india.org/data.json")
  if response.status_code == 200:
      x = json.loads(response.content.decode('utf-8'))
      
  with open('india_states.geojson', 'r') as f:
        data = json.load(f)
  for i in range(len(data['features'])):
    a = data['features'][i]['properties']["name"]
    b = x["statewise"]
    for j in b:
      if j['state']!="Total":
        if a == j['state']:
          data['features'][i]['properties']['confirmed_case'] = j['confirmed']
          break
  with open('india_states.geojson', 'w') as file:
        json.dump(data,file)
  
    

