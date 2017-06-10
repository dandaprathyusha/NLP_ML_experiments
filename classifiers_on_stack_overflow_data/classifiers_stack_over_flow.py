import numpy as np
import time
from sys import argv
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.cluster import KMeans
from sklearn.svm import LinearSVC


'''
Take data file and label file as input
'''
data_list = open(argv[1]).read().split('\n')
label_list = open(argv[2]).read().split('\n')

'''
Split the data into train and test; split 90-10
'''
X_train, X_test, y_train, y_test = train_test_split(data_list, label_list, test_size=0.10, random_state=42)
'''
Count vectorizer and then get tf-idf features
'''
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

'''
Training a Naive Bayes Classfier
'''

clf = MultinomialNB().fit(X_train_tfidf, y_train)
#print(X_train_tfidf.shape)

'''
Test data, accuracy and confusion matrix
'''
docs_new = X_test
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
#print(X_new_tfidf.shape)
start = time.process_time()
predicted = clf.predict(X_new_tfidf)
end = time.process_time()
'''
for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, category))

'''
print('NB time', end-start)
print('NB Accuracy', np.mean(predicted == y_test))
print(metrics.classification_report(y_test, predicted, target_names=list(set(label_list))))
print('Confusion Matrix', metrics.confusion_matrix(y_test, predicted))


'''
OnevsRest
'''

clf_1 = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X_train_tfidf, y_train)
start = time.process_time()
predicted_1 = clf_1.predict(X_new_tfidf)
end = time.process_time()
'''
for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, category))
'''

print('OnevsRest Time', end-start)
print('OnevsRest Accuracy', np.mean(predicted_1 == y_test))
print(metrics.classification_report(y_test, predicted_1, target_names=list(set(label_list))))
print('Confusion Matrix', metrics.confusion_matrix(y_test, predicted_1))


'''
OnevsOne
'''

clf_2 = OneVsOneClassifier(LinearSVC(C=100.)).fit(X_train_tfidf, y_train)
start = time.process_time()
predicted_2 = clf_2.predict(X_new_tfidf)
end = time.process_time()

print('OnevsOne Time', end-start)
print('OnevsOne Accuracy', np.mean(predicted_2 == y_test))
print(metrics.classification_report(y_test, predicted_2, target_names=list(set(label_list))))
print('Confusion Matrix', metrics.confusion_matrix(y_test, predicted_2))

'''
SGD
'''

clf_3 = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, y_train)

start = time.process_time()
predicted_3 = clf_3.predict(X_new_tfidf)
end = time.process_time()
print('SGD Time', end-start)
print('SGD Accuracy', np.mean(predicted_3 == y_test))
print(metrics.classification_report(y_test, predicted_3, target_names=list(set(label_list))))
print('Confusion Matrix', metrics.confusion_matrix(y_test, predicted_3))

'''
K means


clf_4 = KMeans(n_clusters=20, random_state=0).fit(X_train_tfidf)
start = time.process_time()
predicted_4 = clf_4.predict(X_new_tfidf)
end = time.process_time()
y_test = list(map(int, y_test))
print('KMeans Time', end-start)

print(len(y_test), len(predicted_4))
print('KMeans Accuracy', np.mean(predicted_4 == y_test))
print(list(set(label_list)))
print(metrics.classification_report(y_test, predicted_4, target_names=list(set(label_list))))
print('Confusion Matrix', metrics.confusion_matrix(y_test, predicted_4))
'''