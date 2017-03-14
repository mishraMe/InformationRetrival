
# This program creates an inverted index for an
#input corups
from nltk import word_tokenize
from nltk.util import ngrams
import os
corpus_dir = "cleaned_content_dir/"
default_corpus = os.listdir(corpus_dir)

word_dic = dict()
doc_tokens = []
doc_token_dic = {}


def create_index(corpus, n_gram_val):
    global doc_tokens
    for doc in corpus:
        doc_file = open(corpus_dir + doc, 'r')
        doc_data = doc_file.read()
        tokens = word_tokenize(doc_data)
        if n_gram_val == 1:
            doc_tokens = tokens
        elif n_gram_val == 2:
            bi_grams = ngrams(tokens, n_gram_val)
            doc_tokens = bi_grams
            for each in bi_grams:
                print each
        elif n_gram_val == 3:
            tri_gram = ngrams(tokens, n_gram_val)
            doc_tokens = tri_gram
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



#verifcation code prints the total count of term reference in the document
    # for word in word_dic:
    #     if word == "solar":
    #         print word_dic[word]
    #     else:
    #         continue


def main():
    n_gram_limit = 1
    while n_gram_limit is not 3:
        create_index(default_corpus, n_gram_limit)
        n_gram_limit += 1

main()
