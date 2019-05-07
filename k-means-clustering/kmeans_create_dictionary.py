import pickle
from tqdm import tqdm
from kmeans_create_vocab import autovivify_list

with open('cluster_to_words.ft.pkl', 'rb') as f:
    clusters = pickle.load(f)
  
  # print(clusters)

#   maxlen = 0
with open('synonym_sample.kmeans.ft.syn', 'w+') as f:
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