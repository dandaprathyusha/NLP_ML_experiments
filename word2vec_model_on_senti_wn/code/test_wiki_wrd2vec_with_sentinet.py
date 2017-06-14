# -*- coding: utf-8 -*-
# @Author: danda
# @Date:   2017-06-09 23:04:48
# @Last Modified by:   danda
# @Last Modified time: 2017-06-10 09:53:05

from sys import argv
from nltk.corpus import wordnet
import gensim
from nltk.stem import WordNetLemmatizer
from operator import add
from functools import reduce


def wiki_wrd2vec_sentinet(wrd2vec_model):
    model = gensim.models.Word2Vec.load(wrd2vec_model)
    accuracies = list()
    for word, vocab_obj in model.wv.vocab.items():
        lemmas_of_synset = list()
        lemmas_of_similar_words = list()
        if len(wordnet.synsets(word)) is not 0:
            for synset in wordnet.synsets(word):
                lemmas_of_synset.append(synset.name().split(".")[0])
            set_lemmas_of_synset = set(lemmas_of_synset)
            similar_words_list = model.similar_by_word(word, topn=20)
            for similar_word in similar_words_list:
                lemmas_of_similar_words.append(similar_word[0])
            per_word_accuracy = len(set(lemmas_of_similar_words) & set_lemmas_of_synset)/len(lemmas_of_synset)
            accuracies.append(per_word_accuracy)
            print("This is per_word_accuracy", per_word_accuracy, word)
            accuracy = reduce(add, accuracies)/len(accuracies)
            print("Accuracy", accuracy)



if __name__ == '__main__':
    wiki_wrd2vec_sentinet(argv[1])

