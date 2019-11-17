
# #### We create a function cleanQ so we can do the cleaning and preperation of our data 
# #### INPUT: String
# #### OUTPUT: Cleaned String

def cleanQ(query):
    query = query.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(query)
    stemmer=[ps.stem(i) for i in tokens]
    filtered_Q = [w for w in stemmer if not w in stopwords.words('english')]
    return filtered_Q

# #### We create a function computeTF so we can calculate the tf
# #### INPUT: Dictionary where the keys are the terms_id and the values are the frequencies of this term Id in the document
# #### OUTPUT: TF of the specific Term_id in the corresponding document

def computeTF(doc_words):
    bow = 0
    for k, v in doc_words.items():
        bow = bow + v
    tf_word = {}
    for word, count in doc_words.items():
        tf_word[word] = count / float(bow)
    return tf_word
