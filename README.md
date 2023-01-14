# shootingstar

Note : For reading api.ini configuration file, it's absolute path is being used as code was not finding file in windows machine though it is in same project folder,
please replace the path by your computer absolute path or by just by the file name**




1.	In this project  An excel sheet with Linked Profile urls to be scrapped  is read and urls are cleaned and written back to an excel sheet
2.	Proxy curl api  is called for data collection from LinkedIn ,it's a onetime call wherein we call proxy curl api for fetching all the LinkedIn profiles that we have 

3.	Data collection process is done in file dataCollectionfrpmProcyCurlApi.py.Data  in JSON format is stored to Mongodb using code in dataCollectionfrpmProcyCurlApi
JSON data is then fetched, cleaned and stored back to db using file cleanjsondata.py

4.	Data is read from Mongodb and cleaned for Individual fields such as profile data, experiences, accomplishments, patents, courses Data from above step is stored as 
separate collections in Mongodb  by using code in file creatingdbtables.py

5.	Data is then read from these collections in cleantext.py file and then all the individual criteria texts are cleaned and merged to create mega text for text analysis 

6.	Model is built in file mlmodel.py and model is written in binary form to naivebayers.pkl for developers and to naivebayers_architect.pkl for architects’ model will predict 1 for selected candidate and 0 for not selected 


7.	 When model predicts 1, evaluate.py file is executed and it has selenium code to automatically navigate go to page where Candidate profile has to be uploaded

8.	Idea was to write all candidates who got selected to and excel sheet with their email id, first name and last name and then upload this file by verifying details manual

9.	Add pre-set test(each test will have individual timings and if time is completed will close) created in the evaluation process , set date in which test should be completed and click on send button

10.	Candidates will receive email, writes test and will click on finish and results will be available in portal once candidates finishes . This is for developer 

11.	For Architects there no programming test created and only email is sent for 1 hour face to face interview







