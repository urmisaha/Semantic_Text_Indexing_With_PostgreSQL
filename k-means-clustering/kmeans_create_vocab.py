from sklearn.cluster import KMeans
from numbers import Number
from pandas import DataFrame
import sys, codecs, numpy
import pickle
from tqdm import tqdm
from gensim.models import FastText
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class autovivify_list(dict):
  '''A pickleable version of collections.defaultdict'''
  def __missing__(self, key):
    '''Given a missing key, set initial value to an empty list'''
    value = self[key] = []
    return value

  def __add__(self, x):
    '''Override addition for numeric types when self is empty'''
    if not self and isinstance(x, Number):
      return x
    raise ValueError

  def __sub__(self, x):
    '''Also provide subtraction method'''
    if not self and isinstance(x, Number):
      return -1 * x
    raise ValueError

def build_word_vector_matrix(vector_file, n_words):
  '''Return the vectors and labels for the first n_words in vector file'''
  numpy_arrays = []
  labels_array = []
  with codecs.open(vector_file, 'r', 'utf-8') as f:
    for c, r in enumerate(f):
      sr = r.split()
      labels_array.append(sr[0])
      numpy_arrays.append( numpy.array([float(i) for i in sr[1:]]) )

      if c == n_words:
        return numpy.array( numpy_arrays ), labels_array

  return numpy.array( numpy_arrays ), labels_array

def find_word_clusters(labels_array, cluster_labels):
  '''Return the set of words in each cluster'''
  cluster_to_words = autovivify_list()
  for c, i in enumerate(cluster_labels):
    cluster_to_words[ i ].append( labels_array[c] )
  return cluster_to_words

word_list = []
sentences = []

stop_words = set(stopwords.words('english'))

# filename = sys.argv[1]

# python kmeans.py glove.6B.100d.txt 300 .1
if __name__ == "__main__":
  # with open("../sentences.pkl", "rb") as f:
  #   sentences = pickle.load(f)

  # with open("../word_list.pkl", "rb") as f:
  #   word_list = pickle.load(f)

  with open("../data/X.txt", 'r') as f:
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

  # using FastText to create embeddings from our dataset
  print("creating FastText model!")
  model = FastText(sentences, size=100, window=5, min_count=5, workers=8,sg=1)
  print("FastText model created successfully!")
  
  numpy_arrays = []
  labels_array = []
  print("creating vocabulary clusters...")
  for word in word_list:
      labels_array.append(word)
      try:
          numpy_arrays.append(model[word])
      except:
          pass
  df = numpy.array(numpy_arrays)

  n_words = int(sys.argv[1]) # Number of words to analyze
  reduction_factor = float(sys.argv[2]) # Amount of dimension reduction {0,1}
  n_clusters = int( n_words * reduction_factor ) # Number of clusters to make
  kmeans_model = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
  kmeans_model.fit(df)

  cluster_labels  = kmeans_model.labels_
  cluster_inertia   = kmeans_model.inertia_
  cluster_to_words  = find_word_clusters(labels_array, cluster_labels)

  with open('cluster_to_words.ft.pkl', 'wb') as f:
      pickle.dump(cluster_to_words, f)
  
  print("cluster vocabulary created successfully!")

  with open('cluster_to_words.ft.pkl', 'rb') as f:
    clusters = pickle.load(f)
  
  # print(clusters)

#   maxlen = 0
with open('synonym_sample.kmeans1.ft.syn', 'w+') as f:
    print("creating dictionary...")
    for c in clusters:
        # print((clusters[c]))
        # print("\n")
        # maxlen = max(maxlen, len(clusters[c]))
        # if maxlen < len(clusters[c]):
        #     maxlen = len(clusters[c])
        #     maxc = clusters[c]
    
        words = clusters[c]
        root, words = words[0], words[1:]
        
        f.write(root+' '+root+'\n')
        for i in range(len(words)):
            f.write(words[i]+' '+root+'\n')
    f.write('indices'+' '+'index*')
    print("dictionary created successfully...")

  # print(maxlen)
  # print(maxc)