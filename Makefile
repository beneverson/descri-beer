data: data/raw/Ratebeer.txt data/raw/beerdf.pandas
	# parse the ratebeer reviews into a csv
	scripts/parse_reviews.py

vector_data: data/interim/ratebeer.csv
	# create the training data for fasttext vectors
	scripts/make_fasttext_data.py --data data/interim/ratebeer.csv --input_type csv
	scripts/make_fasttext_data.py --data data/raw/beerdf.pandas --input_type pickle

vectors: data/interim/reviews_raw.txt 
	# train fasttext vectors
	fasttext skipgram -input data/interim/reviews_raw.txt -output models/beervectors

model: data/interim/ratebeer.csv 
	# train the tfidf model
	scripts/train_tfidf_model.py

clean: 
	# delete all of the files we created
	rm -r data/interim/ratebeer.csv
	rm -r data/interim/reviews_raw.txt
	rm -r models/beervectors.bin
	rm -r models/beervectors.vec
	rm -r models/index_to_beerid.pkl
	rm -r models/index_to_name.pkl
	rm -r models/tfidf_index.ann
	rm -r models/tfidf_model.pkl

all: data vector_data vectors model

.PHONY: data vectors model all