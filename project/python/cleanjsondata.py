import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
import requests
import datetime as dt

import codecs

class CleanJsonData:
 #Takes in a Pandas Series of dicts with the format - {'day':X, 'month':Y, 'year':Z}
 #and converts them into a Pandas Series of Python date objects.'''
  def dict_to_date(Series):
    dates = []
    for dicts in Series:
        if type(dicts) != dict:
            #print('nan')
            dates.append(None)
        
        else:
            i = 0
            while i < 3:
                my_lst = []
                
                for v in dicts.values():
                    my_lst.append(v)
                    i+=1
            date = dt.date(year = my_lst[-1],month = my_lst[1], day = my_lst[0])
            dates.append(date)   
    return(pd.Series(dates))


  def cleanJsonData():
        #client = MongoClient('mongodb://127.0.0.1:27017/')
        conn = "mongodb+srv://jaiahujaa:Jaiahuja9$@cluster0.ehbij.mongodb.net/test"
        client = MongoClient(conn)
        db = client["Linkedin"]

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        linkdedInProfile = db['Linkedin_Profiles']

        #loading data as dataframe
        test = pd.DataFrame(list(linkdedInProfile.find()))


        profile_fields = test[['_id','public_identifier','first_name','last_name','occupation','headline',
                    'summary','country_full_name','city','experiences','education','languages',
                    'accomplishment_organisations','accomplishment_publications',
                    'accomplishment_honors_awards','accomplishment_patents',
                    'accomplishment_courses','accomplishment_projects', 'accomplishment_test_scores',
                    'volunteer_work', 'certifications','connections','recommendations']]

        #remove missing data
        profile_fields.dropna(thresh = 15, inplace = True)

        profile_fields.reset_index(drop = True, inplace =True)

        # INSERTING PROFILE_ID COLUMN
        profile_fields.insert(0, 'profile_id', range(0,len(profile_fields)))

        #parsing experience clumn
        experience_df = profile_fields[['profile_id','experiences']]
        experience_df.reset_index(drop = True, inplace = True)
        experience_df = experience_df.explode('experiences')
        experience_df.reset_index(drop = True, inplace = True)
        experience_df_2 = experience_df['experiences'].apply(pd.Series)
        experience_df_final = pd.concat([experience_df, experience_df_2], axis = 1).drop('experiences', axis = 1)
        experience_df_final.drop(columns = [0,'logo_url','company_linkedin_profile_url'],axis = 1, inplace = True)

        # Rearranging the columns
        print(experience_df_final.columns)

        experience_df_final = experience_df_final[['profile_id','starts_at', 'ends_at',
                                                    'title', 'description',
                                                    'company', 'location']]


        experience_df_final.starts_at = CleanJsonData.dict_to_date(experience_df_final.starts_at)
        experience_df_final.ends_at = CleanJsonData.dict_to_date(experience_df_final.ends_at)
        print(experience_df_final)
        print('cleaning file')
        return experience_df_final


