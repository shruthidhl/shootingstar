import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
import requests
import datetime as dt
from configparser import SafeConfigParser
import codecs


#client = MongoClient('mongodb://127.0.0.1:27017/')
parser = SafeConfigParser()
with codecs.open('C:/Users/Dell/Documents/GitHub/big-data-programming-april2021-group-5/project/python/app.ini', 'r', encoding='utf-8') as f:
        parser.read_file(f)

conn=parser['mongodb']['mongodb_url']
#conn = "mongodb+srv://jaiahujaa:Jaiahuja9$@cluster0.ehbij.mongodb.net/test"
client = MongoClient(conn)
dbName=parser['mongodb']['dbName']
db = client[dbName]

import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

print(db.list_collection_names())

# CONNECTING TO THE COLLECTION 
linkedInProfiles = ''


def cleaningProfileData():
    #reading required fields
   
    linkedInProfiles=pd.DataFrame(list(db['Linkedin_Profiles'].find()))
    profile_fields = linkedInProfiles[['_id','public_identifier','first_name','last_name','occupation','headline',
             'summary','country_full_name','city','experiences','education','languages',
            'accomplishment_organisations','accomplishment_publications',
             'accomplishment_honors_awards','accomplishment_patents',
             'accomplishment_courses','accomplishment_projects', 'accomplishment_test_scores',
             'volunteer_work', 'certifications','connections','recommendations']]

   # DROP COLUMNS WITH NaN
    profile_fields.dropna(thresh = 15, inplace = True)
    profile_fields.reset_index(drop = True, inplace =True)

   #check for duplicates 
    profile_fields.public_identifier.duplicated().value_counts()

   #insert data to mongodb
    profile_fields.insert(0, 'profile_id', range(0,len(profile_fields)))
    return profile_fields


# Select the subset DataFrame
# Explode the dataframe
# Convert the dictionary based column to Series and then concat to a DataFrame

def linkedin_col_parser(df,_id,col):
    df1 = df[[_id, col]]  
    df1 = df1.explode(col)
    df1.reset_index(drop = True, inplace = True)
    df2 = df1[col].apply(pd.Series)
    
    return (pd.concat([df1,df2], axis = 1).drop(col, axis = 1)).drop(0,axis = 1)


# Fix For Dates

def dict_to_date(Series):
    '''Takes in a Pandas Series of dicts with the format - {'day':X, 'month':Y, 'year':Z}
    and converts them into a Pandas Series of Python date objects.'''
    dates = []
    for dicts in Series:
        if type(dicts) != dict:
            #print('nan')
            dates.append(np.nan)
        
        else:
            i = 0
            while i < 3:
                my_lst = []
                
                for v in dicts.values():
                    my_lst.append(v)
                    i+=1
            date = dt.datetime(year = my_lst[-1],month = my_lst[1], day = my_lst[0])
            dates.append(date)
    
    return(pd.Series(dates))


def to_mongo(database, collection, df):
    '''Takes a dataframe and uploads it to a pre-existing MongoDB collection.
    Dates need to be converted to string.'''
    
    db = client[database]
    coll = db[collection]
    
    df.reset_index(drop = True, inplace = True)
    coll.insert_many(df.to_dict('records'))


profile_fields=cleaningProfileData()

#parsing required tables
profile_df = profile_fields[['profile_id','public_identifier','first_name','last_name',
                             'occupation','headline','summary','country_full_name','recommendations']]

profile_df.recommendations.replace([],None, inplace = True)

def cleanRecommendations(profile_fields):
    try:
       #d.x = d.x.apply(lambda y: np.nan if len(y)==0 else y)
       profile_df.recommendations = profile_df.recommendations.apply(lambda y: np.nan if len(y) == 0 else y)
       profile_df.reset_index(drop = True,inplace = True)
       #to_mongo('Linkedin','profile_data',profile_df)
    except TypeError:
        print('eror occured while cleaning recommendations')

def cleanExperience(profile_fields):
    #experiece table
    experience_df = linkedin_col_parser(profile_fields,'profile_id','experiences')
    
    experience_df.starts_at = dict_to_date(experience_df.starts_at)
    experience_df.ends_at = dict_to_date(experience_df.ends_at)

    #reading required columns 
    experience_df = experience_df[['profile_id','starts_at', 'ends_at','title', 'description',
                                     'company', 'location']]
    #frame[‘DataFrame Column’]= frame[‘DataFrame Column’].apply(str)
    experience_df.starts_at = experience_df.starts_at.apply(str)
    experience_df.ends_at = experience_df.ends_at.apply(str)

def cleanEducation(profile_fields):
   #3 education
   education_df = linkedin_col_parser(profile_fields,'profile_id','education')
   education_df.starts_at = dict_to_date(education_df.starts_at)
   education_df.ends_at = dict_to_date(education_df.ends_at)
   #reading required columns
   education_df = education_df[['profile_id','starts_at','ends_at','field_of_study','degree_name',
                             'school','description']]
   
   
   education_df.starts_at = education_df.starts_at.apply(str)
   education_df.ends_at = education_df.ends_at.apply(str)
   #to_mongo('Linkedin','education_data',education_df)


#accomplishments
def cleanAccompliashments(profile_fields):
   ac_organisation_df = linkedin_col_parser(profile_fields,'profile_id',
                                         'accomplishment_organisations')
   ac_organisation_df.starts_at = dict_to_date(ac_organisation_df.starts_at)
   ac_organisation_df.ends_at = dict_to_date(ac_organisation_df.ends_at)
   ac_organisation_df = ac_organisation_df[['profile_id', 'starts_at', 'ends_at','title',
                                         'org_name','description']]
   ac_organisation_df.loc[15:35]
   ac_organisation_df.starts_at = ac_organisation_df.starts_at.apply(str)
   ac_organisation_df.ends_at = ac_organisation_df.ends_at.apply(str)
   #to_mongo('Linkedin','ac_organisation',ac_organisation_df)


def cleanPublication(profile_fields):
   ac_publication_df = linkedin_col_parser(profile_fields,'profile_id',
                                        'accomplishment_publications')
   
  
   ac_publication_df.published_on = ac_publication_df.published_on.apply(str)
   #to_mongo('Linkedin','ac_publication',ac_publication_df)

def cleanHonors(profile_fields):
    ac_award_df = linkedin_col_parser(profile_fields,'profile_id',
                                 'accomplishment_honors_awards')
    ac_award_df.issued_on = dict_to_date(ac_award_df.issued_on)
   
    ac_award_df.issued_on = ac_award_df.issued_on.apply(str)
     #to_mongo('Linkedin','ac_award',ac_award_df)

#patents
def cleanPatents(profile_df):
    ac_patent_df = linkedin_col_parser(profile_df,'profile_id',
                                 'accomplishment_patents')
    ac_patent_df.issued_on = dict_to_date(ac_patent_df.issued_on)
   
   
    ac_patent_df.issued_on = ac_patent_df.issued_on.apply(str)
   #to_mongo('Linkedin','ac_patent',ac_patent_df)


#course
def cleanCourses(profile_fields):
    ac_course_df = linkedin_col_parser(profile_fields,'profile_id',
                                   'accomplishment_courses')
   


#9.Projects 
def cleanProjects(profile_fields):
    ac_project_df = linkedin_col_parser(profile_fields,'profile_id',
                                   'accomplishment_projects')
    ac_project_df.starts_at = dict_to_date(ac_project_df.starts_at)
    ac_project_df.ends_at = dict_to_date(ac_project_df.ends_at)
    

  
    ac_project_df.starts_at = ac_project_df.starts_at.apply(str)   
    ac_project_df.ends_at = ac_project_df.ends_at.apply(str)
   #to_mongo('Linkedin','ac_project',ac_project_df)


#10. test scores

def cleanCertification(profile_fields):
    ac_test_df = linkedin_col_parser(profile_fields,'profile_id',
                              'certifications')
    ac_test_df.starts_at = dict_to_date(ac_test_df.starts_at)
    ac_test_df.ends_at = dict_to_date(ac_test_df.ends_at)
    print(ac_test_df.loc[10:20])

   
    ac_test_df.starts_at = ac_test_df.starts_at.apply(str)
    ac_test_df.ends_at = ac_test_df.ends_at.apply(str)
    #to_mongo('Linkedin','ac_test',ac_test_df)

def createTables():
    cleanRecommendations(profile_fields)
    cleanExperience(profile_fields)
    cleanEducation(profile_fields)
    cleanAccompliashments(profile_fields)
    cleanPublication(profile_fields)
    cleanPatents(profile_fields)
    cleanProjects(profile_fields)
    cleanCourses(profile_fields)
    cleanCertification(profile_fields)
    



