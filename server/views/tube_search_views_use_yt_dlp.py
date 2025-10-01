# server/views/tube_search_views.py

from flask import Blueprint, request, jsonify
import yt_dlp

bp = Blueprint('youtube_search', __name__, url_prefix='/search')

@bp.route('/search', methods=['GET'])
def search_youtube():
    query = request.args.get('query')
    print(f"Received search query: {query}")
    if not query:
        return jsonify({'code': 400, 'message': '검색어를 입력해 주세요.'}), 400

    try:
        videos = fetch_youtube_search_results(query, max_results=10)

        result = []
        for video in videos:
            video_info = {
                'title': video.get('title'),
                'video_id': video.get('id'),
                'url': f"https://www.youtube.com/watch?v={video.get('id')}",
                'duration': seconds_to_hhmmss(video.get('duration', 0)),
                'thumbnail': video.get('thumbnail')  # ✨ 썸네일 URL 추가
            }
            result.append(video_info)

        return jsonify({'code': 200, 'videos': result}), 200

    except Exception as e:
        print(f"Error fetching YouTube search results: {e}")
        return jsonify({'code': 500, 'message': '서버 오류가 발생했습니다.'}), 500


def fetch_youtube_search_results(query, max_results=10):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    search_url = f"ytsearch{max_results}:{query}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=False)
        return info['entries']


def seconds_to_hhmmss(seconds):
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h:02}:{m:02}:{s:02}"
    else:
        return f"{m:02}:{s:02}"
