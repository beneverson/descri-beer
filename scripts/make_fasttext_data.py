#!/usr/bin/env python

import argparse
import pickle
import string

import pandas as pd


def parse_csv(filepath, column):
    # read the file at filepath with pandas
    df = pd.read_csv(filepath)
    # return the reviews column as a list
    return df[column].astype(str).tolist()


def parse_pickle(filepath, column):
    # load the file at filepath with pickle
    with open(filepath, 'rb') as f:
        df = pickle.load(f, encoding='ISO-8859-1')
    # return the reviews column as a list
    return df[column].astype(str).tolist()


def clean_review(review):
    # make a translator object in order to remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    # remove punctuation, and make text lowercase
    return review.translate(translator).lower()


def clean_merge_reviews(reviews):
    # clean reviews and merge them with newline characters
    return '\n'.join([clean_review(r) for r in reviews])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str,
                        default='data/interim/ratebeer.csv',
                        help='path to read source data')
    parser.add_argument('--input_type', type=str, default='csv',
                        choices=['csv', 'pickle'], help='filetype of input')
    parser.add_argument('--review_column', type=str, default='review/text',
                        help='column of input data containing review text')
    parser.add_argument('--outfile', type=str,
                        default='/data/interim/reviews_raw.txt',
                        help='path to write cleaned review text')
    args = parser.parse_args()
    # parse the input file into a list of (unmodified) review string
    if args.input_type == 'pickle':
        reviews = parse_pickle(args.data, args.review_column)
    else:
        reviews = parse_csv(args.data, args.review_column)
    # clean review strings, merge into single string
    cleaned_reviews = clean_merge_reviews(reviews)
    # write out the merged string into the outfile, in append mode
    with open(args.outfile, 'a+') as f:
        f.write(cleaned_reviews)

if __name__ == '__main__':
    main()
