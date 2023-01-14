import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
import requests
from configparser import SafeConfigParser
import codecs
import aiohttp
import asyncio



#this is a one time opeartion as proxy curl api charges for every request that's being send to linkedin 
class DataCollection:
  parser = SafeConfigParser()

  def dbConnection():
     # Establish Connection with cloud server
     #conn = "mongodb+srv://jaiahujaa:Jaiahuja9$@cluster0.ehbij.mongodb.net/test"
     conn=DataCollection.parser['mongodb']['mongodb_url']
     client = MongoClient(conn)
     # Connect to Database
     dbName=parser['mongodb']['dbName']
     db = client[dbName]
  def cleanLinkedProfileUrls():
     #read linkednInProfile urls from excel sheet
     profile_df = pd.read_excel('Profile Links.xlsx')
     profile_df['Links'].iloc[20:40]

     #splitting the links
     for i in range(99):
         profile_df['Links'].iloc[i] = profile_df.Links.iloc[i].split('?')[0]

     #saving cleaned link to proxy curl
     profile_df.to_excel('linkedin_profiles.xlsx')
     profiles_df = pd.read_excel('linkedin_profiles.xlsx')

     profiles_list = []
     for index,value in profiles_df.Links.items():
         profiles_list.append(value)

     return profiles_list

  # api call to proxycul  to gather data 
  async def connectToProxyCurl():
       results=[]
       session = aiohttp.ClientSession()
       tasks = DataCollection.get_tasks(session)   
       responses = await asyncio.gather(*tasks)
       for response in responses:
            results.append(await response.json())
            await session.close()
       return results

    
  def get_tasks(session):
    #api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    #api_key = 'FLJfoTCJ-Mf3Wfx_zKUPLQ'
    tasks = []
    db=DataCollection.dbConnection()
    linkdProfCol = db['Linkedin_Profiles']

    profiles_list=DataCollection.cleanLinkedProfileUrls

     # Open the file with the correct encoding
    with codecs.open('app.ini', 'r', encoding='utf-8') as f:
          DataCollection.parser.readfp(f)
          
    password = DataCollection.parser['proxycurl']['password']
    api_endpoint=   DataCollection.parser['proxycurl']['api_endpoint']
    api_key=DataCollection.parser['proxycurl']['api_key']

    header_dic = {'Authorization': 'Bearer ' + api_key}

    for profile in profiles_list:
        params = {
                 'url': profile,
                 'use_cache': 'if-present'}
        tasks.append(session.get(api_endpoint,
                        params=params,
                        headers=header_dic))
    return tasks
 


  def saveProfiles( results):
    db=DataCollection.dbConnection()
    linkdProfCol = db['Linkedin_Profiles']

    profiles_list=DataCollection.cleanLinkedProfileUrls
    for i in range (len(results)):
            linkdProfCol.insert_one(results[i])
            print(db.list_collection_names())


results=asyncio.run(DataCollection.connectToProxyCurl())
#saving each invidual profile data to mongo db collection Linkedin_Profiles  
DataCollection.saveProfiles(results)




