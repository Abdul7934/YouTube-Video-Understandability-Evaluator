from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

def compute_similarity(tfidf_matrix):
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity
