from sys import argv
import os
from bs4 import BeautifulSoup

'''
given folder containing html files, output text files with content in them
'''


def processing_crawled_data(input_folder_dest, output_folder_dest):
    for file in os.listdir(input_folder_dest):
        h = ''
        html_file = input_folder_dest + file
        with open(html_file, encoding="utf-8") as html_f:
            html_doc = html_f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        h += soup.get_text()
        f = open(os.path.join(output_folder_dest, file.split('.')[0] + '.txt'), 'w')
        f.write(h)


if __name__ == '__main__':
    processing_crawled_data(argv[1], argv[2])