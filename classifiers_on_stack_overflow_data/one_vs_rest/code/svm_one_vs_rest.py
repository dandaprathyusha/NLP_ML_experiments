import numpy as np
import os
import time
from sys import argv
from collections import defaultdict
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC


def nb_one_vs_rest(test_file, input_folder_dest, output_folder_dest):

    '''
    reading test file
    '''
    test_data_label_list = open(test_file).read().split('\n')
    test_data_label_list = list(filter(None, test_data_label_list))
    test_label = [i.split('\t')[0] for i in test_data_label_list]
    test_data = [i.split('\t')[1] for i in test_data_label_list]

    test_dict = defaultdict(list)
    for num, test_label_item in enumerate(test_label):
        test_dict[test_label_item].append(test_data[num])

    for file in os.listdir(input_folder_dest):
        data_label = open(os.path.join(input_folder_dest, file)).read().split('\n')

        '''
        reading data file, give 1 for class and -1 label for rest
        '''

        data_label = list(filter(None, data_label))
        label_list = [i.split('\t')[0] for i in data_label]
        data_list = [i.split('\t')[1] for i in data_label]
        X_train = data_list
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
                X_test.append(test_data[i])


        '''
        Count vectorizer and tf-idf features
        '''
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        X_new_counts = count_vect.transform(X_test)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        clf = LinearSVC(random_state=0).fit(X_train_tfidf, y_train)
        start = time.process_time()
        predicted = clf.predict(X_new_tfidf)
        end = time.process_time()

        ''''
        Writing time and accuracy into output file
        '''

        f = open(os.path.join(output_folder_dest, file.split('.')[0] + '_time_acc_out.txt'), 'w')
        f.writelines(['SVM time   ', str(end-start), '\n'])
        f.writelines(['SVM Accuracy   ', str(np.mean(predicted == y_test)), '\n'])
        f.write(metrics.classification_report(y_test, predicted, target_names=list(set(label_list))))
        f.close()
        print(clf.classes_)

        '''
        Probabilities of classes
        with open(os.path.join(output_folder_dest, file.split('.')[0] + '_out.txt'), 'wb') as g:
            np.savetxt(g, clf.predict_proba(X_new_tfidf), fmt='%.3f')
        '''

if __name__ == '__main__':
    nb_one_vs_rest(argv[1], argv[2], argv[3])