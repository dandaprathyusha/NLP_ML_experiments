# -*- coding: utf-8 -*-
# @Author: danda
# @Date:   2017-06-09 15:46:07
# @Last Modified by:   danda
# @Last Modified time: 2017-06-09 19:09:55

from sys import argv
import logging
from gensim import corpora
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


def word2vec_model(input_file, trained_model, word_vectors, saved_dictionary):
    list_of_documents = list(LineSentence(input_file))
    dictionary = corpora.Dictionary(list_of_documents)
    dictionary.save(saved_dictionary)
    model = Word2Vec(LineSentence(input_file), size=300, window=5, min_count=5)
    model.save(trained_model)
    model.wv.save_word2vec_format(word_vectors, binary=False)


if __name__ == '__main__':
    word2vec_model(argv[1], argv[2], argv[3], argv[4])
