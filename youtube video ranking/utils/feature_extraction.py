from sklearn.feature_extraction.text import TfidfVectorizer

def get_tfidf_features(text_list):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_list)
    return tfidf_matrix, vectorizer
