# Searching documents containing words in query as well as words which are similar to query words.

### Approaches
1. Similarity based: FastText, GloVe
2. k-means Clustering
3. Synonym based approach using Wordnet
4. LSH (not yet integrated with postgresql) 
5. Topic Modelling using LDA (not completed)

### Observations
> k-means clustering based approach performs the best when used with word vectors learned from FastText.

### Folder Structure
Important folders are mentioned in the following folder structure:
```
Semantic_Text_Indexing_With_PostgreSQL
|
|_data_ 
|   |_ X.txt
|   |_ create_large_dataset.py: inserts data from X.txt into table
|
|_k-means-clustering_
|	|_ kmeans_create_vocab.py: preprocesses text data and creates vocabulary, then creates clusters and store the mapping syn dictionary
|
|_similarity_
|	|_ create_vocab.py: preprocesses data and creates vocabulary
|	|_ create_dictionary.py: creates syn dictionary with mapping between similar words from the vocabulary
|
|_ other folders...
```

### Steps to run the project
1. Create table documents:
create table documents
	(title		varchar(20), 
	 description		TEXT
	);

2. Insert data into table: python data/create_large_dataset.py X.txt

3. Preprocess data and create vocabulary with [method:wordnet/glove/fasttext]: python create_vocab.py [method]
For k-means-clustering (along with preprocessing data and creating vocabulary, this also creates dictionary): python kmeans_create_vocab.py [n_words] [reduction_factor] 

4. Create dictionary with [method:wordnet/glove/fasttext]: python create_dictionary.py [method]

5. syn dictionary is formed in [name].syn format: e.g. synonym_sample_[method].syn
Location of this file: ```/home/user/git/postgresql/src/install/share/tsearch_data```
This file is used by pgadm3 in the following steps.

6. From pgadm3 interface:
```
Create TEXT SEARCH DICTIONARY
CREATE TEXT SEARCH DICTIONARY document_dict (
    template = synonym,
    synonyms = synonym_sample
);
```
To delete dictionary for recreating it for various methods:
```
DROP TEXT SEARCH DICTIONARY document_dict CASCADE;
```

7. From pgadm3 interface:
```
CREATE TEXT SEARCH CONFIGURATION document_config (copy=simple);
```

8. Map TEXT SEARCH CONFIGURATION to TEXT SEARCH DICTIONARY:
```
ALTER TEXT SEARCH CONFIGURATION document_config
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
                  word, hword, hword_part
    WITH document_dict;
```

9. Try searching with a query word:
```
SELECT title from documents where to_tsvector('document_config_ft', description) @@ to_tsquery('document_config_ft','anthropologists');
 ```
 This should fetch _titles_ of documents whose _description_ column contains the _query word_ or any other word which is similar to _query word_ as per the mapping in the dictionary configuration currently used (document_config)

 Indexing has been done by GIN index:
 ```
CREATE INDEX vector ON documents USING GIN (document_index_description);
 ```
