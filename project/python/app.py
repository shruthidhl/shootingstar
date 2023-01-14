from flask import Flask, render_template, request,jsonify
import json
from flask.wrappers import Response
import pickle
from cleanjsondata import CleanJsonData
import creatingdbtables
import textcleaning
import mlmodel
import nltk 
nltk.download('stopwords')
#import evaluate
from configparser import SafeConfigParser
import codecs

#Initialize the flask App
app = Flask(__name__)

#model = pickle.load(open('model.pkl', 'rb'))


#index page of our web-app
@app.route('/')
def index():
    return render_template("index.html")  

# page displaying selectedroles
@app.route('/role', methods=['GET', 'POST'])
def selectRoles():
    message = ""
    parser = SafeConfigParser()
    with codecs.open('C:/Users/Dell/Documents/GitHub/big-data-programming-april2021-group-5/project/python/app.ini', 'r', encoding='utf-8') as f:
        parser.read_file(f)
    path=parser['model']['path']

    if request.method == 'POST':
        selectedRole= request.form.get('selectRole')        
        if selectedRole == '1':           
            message = "developer selected"
            CleanJsonData.cleanJsonData()
            creatingdbtables.createTables()
            mega_text=['jain university bangalore software developer breathbit intern tata consultancy services campus ambassador entrepreneurship cell iit kharagpur information technology btech bachelor python programming language microsoft word c public speaking breathbit experienced campus ambassador non profit organization management industry skilled breathbit software developer btech bachelor information technology software developer java strong education professional technology focused technology demonstrated history working']
            
            mlmodel.modelBuilding()
            model=''
            
            with open(path+'/naivebayes.pkl', 'rb') as f:
                 model = pickle.load(f)
            #    model = pickle.load(open('C:/Users/Dell/Documents/GitHub/big-data-programming-april2021-group-5/project/python/naivebayes.pkl', 'rb'))
            prediction = model.predict(mega_text)
            print(prediction)
         
        elif selectedRole=='3':
            message = " Solution Architect "
            CleanJsonData.cleanJsonData()
    print('message', message)
    return render_template("message.html", download_message=message)  

    
if __name__ == "__main__":
    app.run(debug=True, port=8080)
