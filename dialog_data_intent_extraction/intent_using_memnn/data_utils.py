from __future__ import absolute_import

import os
import re
import numpy as np


def load_task(data_dir, task_id, only_supporting=False):
    '''Load the nth task. There are 20 tasks in total.

    Returns a tuple containing the training and testing data for the task.
    '''
    assert task_id > 0 and task_id < 21

    files = os.listdir(data_dir)
    files = [os.path.join(data_dir, f) for f in files]
    s = 'dialog-babi-task{}-'.format(task_id)
    train_file = [f for f in files if s in f and 'te-trn' in f][0]
    test_file = [f for f in files if s in f and 'te-tst' in f][0]
    train_data = get_stories(train_file, only_supporting)
    test_data = get_stories(test_file, only_supporting)
#    print(train_data)
    return train_data, test_data

'''
def all_candidate_responses(data_dir, word_idx):
    files = os.listdir(data_dir)
    files = [os.path.join(data_dir, f) for f in files]
    q = 'dialog-babi-candidates'
    all_candidate_responses_file = [f for f in files if q in f][0]
    question_list = list()
    QC = list()
    with open(all_candidate_responses_file) as f:
        for line in f.readlines():
            if 'api_call' in line:
                line = line.strip()
                line = str.lower(line)
                nid, line = line.split(' ', 1)
                q = tokenize(line)
                question_list.append(q)

                for i in range(len(q)):
                    if q[i] not in word_idx and q[i] is not 'api_call':
                        print(q[i],"heyyyyyyyyyyyyyyyy")
                        word_idx[q[i]] = len(word_idx)
    print(len(word_idx))
    for i in range(len(question_list)):
        y = np.zeros(len(word_idx) + 1)
        for j in range(len(question_list[i])):
            if question_list[i][j] is not 'api_call':
                y[word_idx[question_list[i][j]]] = 1
        QC.append(y)
#    for num, data in enumerate(question_list):
#        print("\n",num, data)
    return word_idx, np.array(QC), QC
'''


def tokenize(sent):
    '''Return the tokens of a sentence including punctuation.
    >>> tokenize('Bob dropped the apple. Where is the apple?')
    ['Bob', 'dropped', 'the', 'apple', '.', 'Where', 'is', 'the', 'apple', '?']
    '''
    return [x.strip() for x in re.split('(\W+)?', sent) if x.strip()]

def get_places():
    tokens_filename_f = open('/home/danda/research/memnet/tourist_data/train_creation_files/unique_places.txt', 'r')
    places_list = list()
    for line in tokens_filename_f.readlines():
        line = line.strip()
        places_list.append(line.lower())
    places_labels_list = []
    for num, data in enumerate(places_list):
        y = np.zeros(len(places_list))
        y[num] = 1
        places_labels_list.append(y)
    places_idx = dict((c, i) for i, c in enumerate(places_list))
    return places_idx, places_labels_list

def parse_stories(lines, only_supporting=False):
    '''Parse stories provided in the bAbI tasks format
    If only_supporting is true, only the sentences that support the answer are kept.
    '''
    data = []
    story = []
    '''
    cuisines = ['cantonese', 'korean', 'japanese', 'thai',
                'vietnamese', 'french', 'spanish', 'british', 'indian', 'italian']
    places = ['paris', 'seoul', 'tokyo', 'beijing', 'bangkok',
        'hanoi', 'rome', 'london', 'bombay', 'madrid','api_call']
        '''
    for line in lines:
        if line == '\n':
            continue
        line = line.strip()
        line = str.lower(line)
        nid, line = line.split(' ', 1)
        nid = int(nid)
        if nid == 1:
            story = []
        if 'api_call' in line:  # question
            q, a = line.split('\t')
            q = tokenize(q)
            a = tokenize(a)
            list_a = list()
            for word in a:
                if 'api_call' != word:
                    list_a.append(word)
            a = list_a
#            print(a)

            # answer is one vocab word even if it's actually multiple words
            # a = [a]
            substory = None

            # remove question marks
            if q[-1] == "api_call":
                q = q[:-1]

            if only_supporting:
                # Only select the related substory
                supporting = map(int, supporting.split())
                substory = [story[i - 1] for i in supporting]
            else:
                # Provide all the substories
                substory = [x for x in story if x]
            data.append((substory, q, a))
            story.append('')
        else:
            # regular sentence
            # remove periods
            sent_list = line.split("\t")
            sent_user = tokenize(sent_list[0])
            sent_system = tokenize(sent_list[1])
            if sent_user[-1] == ".":
                sent_user = sent_user[:-1]
            if sent_system[-1] == ".":
                sent_system = sent_system[:-1]
            story.append(sent_user)
            story.append(sent_system)
            '''
            sent_user = tokenize(line)
            if sent_user[-1] == ".":
                sent_user = sent_user[:-1]
            story.append(sent_user)
            print(story)
            '''
    return data


def get_stories(f, only_supporting=False):
    '''Given a file name, read the file, retrieve the stories, and then convert the sentences into a single story.
    If max_length is supplied, any stories longer than max_length tokens will be discarded.
    '''
    with open(f) as f:
        return parse_stories(f.readlines(), only_supporting=only_supporting)


def vectorize_data(data, word_idx, sentence_size, memory_size):
    """
    Vectorize stories and queries.

    If a sentence length < sentence_size, the sentence will be padded with 0's.

    If a story length < memory_size, the story will be padded with empty memories.
    Empty memories are 1-D arrays of length sentence_size filled with 0's.

    The answer array is returned as a one-hot encoding.
    """
    S = []
    Q = []
    A1 = []
    A2 = []
#    A3 = []
#    A4 = []

    places_idx, labels_places_list = get_places()
    print(places_idx)
    for story, query, answer in data:
        ss = []
        k = 0
        for i, sentence in enumerate(story, 1):
            ls = max(0, sentence_size - len(sentence))
            ss.append([word_idx[w] for w in sentence] + [0] * ls)

        # take only the most recent sentences that fit in memory
        ss = ss[::-1][:memory_size][::-1]

        # Make the last word of each sentence the time 'word' which
        # corresponds to vector of lookup table
        for i in range(len(ss)):
            ss[i][-1] = len(word_idx) - memory_size - i + len(ss)

        for i in range(len(ss)):
            if (i % 2) == 0:
                ss[i][-2] = 0
            else:
                ss[i][-2] = 1

        # pad to memory_size
        lm = max(0, memory_size - len(ss))
        for _ in range(lm):
            ss.append([0] * sentence_size)

        lq = max(0, sentence_size - len(query))
        q = [word_idx[w] for w in query] + [0] * lq

        y1 = np.zeros(len(places_idx))
        y2 = np.zeros(len(places_idx))
        # y1 = np.zeros(len(word_idx) + 1)  # 0 is reserved for nil word
        # y2 = np.zeros(len(word_idx) + 1)
#        y3 = np.zeros(len(word_idx) + 1)
#        y4 = np.zeros(len(word_idx) + 1)
#        print("\n",answer)

        y1[places_idx[answer[0]]] = 1
#        y2[places_idx[answer[1]]] = 1
#        y3[word_idx[answer[2]]] = 1
#        y4[word_idx[answer[3]]] = 1

        S.append(ss)
        Q.append(q)
        A1.append(y1)
#        A2.append(y2)
#        A3.append(y3)
#        A4.append(y4)

    return np.array(S), np.array(Q), np.array(A1)
    # np.array(A2)
    #, np.array(A3), np.array(A4)
