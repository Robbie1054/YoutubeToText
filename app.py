from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_transcript', methods=['POST'])
def get_url():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    return url_format(url)

def url_format(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    return get_transcript(video_id)

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return get_output(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_output(transcript):
    return jsonify(transcript)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
