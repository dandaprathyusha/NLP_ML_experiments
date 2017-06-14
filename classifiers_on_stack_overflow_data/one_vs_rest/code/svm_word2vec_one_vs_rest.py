# -*- coding: utf-8 -*-
# @Author: Prathyusha Danda
# @Date:   2017-06-14 10:56:14
# @Last Modified by:   Prathyusha Danda
# @Last Modified time: 2017-06-14 13:47:39

import numpy as np
import os
import time
import random
import gensim
from sys import argv
from collections import defaultdict
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC



def wrdvec_and_padding(X_list, w2v, max_len_sent, word_vec_length):
    X_list_wrd2vec = list()
    for sent in X_list:
        wrdvec_of_sent = []
        for token in sent:
            if token.decode('utf-8') not in w2v:
                wrdvec_of_sent.append(word_vec_length*[0])
            else:
                wrdvec_of_sent.append(w2v[token.decode('utf-8')])
        if len(wrdvec_of_sent) < max_len_sent:
            pad_vector = word_vec_length*[0]
            pad_vectors_list = [pad_vector for i in range(max_len_sent - len(wrdvec_of_sent))]
            wrdvec_of_sent = wrdvec_of_sent + pad_vectors_list
        flat_wrdvec_of_sent= [item for sublist in wrdvec_of_sent for item in sublist]
        X_list_wrd2vec.append(flat_wrdvec_of_sent)
    print(len(X_list_wrd2vec), 'loooll')
    return(X_list_wrd2vec)


def nb_word2vec_one_vs_rest(word2vec_model, test_file, input_folder_dest, output_folder_dest):

    model = gensim.models.Word2Vec.load(word2vec_model)
    w2v = dict(zip(model.wv.index2word, model.wv.syn0))

    '''
    reading test file
    '''
    test_data_label_list = open(test_file).read().split('\n')
    test_data_label_list = list(filter(None, test_data_label_list))
    test_label = [i.split('\t')[0] for i in test_data_label_list]
    test_data = [i.split('\t')[1] for i in test_data_label_list]
    test_data_tokenised = [gensim.corpora.wikicorpus.tokenize(i) for i in test_data]

    for file in os.listdir(input_folder_dest):
        data_label = open(os.path.join(input_folder_dest, file)).read().split('\n')

        '''
        reading data file, give 1 for class and -1 label for rest
        '''

        data_label = list(filter(None, data_label))
        label_list = [i.split('\t')[0] for i in data_label]
        data_list = [i.split('\t')[1] for i in data_label]
        data_list_tokenised = [gensim.corpora.wikicorpus.tokenize(i) for i in data_list]
        X_train = data_list_tokenised
        y_train = list()
        for item in label_list:
            if item == '21':
                y_train.append(-1)
            else:
                y_train.append(1)

        '''
        taking only test samples belonging to current class, to know class classification accuracy
        '''

        y_test = list()
        X_test = list()
        for i in range(len(test_label)):
            if test_label[i] == str(file.split('.')[0]):
                y_test.append(1)
                X_test.append(test_data_tokenised[i])
        X_train_wrd2vec = list()
        X_test_wrd2vec = list()
        list_train_test_data = X_train + X_test
        max_len_sent = max(len(list_elem) for list_elem in list_train_test_data)
        random_key, random_value = random.choice(list(w2v.items()))
        word_vec_length = len(random_value)
        train_list_sent_wrd2vec = wrdvec_and_padding(X_train, w2v, max_len_sent, word_vec_length)
        test_list_sent_wrd2vec = wrdvec_and_padding(X_test, w2v, max_len_sent, word_vec_length)
        '''
        Count vectorizer and tf-idf features
        '''
        '''
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        X_new_counts = count_vect.transform(X_test)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        '''



        X_train_wrd2vec = np.array(train_list_sent_wrd2vec)
        print(X_train_wrd2vec.shape)
        X_test_wrd2vec = np.array(test_list_sent_wrd2vec)
        print(X_test_wrd2vec.shape)
        clf = LinearSVC(random_state=0).fit(X_train_wrd2vec, y_train)
        start = time.process_time()
        predicted = clf.predict(X_test_wrd2vec)
        end = time.process_time()

        ''''
        Writing time and accuracy into output file
        '''

        f = open(os.path.join(output_folder_dest, file.split('.')[0] + '_time_acc_out.txt'), 'w')
        f.writelines(['NB time   ', str(end-start), '\n'])
        f.writelines(['NB Accuracy   ', str(np.mean(predicted == y_test)), '\n'])
        f.write(metrics.classification_report(y_test, predicted, target_names=list(set(label_list))))
        f.close()
        print(clf.classes_)

        '''
        Probabilities of classes
        with open(os.path.join(output_folder_dest, file.split('.')[0] + '_out.txt'), 'wb') as g:
            np.savetxt(g, clf.predict_proba(X_new_tfidf), fmt='%.3f')
        '''

if __name__ == '__main__':
    nb_word2vec_one_vs_rest(argv[1], argv[2], argv[3], argv[4])