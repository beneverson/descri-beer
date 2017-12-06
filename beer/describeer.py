#!/usr/bin/env python

import pickle

from annoy import AnnoyIndex
from gensim.models import KeyedVectors
from sklearn.externals import joblib


class Describeer(object):
    '''Class for retrieving beers by descriptor from review data.'''

    def __init__(self, vectors_path='models/beervectors.vec',
                 annoy_path='models/tfidf_index.ann',
                 model_path='models/tfidf_model.pkl',
                 index_lookup_path='models/index_to_beerid.pkl',
                 name_lookup_path='models/index_to_name.pkl'):
        # load the word vector model
        self.word_vectors = KeyedVectors.load_word2vec_format(vectors_path)
        # load the tfidf model
        self.tfidf_model = joblib.load(model_path)
        # load the annoy index, using the appropriate number of features
        self.annoy_index = AnnoyIndex(len(self.tfidf_model.vocabulary_.keys()))
        self.annoy_index.load(annoy_path)
        # load the index_to_beerid dict
        with open(index_lookup_path, 'rb') as f:
            self.index_to_beerid = pickle.load(f)
        with open(name_lookup_path, 'rb') as f:
            self.index_to_name = pickle.load(f)

    def expand_query(self, query, topn=10):
        expanded_query = []
        # query is a space-delimited string of query tokens
        for term in query.split(' '):
            expanded_term = []
            # add the original term if its in the model vocabulary
            if term in self.tfidf_model.vocabulary_.keys():
                expanded_term.append(term)
            # add any similar terms found by the word similarity model
            if term in self.word_vectors.vocab.keys():
                for word, score in (self.word_vectors
                                    .similar_by_word(term, topn=10*topn)):
                    # making sure the word is also in the tfifd model's vocab
                    if word in self.tfidf_model.vocabulary_.keys():
                        expanded_term.append(word)
            # extend the full query by the expanded term
            expanded_query.extend(expanded_term[:topn+1])
        # join all with spaces and return
        return ' '.join(expanded_query)

    def search(self, positive='', negative='', n_results=20):
        # first expand the queries
        pos_expanded = self.expand_query(positive)
        neg_expanded = self.expand_query(negative)
        # form positive query vectors via tfidf
        query_vec_p = (self.tfidf_model.transform([pos_expanded])
                                       .toarray()
                                       .reshape(-1))
        # form negative query vectors via tfidf
        query_vec_n = (self.tfidf_model.transform([neg_expanded])
                                       .toarray()
                                       .reshape(-1))
        # subtract positive and negative vectors
        query_vec = query_vec_p - query_vec_n
        # find the nearest neighbors according to annoy index
        items, distances = (self.annoy_index
                                .get_nns_by_vector(query_vec,
                                                   n=n_results,
                                                   include_distances=True,
                                                   search_k=-1))
        # retrieve the name and beerid for each result
        result_names = [self.index_to_name[i] for i in items]
        result_beerids = [self.index_to_beerid[i] for i in items]
        # zip up the results and return
        return list(zip(result_names, result_beerids, distances))
