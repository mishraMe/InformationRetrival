
# This program creates an inverted index for an
#input corups

import os
corpus_dir = "cleaned_content_dir/"
default_corpus = os.listdir(corpus_dir)

word_dic = dict()
doc_tokens = []
doc_token_dic = {}


def create_index(corpus, n_gram):
    global doc_tokens
    for doc in corpus:
        doc_file = open(corpus_dir + doc, 'r')
        doc_data = doc_file.read()
        if n_gram == 1:
            doc_tokens = doc_data.split()
        else:
            doc_tokens = doc_data.split(" ", n_gram)
        doc_token_dic[doc] = doc_tokens
        doc_file.close()

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

    for word in word_dic:
        if word == "solar":
            print word_dic[word]
        else:
            continue


def main():
    n_gram_limit = 1
    while n_gram_limit is not 2:
        create_index(default_corpus, n_gram_limit)
        n_gram_limit += 1

main()
