from flask import Flask, request, render_template
from utils.data_collection import get_transcript
from utils.preprocessing import preprocess_text
from utils.feature_extraction import get_tfidf_features
from utils.content_analysis import compute_similarity, analyze_sentiment
from utils.evaluation import compute_understanding_score

app = Flask(__name__)

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be" in url:
        return url.split('/')[-1].split('?')[0]
    else:
        return url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        links = request.form['links'].splitlines()  # Split input links by newlines
        
        transcripts = []
        cleaned_texts = []
        
        # Process each video
        for link in links:
            video_id = extract_video_id(link)
            transcript = get_transcript(video_id)  # Get transcript for each video
            cleaned_text = preprocess_text(transcript)  # Clean the transcript text
            transcripts.append(transcript)  # Store original transcripts
            cleaned_texts.append(cleaned_text)  # Store cleaned transcripts for analysis

        # Feature Extraction
        tfidf_matrix, _ = get_tfidf_features(cleaned_texts)

        # Content Analysis (similarity and sentiment)
        similarity_matrix = compute_similarity(tfidf_matrix)
        sentiment_scores = [analyze_sentiment(text) for text in cleaned_texts]

        # Evaluation & Ranking
        scores = [compute_understanding_score(similarity_matrix[i][i], sentiment_scores[i]) for i in range(len(links))]
        best_video_index = scores.index(max(scores))  # Get index of best video
        best_video = links[best_video_index]  # Get the best video link
        best_transcript = transcripts[best_video_index]  # Get the corresponding transcript

        return render_template('index.html', best_video=best_video, best_transcript=best_transcript, subject=subject)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
