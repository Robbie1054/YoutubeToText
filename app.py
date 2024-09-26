from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import html

app = Flask(__name__)

# Replace with your actual API key
YOUTUBE_API_KEY = 'YOUR_API_KEY_HERE'

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "URL is required"}), 400
    
    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        captions = fetch_captions(video_id)
        return jsonify(captions)
    except HttpError as e:
        return jsonify({"error": f"YouTube API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def extract_video_id(url):
    import re
    video_id_match = re.search(r"(?<=v=)[^&#]+", url)
    if video_id_match:
        return video_id_match.group(0)
    return None

def fetch_captions(video_id):
    captions_response = youtube.captions().list(
        part="snippet",
        videoId=video_id
    ).execute()

    caption_track = next((track for track in captions_response['items'] 
                          if track['snippet']['language'] == 'en'), None)
    
    if not caption_track:
        return []

    caption_track_id = caption_track['id']
    subtitle = youtube.captions().download(
        id=caption_track_id,
        tfmt='srt'
    ).execute()

    return parse_srt(subtitle.decode('utf-8'))

def parse_srt(srt_string):
    import re
    subtitle_parts = re.split(r'\n\n', srt_string.strip())
    captions = []

    for part in subtitle_parts:
        lines = part.split('\n')
        if len(lines) >= 3:
            time_line = lines[1]
            text = ' '.join(lines[2:])
            
            start, end = time_line.split(' --> ')
            
            captions.append({
                'start': time_to_seconds(start),
                'end': time_to_seconds(end),
                'text': html.unescape(text)
            })

    return captions

def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s.replace(',', '.'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
