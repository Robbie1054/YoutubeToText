from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, jsonify

app = Flask(__name__)

url = 'https://www.youtube.com/watch?v=5YytKT8Z8W8'
print(url)

def url_format(url):
  video_id = url.replace('https://www.youtube.com/watch?v=', '')
  print(video_id)
  get_transcript(video_id)

def get_transcript(video_id):
  transcript = YouTubeTranscriptApi.get_transcript(video_id)
  get_output(transcript)

def get_output(transcript):
  output=''
  for x in transcript:
    sentence = x['text']
    output += f' {sentence}\n'
  print(output)

if __name__ == "__main__":
  url_format(url)
