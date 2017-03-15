
# This program creates an inverted index for an
#input corups
from nltk import word_tokenize
from nltk.util import ngrams
import os
import operator
from collections import OrderedDict
corpus_dir = "cleaned_content_dir/"
default_corpus = os.listdir(corpus_dir)
doc_token_count_dic = {}


def create_index(corpus, n_gram_val):
    doc_token_dic = {}
    for doc in corpus:
        doc_file = open(corpus_dir + doc, 'r')
        doc_data = doc_file.read()
        tokens = word_tokenize(doc_data)
        if n_gram_val == 1:
            doc_token_dic[doc] = tokens
        elif n_gram_val == 2:
            bi_grams = ngrams(tokens, n_gram_val)
            doc_token_dic[doc] = bi_grams
        elif n_gram_val == 3:
            tri_gram = ngrams(tokens, n_gram_val)
            doc_token_dic[doc] = tri_gram
        doc_file.close()
    create_word_dic(doc_token_dic, n_gram_val)


def create_word_dic(doc_token_dic, n_gram_value):
    word_dic = dict()
    for each in doc_token_dic:
        for word in doc_token_dic[each]:
            if word in word_dic:
                if each in word_dic[word]:
                    word_dic[word][each] += 1
                else:
                    word_dic[word][each] = 1
            else:
                doc_dic = dict()
                doc_dic[each] = 1
                word_dic[word] = doc_dic
    create_term_freq_table(word_dic, n_gram_value)
    create_doc_freq_table(word_dic, n_gram_value)


def create_term_freq_table(word_dic, n_gram_val):
    doc_val = 0
    term_freq = {}
    file_name = open(corpus_dir + "term_freq_table_for_"
                     + str(n_gram_val) +"_ngrams", "w+")
    for word in word_dic:
        for doc in word_dic[word]:
            doc_val += word_dic[word][doc]
        term_freq[word] = doc_val
    sorted_dict = list(sorted(term_freq.items(), key=lambda i: (i[1], i[0]), reverse=True))
    for each in sorted_dict:
        file_name.writelines("term -> " + str(each[0])
                             + ", freq -> " + str(each[1]) + '\n')
    file_name.close()
    return 0


def create_doc_freq_table(word_dic, n_grams):
    file_name = open(corpus_dir + "document_frequency_table_for_"
                     + str(n_grams) + "_ngrams", "w+")
    for word in word_dic:
        docs = word_dic[word]
        doc_total = len(docs)
        file_name.writelines("word -> " + str(word) + ", docs -> "
                             + str(docs.keys()) + ", doc_frequency "
                             + str(doc_total) + '\n')
    file_name.close()
    return 0

#verifcation code prints the total count of term reference in the document
    # for word in word_dic:
    #     if word == ('in', 'solar'):
    #         print word_dic[word]
    #     else:
    #         continue


def main():
    n_gram_limit = 1
    while n_gram_limit is not 4:
        create_index(default_corpus, n_gram_limit)
        n_gram_limit += 1

main()
