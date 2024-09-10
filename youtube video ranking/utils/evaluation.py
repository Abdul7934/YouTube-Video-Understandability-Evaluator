def compute_understanding_score(similarity, sentiment_score):
    score = (similarity + sentiment_score) / 2
    return score
