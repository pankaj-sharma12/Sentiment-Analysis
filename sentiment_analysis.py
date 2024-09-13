# -*- coding: utf-8 -*-
"""Sentiment_Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1atAIsegx4RiNUjSBTQBYgJdWZZSSBOAU
"""

pip install kaggle

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/. kaggle/kaggle.json

!chmod 600 ./kaggle/kaggle.json

#Api to fetch the dataset from Kaggle
!kaggle datasets download -d kazanova/sentiment140

#extracting the compressed dataset
from zipfile import ZipFile
dataset= '/content/sentiment140.zip'

with ZipFile(dataset,'r') as zip:
  zip.extractall()
  print('The dataset is extracted')

#Importing the dependencies
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwards')

nltk.download('stopwords')

# printing the stopwords in english
print(stopwords.words('english'))

"""Data Processing"""

#loading the data from csv file to pandas dataframe
twitter_data=pd.read_csv('/content/training.1600000.processed.noemoticon.csv',encoding='ISO-8859-1')

twitter_data.shape

# priting the first 5 rows of dataframe
twitter_data.head()

#naming the columns and reading the dataset again
column_names=['target','id','data','flag','user','text']
twitter_data=pd.read_csv('/content/training.1600000.processed.noemoticon.csv',names=column_names,encoding='ISO-8859-1')

twitter_data.head()

twitter_data.shape

# COUNTING THE NO. OF MISSING VALUE OR TEXT IN THE DATASET
twitter_data.isnull().sum()

#checking the distribution of target columns
twitter_data['target'].value_counts()

"""Convert the target '4' to '1'"""

twitter_data.replace({'target':{4:1}},inplace=True)

twitter_data['target'].value_counts()

"""0--> Negative Tweet
1--> Positive Tweet

**STemming**

Stemming is the process of reducing a word to its Root word
Example: actor,actress,acting= act
"""

port_stem=PorterStemmer()

def stemming(content):
  stemmed_content=re.sub('[^a-zA-Z]',' ',content)
  stemmed_content=  stemmed_content.lower()
  stemmed_content=  stemmed_content.split()
  stemmed_content=[port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content=' '.join(stemmed_content)

  return   stemmed_content;

twitter_data['stemmed_content']=twitter_data['text'].apply(stemming);
print(twitter_data['stemmed_content'].head())

"""50 minutes to complete above execution"""

# seperating the data and label
X = twitter_data['stemmed_content'].values
Y =twitter_data['target'].values

print(X)

"""Splitting the data to training data and test data"""

X_train , X_test,Y_train , Y_test = train_test_split(X,Y,test_size=0.2,stratify = Y , random_state=2)

print(len(X_train))

print(X.shape,X_train.shape,X_test.shape)

# converting the textual data to numerical data

vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)

X_test= vectorizer.transform(X_test)

print(X_train)

print(X_test)

"""Training the Machine Learning Model


Logistic Regression -> used for classification types problems

"""

model=LogisticRegression(max_iter=1000)

model.fit(X_train,Y_train)

"""Model evaluation

Accuracy Score
"""

# accuracy score on the training data

X_train_predicton=model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train,X_train_predicton)

print("accuracy score on the training data : ",training_data_accuracy)

X_test_predicton=model.predict(X_test)
test_data_accuracy = accuracy_score(Y_test,X_test_predicton)
print("accuracy score on the test data : ",test_data_accuracy)

"""Model accuracy is 77.8%

Saving the trained Model
"""

import pickle

filename = 'trained_model.sav'
pickle.dump(model,open(filename,'wb'))

"""Using the saved model for future predictions"""

#Loading the saved model
loaded_model=pickle.load(open('/content/trained_model.sav','rb'))

X_new = X_test[200]
print(Y_test[200])
prediction = model.predict(X_new)
print(prediction)
if (prediction[0]==0):
   print("negative tweet")
else:
   print("Postive Tweet")

