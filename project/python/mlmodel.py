from rake_nltk import Rake
rake_nltk_var = Rake()
import textcleaning
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import plot_confusion_matrix,classification_report
from sklearn.pipeline import Pipeline
import pickle
from textcleaning import TransformData
from configparser import SafeConfigParser
import codecs


def report(model,x_train_tfidf,x_test_tfidf,y_test):
    preds = model.predict(x_test_tfidf)
    print(classification_report(y_test,preds))
    plot_confusion_matrix(model,x_test_tfidf,y_test)

def modelBuilding():
    mega_text=textcleaning.textCleaning()
    i = 0
    for text in mega_text.text:
        rake_nltk_var.extract_keywords_from_text(text)
        keywords = rake_nltk_var.get_ranked_phrases()
        keywords = ' '.join(keywords)
        #print(keywords)
        mega_text.text.iloc[i] = keywords
        i+=1

    #creating model
    mega_text['selection'] =[1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,
    0,1,1,0,1,0,0,1,1,1,0,1,0,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0]

    y = mega_text['selection']
    x = mega_text['text']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=21)

    tfidf = TfidfVectorizer(stop_words='english')

    # Fitting the model
    tfidf.fit(x_train)

    x_train_tfidf = tfidf.transform(x_train)
    x_test_tfidf = tfidf.transform(x_test)

    x_train_tfidf.todense()

    nb = MultinomialNB()
    nb.fit(x_train_tfidf,y_train)

    #report(nb, x_train_tfidf,x_test_tfidf,y_test)

    #model predictions
    pipe = Pipeline([('tfidf',TfidfVectorizer()),('nb',MultinomialNB())])

    pipe.fit(mega_text['text'],mega_text['selection'])


    # Saving model to disk
    # Pickle serializes objects so they can be saved to a file, and loaded in a program again later on.
    parser = SafeConfigParser()

    with codecs.open('C:/Users/Dell/Documents/GitHub/big-data-programming-april2021-group-5/project/python/app.ini', 'r', encoding='utf-8') as f:
        parser.read_file(f)
    path=parser['model']['path']
    
    with open(path+'/naivebayes.pkl', 'wb') as f:
         pickle.dump(pipe, f)

    '''
    #Loading model to compare the results
    model = pickle.load(open('naivebayes.pkl','rb'))
    new_text = ['cloud ui aws python java', 'helllo PHP HTML Java',
            'design prototypes creating digital products gtworld mobile app private repository collaborated identify customer ’ client projects ranging usable experience responsibilities redesign design design design design development gtpay product company ’ technology product collaborated customers designed house operations success useful feedback']


    print(pipe.predict(new_text))

'''



