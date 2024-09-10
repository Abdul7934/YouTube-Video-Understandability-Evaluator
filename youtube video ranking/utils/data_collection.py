import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi

# Set up YouTube API service
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyD8MAHtts2r7caEbpO79L3Q7rK-xE7_GRQ"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    if "v=" in url:
        # Extract video ID from full URL
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be" in url:
        # Extract video ID from shortened URL
        return url.split('/')[-1].split('?')[0]
    else:
        # Return the URL itself if it's already the video ID
        return url

def get_video_details(video_url_or_id):
    """Retrieve details about the YouTube video."""
    video_id = extract_video_id(video_url_or_id)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    return response

def get_transcript(video_url_or_id):
    """Retrieve the transcript of the YouTube video."""
    video_id = extract_video_id(video_url_or_id)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

# Example usage: Place your YouTube links here
if __name__ == '__main__':
    video_url = "https://youtu.be/ENLEjGozrio?si=OrdQaSFlszCZuJcU"
    
    # Fetch video details
    details = get_video_details(video_url)
    print("Video Details:", details)

    # Fetch transcript
    transcript = get_transcript(video_url)
    print("Transcript:", transcript)
