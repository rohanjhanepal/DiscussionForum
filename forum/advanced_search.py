from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



def search(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_sentence = []
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence
    """
    This function takes a text a.
    It returns a list of all the search terms that appear in the text.
    """ 
