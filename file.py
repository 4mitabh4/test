import requests
# import sys
from bs4 import BeautifulSoup
import json


def getdata(url):
  x = requests.get(url)
  return x.text

if __name__ == "__main__":
  # sys.stdout = open('output.txt', "w")
  data = getdata('https://www.mohfw.gov.in/')
  soup = BeautifulSoup(data, 'html.parser')
  mydata=''
  for tr in soup.find_all('div', {'class': 'content'}):
    for i in tr.find_all('tbody'):
      mydata += i.get_text()
  
  mylist = mydata.split("\n\n")
  n=len(mylist) - 5
  total = mylist[n:]
  mylist=mylist[:n]
  l=[]
  for i in mylist[1:]:
    l.append(i.split('\n'))
  for i in range(len(l)):
    if i > 0:
      l[i]=l[i][1:]
  d={}
  for i in range(len(l)):
    d[l[i][1]] = l[i][:1]+l[i][2:]
  with open('new_data.json', 'w') as file:
    json.dump(d,file)
  
  d = {}
  a = []
  k=1
  for i in l:
      d['sl_no'] = k
      d['name'] = i[1]
      d['c_case_n'] = i[2]
      d['c_case_i'] = i[3]
      d['cured'] = i[4]
      d['death'] = i[5]
      a.append(d.copy())
      k+=1
  with open('test.json', 'w') as file:
    json.dump(a, file)

  # data collection part ends
  # data transfer part starts 
  with open('india_states.geojson', 'r') as f:
        data = json.load(f)
  with open('new_data.json', 'r') as file:
      xx = json.load(file)
  for i in range(len(data['features'])):

      # update confirmed case
      a = data['features'][i]['properties']["confirmed_case"]
      b = xx.get(str(data['features'][i]['properties']["name"]))
      if b:
          data['features'][i]['properties']["confirmed_case"]= b[1]
      
      # update death
      c =data['features'][i]['properties']["Death"]
      d = xx.get(str(data['features'][i]['properties']["name"]))
      if d:
        if c !=d[4]:
          data['features'][i]['properties']["Death"]=d[4]
    #   # print(data['features'][i]['properties'])
    
  with open('india_states.geojson', 'w') as f:
        json.dump(data, f)
