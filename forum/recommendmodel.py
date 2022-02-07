import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer as vectorizer
from sklearn.metrics.pairwise import sigmoid_kernel 
import os

from django.conf import settings
#from difflib import SequenceMatcher as sm



settings.configure()

'''['id', 'title', 'category', 'subcategory','answers' , 'combined']'''


post_df = None
sig = None
index =None

#base = settings.VARIABLE['BASE_DIR']
#print(type(base))


def load_data():
    
    #df = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/data.csv'))
    df = pd.read_csv('data/data.csv')
    return df
    
def pre_process():
    data = load_data()
    
    
    return data



def process():
    global post_df , sig , index
    post_df = pre_process() 
    tfv = vectorizer(min_df=4,max_df=20 , max_features=None , strip_accents ='unicode' , analyzer='word'
        ,token_pattern = r'\w{1,}' ,
                ngram_range=(1,3),
                stop_words = 'english')
    tfv_matrix = tfv.fit_transform(post_df['combined'])
    sig = sigmoid_kernel(tfv_matrix,tfv_matrix)
    index = pd.Series(post_df.index, index=post_df['title']).drop_duplicates()
    
def recommend(search_word):
    
    post_df = pre_process() 
    
    tfv = vectorizer(min_df=0.5 , max_features=None , strip_accents ='unicode' , analyzer='word'
        ,token_pattern = r'\w{1,}' ,
                ngram_range=(1,3),
                stop_words = 'english')
    tfv_matrix = tfv.fit_transform(post_df['combined'])
    sig = sigmoid_kernel(tfv_matrix,tfv_matrix)
    index = pd.Series(post_df.index, index=post_df['id']).drop_duplicates()
    #print(post_df['id'])
   
    
    
    title= search_word
    
    max_se = 0.0
    name = ''
    '''for i in list(post_df['title']):
        se = sm(None , title , i)
        if(se.ratio() > max_se):
            name = i
            max_se = se.ratio()
            '''
    name = title
    idx = index[name]
    if(type(idx) == pd.core.series.Series):
        print(type(idx) == pd.core.series.Series)
        idx = index[name]
        idx = idx[[random.randint(0,(len(idx)-1))]]
        idx = idx[name]
    else:
        idx = index[name]
    print(index)
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:8]
    indices = [i[0] for i in sig_scores]
    return list(post_df['id'].iloc[indices])
    


def recommend_pro(search_word):
    post_list = recommend(search_word)
    if(post_list == None):
        return None
    
    return post_list


po = recommend_pro(2)
print(po)
