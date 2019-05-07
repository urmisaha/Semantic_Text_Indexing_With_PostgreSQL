# Searching documents containing words in query as well as words which are similar to query words.

### Steps to run project

1. Create table documents:
create table documents
	(title		varchar(20), 
	 description		TEXT
	);

2. Insert data into table: python data/create_large_dataset.py X.txt

3. Preprocess the data in datafile: python preprocessing.py data/X.txt (Run from folder containing preprocessing.py file)

4. Create vocabulary with [method:wordnet/glove/fasttext]: python create_vocab.py [method]
For k-means-clustering: python kmeans_create_vocab.py [n_words] [reduction_factor] 

5. Create dictionary with [method:wordnet/glove/fasttext]: python create_dictionary.py [method]
> For k-means-clustering: python kmeans_create_dictionary.py

6. syn dictionary is formed in [].syn format: e.g. synonym_sample_[method].syn
Location of this file: ```/home/user/git/postgresql/src/install/share/tsearch_data```
This file is used by pgadm3 in the following steps.

7. From pgadm3 interface:
Create TEXT SEARCH DICTIONARY
CREATE TEXT SEARCH DICTIONARY document_dict (
    template = synonym,
    synonyms = synonym_sample
);
To delete dictionary for recreating it for various methods:
DROP TEXT SEARCH DICTIONARY document_dict CASCADE;

8. From pgadm3 interface::
CREATE TEXT SEARCH CONFIGURATION document_config (copy=simple);

9. Map TEXT SEARCH CONFIGURATION to TEXT SEARCH DICTIONARY:
ALTER TEXT SEARCH CONFIGURATION document_config
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
                  word, hword, hword_part
    WITH document_dict;

10. Try searching with a query word:
SELECT title from documents where to_tsvector('document_config_ft', description) @@ to_tsquery('document_config_ft','anthropologists');
 This should fetch _titles_ of documents whose _description_ column contains the _query word_ or any other word which is similar to _query word_ as per the mapping in the dictionary configuration currently used (document_config)