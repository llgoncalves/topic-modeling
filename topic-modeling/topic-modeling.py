#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from sklearn.decomposition import NMF
from itertools import groupby
from collections import Counter
import sys
import heapq
import string
import argparse

import numpy as np
import operator
import nltk
nltk.download('stopwords')


class TopicModeling(object):
    def __init__(self, filename, numTopics):
        self.filename = filename
        self.method = method
        self.stemmer = stemmer = LancasterStemmer()
        self.cachedStopWords = stopwords.words("english")
        self.content = None
        self.content_stem = []
        self.word_map_count = None
        self.word_map = None
        self.word_count_matrix = []
        self.word_count = None
        self.word_count_vector = None
        self.num_topics = numTopics

    def __normalize(self, array):
        arrayNorm = [0] * len(array)
        sumTotal = sum(array)

        if (sumTotal > 0):
            for value in array:
                norm = float(value) / float(sumTotal)
                arrayNorm.append(norm)

        return arrayNorm

    def __unique_words(self, l):
        ulist = []
        [ulist.append(x) for x in l if x not in ulist]
        return ulist

    def preprocessing(self):
        print("Preprocessing...")

        try:
            file = open(self.filename)
        except IOError:
            sys.stdout.write("File doesn't exist!\n")
            exit()

        self.content = file.read()
        content = ' '.join(
            [word for word in self.content.split() if word not in self.cachedStopWords])

        table = str.maketrans('', '', string.punctuation)
        self.content = self.content.translate(table)
        self.content = self.content.split()

        for word in self.content:
            self.content_stem.append(self.stemmer.stem(word))

        self.word_map_count = Counter(self.content_stem)
        self.word_map = self.__unique_words(self.content_stem)

        file.close()

        with open(self.filename) as file:

            for paragraph in file:

                paragraph = ' '.join(
                    [word for word in paragraph.split() if word not in self.cachedStopWords])
                table = str.maketrans('', '', string.punctuation)
                paragraph = paragraph.translate(table)
                paragraph = paragraph.split()

                paragraph_stem = []

                for word in paragraph:
                    paragraph_stem.append(self.stemmer.stem(word))

                self.word_count = Counter(paragraph_stem)

                self.word_count_vector = [0] * len(self.word_map)

                for k in self.word_count.keys():
                    self.word_count_vector[self.word_map.index(
                        k)] = self.word_count[k]

                self.word_count_matrix.append(self.word_count_vector)

    def lda(self):
        print("Running LDA...")

    def nmf(self):
        print("Running NMF...")
        nmf = NMF(n_components=self.num_topics, init='random', random_state=0)
        w_matriz = nmf.fit_transform(np.matrix(self.word_count_matrix))
        h_matriz = nmf.components_

        w_matrix_norm = []

        for w_array in w_matriz.T:
            w_matrix_norm.append(self.__normalize(w_array))

        w_matrix_norm = np.matrix(w_matrix_norm)

        h_matrix_norm = []

        for h_array in h_matriz:
            h_matrix_norm.append(self.__normalize(h_array))

        h_matrix_norm = np.matrix(h_matrix_norm)

        Gw = np.zeros((self.num_topics, self.num_topics))

        for i in range(self.num_topics):
            for j in range(self.num_topics):
                sumKT = 0

                for k in range(len(w_matrix_norm.A[i])):
                    sumKT = sumKT + (w_matrix_norm[i, k] * w_matrix_norm[j, k])

                Gw[i, j] = sumKT

        Gh = np.zeros((self.num_topics, self.num_topics))

        for i in range(self.num_topics):
            for j in range(self.num_topics):
                sumKT = 0

                for k in range(len(h_matrix_norm.A[i])):
                    sumKT = sumKT + (h_matrix_norm[i, k] * h_matrix_norm[j, k])

                Gh[i, j] = sumKT

        G = np.zeros((self.num_topics, self.num_topics))

        for i in range(self.num_topics):
            for j in range(self.num_topics):
                G[i, j] = Gw[i, j] + Gh[i, j]

        print(G)


def main(filename, method, numTopics):
    tm = TopicModeling(filename, numTopics)
    tm.preprocessing()

    if (method == "lda"):
        tm.lda()
    else:
        tm.nmf()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs=1, type=str,
                        help="Input the filename")

    parser.add_argument("-a", nargs=1, default="nmf", type=str,
                        choices=["lda", "nmf"],
                        help="Choose LDA or NMF algorithm (default: nmf).")

    parser.add_argument("-t", nargs=1, default=5, type=int,
                        help="Set the number of topics (default: 5).")

    args = parser.parse_args()
    filename = args.filename[0]
    method = args.a
    numTopics = args.t

    main(filename, method, numTopics)
