#!/usr/bin/env python

import argparse

import pandas as pd
from tqdm import tqdm


def parse(review):
    '''Parse a list of review lines into a dictionary.'''
    return {r.split(': ')[0].strip(): r.split(': ')[1].strip()
            for r in review}


def read_reviews(path):
    '''Read reviews from file, return as a list of dicts.'''
    reviews = []
    delimiter = '\n'
    review = []
    with open(path, "r", encoding='latin1') as f:
        # iterate thru file, and parse blank-line delimited chunks
        for line in tqdm(f.readlines()):
            if line == delimiter:
                reviews.append(parse(review))
                review = []
            else:
                review.append(line)
    return reviews


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/raw/Ratebeer.txt',
                        help='path to read source data')
    parser.add_argument('--outfile', type=str,
                        default='data/interim/ratebeer.csv',
                        help='path to write parsed CSV file')
    args = parser.parse_args()
    # read and parse reviews
    reviews = read_reviews(args.data)
    # convert to dataframe representation
    df = pd.DataFrame(reviews)
    # save as CSV
    df.to_csv(args.outfile, index=False)

if __name__ == '__main__':
    main()
