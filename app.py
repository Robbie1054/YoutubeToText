from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_url():
    data = request.json
    url = data.get('url')
    url_format(url)

def url_format(url):
  video_id = url.replace('https://www.youtube.com/watch?v=', '')
  print(video_id)
  get_transcript(video_id)

def get_transcript(video_id):
  transcript = YouTubeTranscriptApi.get_transcript(video_id)
  get_output(transcript)

def get_output(transcript):
  return jsonify(transcript)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
