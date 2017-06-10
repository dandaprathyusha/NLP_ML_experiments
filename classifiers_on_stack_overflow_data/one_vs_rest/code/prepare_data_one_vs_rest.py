from sys import argv
import os
from sklearn.model_selection import train_test_split
from collections import defaultdict

'''
Prepare one vs rest data,
arg1 - give datafile; it contains label and text, tab separated, in that order.
arg2 - destination folder to write train files and a test file
'''


def prepare(data_file, path_to_write):
    f = open(data_file).read()
    label_data_list = f.split('\n')
    label_list = [i.split('\t')[0] for i in label_data_list]
    data_list = [i.split('\t')[1] for i in label_data_list]
    label_data_dict = defaultdict(list)
    X_train, X_test, y_train, y_test = train_test_split(data_list, label_list, test_size=0.10, random_state=42)

    for num, label_item in enumerate(y_train):
        label_data_dict[label_item].append(X_train[num])

    test_f = open('test.txt', 'w')

    for num, data in enumerate(y_test):
        test_f.write(str(data) + '\t' + str(X_test[num]) + '\n')

    for label_list_item in list(set(y_train)):
        f = open(os.path.join(path_to_write, str(label_list_item) + '.txt'), 'w')
        for key, value in label_data_dict.items():
            if key == label_list_item:
                for item in value:
                    f.write(str(key) + '\t' + str(item) + '\n')
            else:
                for item in value:
                    f.write('21' + '\t' + str(item) + '\n')


if __name__ == '__main__':
    prepare(argv[1], argv[2])
