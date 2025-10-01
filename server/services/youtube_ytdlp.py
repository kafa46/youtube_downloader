# server/services/youtube_ytdlp.py

from datetime import datetime
import yt_dlp
from server.utils.time_utils import seconds_to_hhmmss
from config import MAX_SEARCH_RESULTS


def fetch_youtube_ytdlp(query: str) -> list[dict] | None:
    """
    yt-dlp를 이용하여 YouTube 검색 결과를 가져옵니다.
    실패 시 None을 반환합니다.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    search_url = f"ytsearch{MAX_SEARCH_RESULTS}:{query}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            result = []
            for video in info.get('entries', []):
                upload_date = video.get('upload_date')  # 문자열 "YYYYMMDD"
                if upload_date:
                    # ISO 포맷으로 변환
                    try:
                        published_at = datetime.strptime(upload_date, "%Y%m%d").isoformat()
                    except ValueError:
                        published_at = None
                else:
                    published_at = None

                video_info = {
                    'title': video.get('title'),
                    'video_id': video.get('id'),
                    'url': f"https://www.youtube.com/watch?v={video.get('id')}",
                    'duration': seconds_to_hhmmss(video.get('duration', 0)),
                    'thumbnail': video.get('thumbnail'),
                    'channelTitle': video.get('uploader', '알 수 없음'),
                    'publishedAt': published_at
                }
                result.append(video_info)
            return result

    except Exception as e:
        print(f"❌ yt-dlp 검색 실패: {e}")
        return None
