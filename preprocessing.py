import sys
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

filename = sys.argv[1]

word_list = []
sentences = []

stop_words = set(stopwords.words('english'))

with open(filename, 'r') as f:
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

with open("word_list.pkl", "wb") as f:
    pickle.dump(word_list, f)

with open("sentences.pkl", "wb") as f:
    pickle.dump(sentences, f)