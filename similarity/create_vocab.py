from nltk.corpus import wordnet as wn
import pickle
from gensim.models import Word2Vec
from gensim.models import FastText
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

method = sys.argv[1]

synset_list = []
similar_list = []
similar_words = []
word_list = []
sentences = []

# with open("../word_list.pkl", "rb") as f:
#     word_list = pickle.load(f)

# with open("../sentences.pkl", "rb") as f:
#     sentences = pickle.load(f)

stop_words = set(stopwords.words('english'))

with open('../data/X.txt', 'r') as f:
    cnt = 0
    for line in f:
        cnt = cnt + 1
        if cnt%500 == 0:
            print("processed: "+str(cnt)+" lines!")
        word_list.extend(nltk.word_tokenize(line))
        word_list = list(set(word_list))
        sublines = line.strip().split('.')
        sublines = [subline.strip().split(' ') for subline in sublines]
        sentences.extend(sublines)
    word_list = [word for word in word_list if word.isalpha()]
    print ("Punctuations removed...")
    word_list = [word for word in word_list if not word in stop_words]
    print ("Stop words removed...")
    word_list = list(set(word_list))
    print("word_list created successfully!\n"+str(len(word_list)))
    print(len(sentences))

if method == 'wordnet':
    print("creating vocabulary...")
    for word in word_list:
        syns = wn.synsets(word)
        temp_list = []
        for s in syns:
            temp_list.append(s.lemmas()[0].name())
        temp_list = list(set(temp_list))
        for s in temp_list:
            synset_list.append((word, s))

    with open('sample_vocab.wn.pkl', 'wb') as f:
        pickle.dump(synset_list, f)
        print("vocabulary created successfully!")

elif method == 'glove':
    print("creating glove model...")
    model = Word2Vec(sentences=sentences, size=100, window=5, min_count=2, workers=4, sg=0)
    print("model created successfully!")
    
    print("creating vocabulary...")
    for word in word_list:
        try:
            similar_words = model.wv.most_similar(word)
        except:
            print("Could not find similar words!")
        for w, sim in similar_words:
            similar_list.append((word, w))
    
    with open('sample_vocab.gv.pkl', 'wb') as f:
        pickle.dump(similar_list, f)
        print("vocabulary created successfully!")

elif method == 'fasttext':
    print("creating fasttext model...")
    model = FastText(sentences, size=100, window=5, min_count=2, workers=4,sg=1)
    print("model created successfully!")
    
    print("creating vocabulary...")
    for word in word_list:
        try:
            similar_words = model.wv.most_similar(word)
        except:
            print("Could not find similar words!")
        for w, sim in similar_words:
            similar_list.append((word, w))
    
    with open('sample_vocab.ft.pkl', 'wb') as f:
        pickle.dump(similar_list, f)
        print("vocabulary created successfully!")
