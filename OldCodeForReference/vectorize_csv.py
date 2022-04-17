import pandas as pd
import numpy as np

from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from tqdm import tqdm
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn import utils

# df = pd.read_csv("/home/utkarsh/PycharmProjects/androidMalwareDetectionUsingNLP/appData/dex2CSV_Files/XML.csv")
#/home/utkarsh/Malware_Analysis/PycharmProjects/androidMalwareDetectionUsingNLP/appData/
data = pd.read_csv("/home/utkarsh/Malware_Analysis/PycharmProjects/androidMalwareDetectionUsingNLP/appData/dex2CSV_Files/Hex.csv")

# data = DataFrame()
# data['label'] = df['label']
# data['strings'] = df['file_content']

print(data.head())


def tag_documents(corpus, label):
    tagged = []
    for i, v in enumerate(corpus):
        tag = label + '_' + str(i)
        # print(v.split())
        tagged.append(TaggedDocument(v.split(), [tag]))
    return tagged


X_train, X_test, y_train, y_test = train_test_split(data.file_content, data.label, random_state=0, test_size=0.2)
# X_train, X_test, y_train, y_test = train_test_split(data.strings, data.label, random_state=0, test_size=0.2)

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

X_train = tag_documents(X_train, 'Train')
X_test = tag_documents(X_test, 'Test')

all_data = X_train + X_test
data = None

model_dbow = Doc2Vec(dm=1, vector_size=300, negative=5, min_count=1, alpha=0.065, min_alpha=0.065)
model_dbow.build_vocab([x for x in tqdm(all_data)])
# model_dbow.train(utils.shuffle([x for x in tqdm(all_data)]), total_examples=len(all_data), epochs=30)
for epoch in range(30):
    model_dbow.train(utils.shuffle([x for x in tqdm(all_data)]), total_examples=len(all_data), epochs=1)
    model_dbow.alpha -= 0.002
    model_dbow.min_alpha = model_dbow.alpha


def retrieve_vectors(doc2vec_model, corpus_size, vectors_size, vector_type):
    vectors = np.zeros((corpus_size, vectors_size))
    for i in range(0, corpus_size):
        prefix = vector_type + '_' + str(i)
        vectors[i] = doc2vec_model.dv[prefix]
    return vectors


train_vectors_dbow = retrieve_vectors(model_dbow, len(X_train), 300, 'Train')
test_vectors_dbow = retrieve_vectors(model_dbow, len(X_test), 300, 'Test')

model = LogisticRegression()
model = model.fit(train_vectors_dbow, y_train)
model_pred = model.predict(test_vectors_dbow)

print('Accuracy %s' % accuracy_score(model_pred, y_test))
print(classification_report(y_test, model_pred))
