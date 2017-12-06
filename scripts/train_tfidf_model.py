#!/usr/bin/env python

import argparse
import pickle
import os

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from annoy import AnnoyIndex
from tqdm import tqdm


def read_data(data_path, review_column, id_column, topn):
    # read data
    df = pd.read_csv(data_path)
    # make sure the reviews and ids are parsed as strings
    df[review_column] = df[review_column].astype(str)
    df[id_column] = df[id_column].astype(str)
    # extract only the topn most popular beers
    topn_df = df[id_column].value_counts().iloc[:topn].reset_index()
    topn_df.columns = [id_column, 'review_count']
    return pd.merge(df, topn_df, how='right', on=id_column)


def save_annoy_index(term_doc_matrix, annoy_index):
    # instantiate a new index
    aix = AnnoyIndex(term_doc_matrix.shape[1])
    # add all beers to the index
    for bix in tqdm(range(term_doc_matrix.shape[0])):
        aix.add_item(bix, term_doc_matrix[bix].toarray().reshape(-1))
    # build the index
    aix.build(100)
    # save the index
    aix.save(annoy_index)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str,
                        default='data/interim/ratebeer.csv',
                        help='path to read source data')
    parser.add_argument('--id_column', type=str, default='beer/beerId',
                        help='column of input data containing beer ids')
    parser.add_argument('--review_column', type=str, default='review/text',
                        help='column of input data containing review text')
    parser.add_argument('--name_column', type=str, default='beer/name',
                        help='column of input data containing beer name')
    parser.add_argument('--topn', type=int, default=2500,
                        help='number of beers to train on, by review count')
    parser.add_argument('--lookups', type=str,
                        default='models/',
                        help='path to save lookup dicts')
    parser.add_argument('--annoy_index', type=str,
                        default='models/tfidf_index.ann',
                        help='path to save annoy index')
    parser.add_argument('--model_path', type=str,
                        default='models/tfidf_model.pkl',
                        help='path to save trained model object')
    args = parser.parse_args()
    # read data
    df = read_data(args.data, args.review_column, args.id_column, args.topn)
    # generate 'documents' by grouping reviews by beerid
    # and concatenating them into big strings
    docs_df = (df.groupby([args.id_column,
                           args.name_column])[args.review_column]
                 .apply(' '.join)
                 .reset_index())
    # save the index_to_beerid lookup dict as a pickle file
    index_to_beerid = docs_df[args.id_column].to_dict()
    with open(os.path.join(args.lookups, 'index_to_beerid.pkl'), 'wb') as f:
        pickle.dump(index_to_beerid, f)
    # save the index_to_name lookup dict as a pickle file
    index_to_name = docs_df[args.name_column].to_dict()
    with open(os.path.join(args.lookups, 'index_to_name.pkl'), 'wb') as f:
        pickle.dump(index_to_name, f)
    # instantiate, train the tfidf model
    tfidf = TfidfVectorizer(min_df=0.001)
    # transform beers into tfidf representation
    term_beer_matrix = tfidf.fit_transform(docs_df[args.review_column].values)
    # save the results in an annoy index
    save_annoy_index(term_beer_matrix, args.annoy_index)
    # save the tfidf model
    joblib.dump(tfidf, args.model_path)

if __name__ == '__main__':
    main()
