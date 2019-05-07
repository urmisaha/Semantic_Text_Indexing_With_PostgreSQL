import pickle
from tqdm import tqdm
import sys

method = sys.argv[1]

if method == 'wordnet':
    with open('sample_vocab.wn.pkl', 'rb') as f:
        synsets = pickle.load(f)
    with open('synonym_sample.wn.syn', 'w+') as f:
        for i in tqdm(range(len(synsets))):
            f.write(synsets[i][1]+' '+synsets[i][0]+'\n')
        f.write('indices'+' '+'index*')

elif method == 'glove':
    with open('sample_vocab.gv.pkl', 'rb') as f:
        similar_words = pickle.load(f)
    with open('synonym_sample.gv.syn', 'w+') as f:
        for i in tqdm(range(len(similar_words))):
            f.write(similar_words[i][1]+' '+similar_words[i][0]+'\n')
        f.write('indices'+' '+'index*')

elif method == 'fasttext':
    with open('sample_vocab.ft.pkl', 'rb') as f:
        similar_words = pickle.load(f)
    with open('synonym_sample.ft.syn', 'w+') as f:
        for i in tqdm(range(len(similar_words))):
            f.write(similar_words[i][1]+' '+similar_words[i][0]+'\n')
        f.write('indices'+' '+'index*')