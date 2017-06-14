# -*- coding: utf-8 -*-
# @Author: danda
# @Date:   2017-06-09 21:09:21
# @Last Modified by:   danda
# @Last Modified time: 2017-06-09 21:16:49

from sys import argv
from gensim.corpora import WikiCorpus

if __name__ == '__main__':
    wiki = WikiCorpus(argv[1])
    output_file = open(argv[2], 'w')
    for text in wiki.get_texts():
        output_file.write(b' '.join(text).decode('utf-8') + '\n')
    output_file.close()
