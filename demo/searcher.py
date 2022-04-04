import numpy as np
import pymorphy2
import re
import nltk
from nltk.corpus import stopwords
from scipy import spatial
import json
import string

nltk.download('stopwords')
nltk.download('punkt')


class Searcher:
    def __init__(self):
        self.index_lemmas, self.lemmas = self.get_index_lemmas()
        self.matrix = self.get_matrix()

    # обработка контента (токенизация, удаление стоп-слов, знаков препинания)
    def tokenize(self, content):
        tokens_ = nltk.word_tokenize(content)
        tokens_ = [i.lower() for i in tokens_]
        tokens_ = [i for i in tokens_ if (i not in string.punctuation)]
        tokens_ = filter(None, [re.sub(r"[^a-zа-я-]+", r"", i) for i in tokens_])

        stop_words = stopwords.words('russian')
        stop_words.extend(['что', 'это', 'так', 'вот', 'как', 'в', 'к',
                           'на', 'о', 'при', 'из-за', 'за', 'ао', 'но', 'х',
                           'хотя', 'среди', 'помимо', 'с'])
        tokens_ = [i for i in tokens_ if (i not in stop_words)]

        stop_words2 = stopwords.words('english')
        stop_words2.extend(['the', 'e', 'a', 'd', 'b', 'x', 'c'])
        tokens_ = [i for i in tokens_ if (i not in stop_words2)]

        tokens_ = [i.replace("«", "").replace("»", "") for i in tokens_]

        return tokens_

    # создание матрицы по индексу лемм
    # строки - документы, столбцы - леммы, пересечения - существует ли данная лемма в данном документе
    def get_matrix_lemmas(self, index_lemmas):
        id = 0
        matrix = []
        for i in range(len(index_lemmas)):
            matrix.append([0] * 100)
        for k in index_lemmas:
            docs = index_lemmas[k][1]
            for doc in docs:
                matrix[id][int(doc) - 1] = 1
            id += 1
        return np.array(matrix).transpose()

    # создание вектора размером кол-ва лемм, значения которого 0 или 1 в зависимости от лемм поисковой фразы
    def get_vector_from_search_query(self, search):
        morph = pymorphy2.MorphAnalyzer()
        tokens = self.tokenize(search)
        lemmas_from_tokens = [morph.parse(token)[0].normal_form for token in tokens]
        vector = [0] * len(self.lemmas)
        for token in lemmas_from_tokens:
            if token in self.lemmas:
                vector[self.lemmas.index(token)] = 1
        return vector

    # Функция поиска: строки матрицы сравниваем с вектором через косинусное расстояние,
    # и записываем для каждого документа значение - степень сходства
    # чем ближе значение косинуса к 1, тем ближе угол к 0 градусам, то есть тем более похожи два вектора
    def search(self, search):
        vector = self.get_vector_from_search_query(search)
        docs = dict()
        for id, doc in enumerate(self.matrix):
            docs[id + 1] = spatial.distance.cosine(vector, doc)
        docs_ = dict(filter(lambda elem: elem[1] != 1.0 and elem[1] != 0, docs.items()))
        sorted_ = sorted(docs_.items(), key=lambda x: x[1])
        sorted_docs = []
        for item in sorted_:
            sorted_docs.append(item[0])
        return sorted_docs

    def get_input_file(self):
        with open('input.txt', encoding="utf-8") as file_:
            rows_ = [row.strip() for row in file_]
        input_files = {}
        for row in rows_:
            row = row.split(' ')
            input_files[row[0]] = row[1]
        return input_files

    def search_top(self, search_, count):
        docs = self.search(search_)
        return docs[:count]

    def get_links(self, docs):
        input_files = self.get_input_file()
        links = []
        for doc in docs:
            links.append(input_files[str(doc)])
        return links

    def get_index_lemmas(self):
        with open('inverted_index_lemmas.txt', encoding="utf-8") as file:
            rows = [row.strip() for row in file]

        index_lemmas = {}
        lemmas = list()
        for row in rows:
            row = row.replace('\'', '\"')
            dict_ = json.loads(row)
            lemmas.append(dict_["word"])
            index_lemmas[dict_["word"]] = [dict_["count"], dict_["inverted_array"]]
        return index_lemmas, lemmas

    def get_matrix(self):
        matrix = self.get_matrix_lemmas(self.index_lemmas)
        return matrix
