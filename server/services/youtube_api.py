# server/services/youtube_api.py

import requests
from config import YOUTUBE_API_URL, MAX_SEARCH_RESULTS
from secret import YOUTUBE_API_KEY


def fetch_youtube_api(query: str) -> list[dict] | None:
    """
    YouTube Data API를 통해 검색 결과를 가져옵니다.
    실패 시 None을 반환합니다.
    """
    try:
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': MAX_SEARCH_RESULTS,
            'key': YOUTUBE_API_KEY
        }

        response = requests.get(YOUTUBE_API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        result = []
        for item in data.get('items', []):
            result.append({
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'duration': "00:00",  # 🔧 나중에 videos.list로 업그레이드 예정
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'channelTitle': item['snippet'].get('channelTitle', '알 수 없음'),
                'publishedAt': item['snippet'].get('publishedAt', None)
            })
        return result

    except Exception as e:
        print(f"❌ YouTube API 호출 실패: {e}")
        return None
