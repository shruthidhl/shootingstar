import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
from pymongo import database
from pymongo.database import Database
import requests
import datetime as dt
import warnings
import re
import emoji
from configparser import SafeConfigParser
import codecs


class TransformData:

  #URI="mongodb+srv://jaiahujaa:Jaiahuja9$@cluster0.ehbij.mongodb.net/test"
  database=''
 
  @staticmethod
  def initialize():
    parser = SafeConfigParser()
    with codecs.open('C:/Users/Dell/Documents/GitHub/big-data-programming-april2021-group-5/project/python/app.ini', 'r', encoding='utf-8') as f:
        parser.read_file(f)
    URI=parser['mongodb']['mongodb_url']


    client=pymongo.MongoClient(URI)
    TransformData.database=client["Linkedin"]
    return TransformData.database
          

def RemoveEmojis(sentence,):
        return emoji.get_emoji_regexp().sub(r'', sentence)


def removeSpecialCharacters(text):
    text = RemoveEmojis(text,)
     # remove URLs
    text = re.sub('http\S+\s*', ' ',text) 
     # remove #
    text = re.sub('#\S+', '', text) 
    # remove @
    text = re.sub('@\S+', '  ', text)  
    # remove signs and bullets
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~•▪︎➦"""), ' ',text)  
    # remove extra whitespace
    text = re.sub('\s+', ' ', text)  
    text = re.sub('\n',' ', text)
    text = re.sub('Null','', text)
    return text

#clean profile part od collected Json
def CleanProfileData():
    dbName=TransformData.initialize()
    #profile collection
    profile = dbName['profile_data']
    profile_df = pd.DataFrame(list(profile.find()))
    
    profile_text = profile_df[['profile_id','occupation','headline','summary']]
    profile_text.fillna('Null', inplace = True)
    profile_text['text1'] = profile_text[['occupation','headline','summary']].agg(' '.join, axis =1)
    profile_text.text1 = profile_text.text1.apply(lambda x: removeSpecialCharacters(x))
    
    return profile_text


#clean experience part of collected Json Data
def cleanExperienceData():
    dbName=TransformData.initialize()
    #expereince Collection
    experience = dbName['experience_data']
    experience_df = pd.DataFrame(list(experience.find()))
    experience_text = experience_df[['profile_id','title','description','company']]
    experience_text.fillna('Null',inplace = True)
    experience_text['text2'] = experience_text[['title','description','company']].agg(' '.join, axis =1)
    experience_text.text2 = experience_text.text2.apply(lambda x: removeSpecialCharacters(x))
    experience_text = experience_text[['profile_id','text2']]
    experience_text['text2'] = experience_text.groupby(['profile_id'])['text2'].transform(lambda x : ' '.join(x))
    experience_text.drop_duplicates(inplace = True)
    experience_text.reset_index(drop = True, inplace = True)
    

    return experience_text

#clean Candidates Education Data
def cleanEducationData():
    dbName=TransformData.initialize()
    education = dbName['education_data']
    education_df = pd.DataFrame(list(education.find()))
    education_text = education_df[['profile_id','field_of_study','degree_name','description']]
    education_text.fillna('Null',inplace = True)
    education_text['text3'] = education_text[['field_of_study','degree_name','description']].agg(' '.join, axis =1)
    education_text.text3 = education_text.text3.apply(lambda x: removeSpecialCharacters(x))
    education_text = education_text[['profile_id','text3']]
    education_text['text3'] = education_text.groupby(['profile_id'])['text3'].transform(lambda x : ' '.join(x))
    education_text.drop_duplicates(inplace = True)
    education_text.reset_index(drop = True, inplace = True)
    
    return education_text

#clean Candiadtes Award data
def cleanAwardsData():  
    dbName=TransformData.initialize()
    award = dbName['ac_award']
    ac_award_df = pd.DataFrame(list(award.find()))
    award_text = ac_award_df[['profile_id','title']]
    award_text.fillna('Null',inplace = True)
    award_text['text4'] = award_text[['title']].agg(' '.join, axis =1)
    award_text.text4 = award_text.text4.apply(lambda x: removeSpecialCharacters(x))
    award_text = award_text[['profile_id','text4']]
    award_text['text4'] = award_text.groupby(['profile_id'])['text4'].transform(lambda x : ' '.join(x))
    award_text.drop_duplicates(inplace = True)
    award_text.reset_index(drop = True, inplace = True)
    
    return award_text

#clean Project Data
def cleanProjectData(): 
    dbName=TransformData.initialize()
    project = dbName['ac_project']
    ac_project_df = pd.DataFrame(list(project.find()))
    project_text = ac_project_df[['profile_id','title']]
    project_text.fillna('Null',inplace = True)
    project_text['text5'] = project_text[['title']].agg(' '.join, axis =1)
    project_text.text5 = project_text.text5.apply(lambda x: removeSpecialCharacters(x))
    project_text = project_text[['profile_id','text5']]
    project_text['text5'] = project_text.groupby(['profile_id'])['text5'].transform(lambda x : ' '.join(x))
    project_text.drop_duplicates(inplace = True)
    project_text.reset_index(drop = True, inplace = True)
    
    return project_text


def textCleaning():
    warnings.filterwarnings('ignore')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    profile_text_df=CleanProfileData()  
    #if profile_text_df is not None: profile_text_df = pd.DataFrame (data = [profile_text_df.iloc[:,0],
    # profile_text_df.iloc[:,1]])  

    experience_text_df=cleanExperienceData()
    # if experience_text_df is not  None:
    # experience_text_df = pd.DataFrame (data = [experience_text_df.iloc[:,0],experience_text_df.iloc[:,1]])  
    
    
    df1 = pd.merge(profile_text_df, experience_text_df, on = 'profile_id')
    df2 = pd.merge(df1, cleanEducationData(), on = 'profile_id')
    df3 = pd.merge(df2, cleanAwardsData(), on = 'profile_id')
    mega_text = pd.merge(df3, cleanProjectData(), on = 'profile_id')
    mega_text['text'] = mega_text[['text1','text2','text3','text4','text5']].agg(' '.join, axis =1)
    mega_text = mega_text[['text']]
    return mega_text













      




    
    
    
    







  
