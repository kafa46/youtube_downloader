# server/views/tube_search_views.py

import json
import os
from flask import Blueprint, request, jsonify, current_app
import requests
from secret import YOUTUBE_API_KEY

bp = Blueprint('youtube_search', __name__, url_prefix='/search')

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
USE_DEVMODE = True  # ✨ 개발모드 on/off 설정
# USE_DEVMODE = False  # ✨ 개발모드 on/off 설정
VIDEO_DATA_FILE = 'sample_videos.json'

@bp.route('/search', methods=['GET'])
def search_youtube():
    DEV_DATA_DIR = os.path.join(current_app.root_path, 'static', 'devdata')
    query = request.args.get('query')
    print(f"Received search query: {query}")
    if not query:
        return jsonify({'code': 400, 'message': '검색어를 입력해 주세요.'}), 400

    if USE_DEVMODE:
        # ✨ 개발 모드: 저장된 JSON 파일 사용
        print("Using development mode: loading sample data")
        with open(os.path.join(DEV_DATA_DIR, VIDEO_DATA_FILE), 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'code': 200, 'videos': data}), 200

    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 10,
        'key': YOUTUBE_API_KEY
    }

    try:
        response = requests.get(YOUTUBE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get('items', []):
            video = {
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'published_at': item['snippet']['publishedAt']
            }
            videos.append(video)

        # Json 개발용 데이터 저장 -> videos만 추출해서 저장
        videos = []
        for item in data.get('items', []):
            video = {
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'published_at': item['snippet']['publishedAt']
            }
            videos.append(video)
        with open(os.path.join(DEV_DATA_DIR, VIDEO_DATA_FILE), 'w', encoding='utf-8') as f:
            json.dump(videos, f, ensure_ascii=False, indent=4)

        # 검색결과 전체 데이터 저장
        with open(os.path.join(DEV_DATA_DIR, 'search_result.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return jsonify({'code': 200, 'videos': videos}), 200

    except requests.exceptions.RequestException as e:
        print(f"YouTube API Request error: {e}")
        return jsonify({'code': 502, 'message': 'YouTube API 요청 실패'}), 502

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'code': 500, 'message': '서버 오류가 발생했습니다.'}), 500