# server/views/tube_search_views.py

from flask import Blueprint, request, jsonify
from server import socketio
from server.schedulers.quota_reset_scheduler import create_quota_scheduler
from server.services.youtube_api import fetch_youtube_api
from server.services.youtube_ytdlp import fetch_youtube_ytdlp
from server.utils.cache import load_from_cache, save_to_cache
from server.state import reset_quota, reduce_quota, get_quota


bp = Blueprint('youtube_search', __name__, url_prefix='/search')

# 스케줄러 등록
create_quota_scheduler(reset_quota)


# YouTube 검색 라우트
@bp.route('/search', methods=['GET'])
def search_youtube():
    query = request.args.get('query')
    socket_id = request.args.get('socket_id')  # ✅ socket_id 수신
    print(f"Received search query: {query}")
    print(f"socket_id: {socket_id}")

    if not query:
        return jsonify({'code': 400, 'message': '검색어를 입력해 주세요.'}), 400

    query = query.strip()

    try:
        # 1. 캐시 먼저 조회
        cached_videos = load_from_cache(query)
        if cached_videos:
            return jsonify({'code': 200, 'videos': cached_videos}), 200

        # 2. API 사용 또는 yt-dlp fallback
        videos = None
        if get_quota() >= 100:  # 여기! 직접 quota 조회
        # if get_quota() >= 1000000:  # 여기! 직접 quota 조회
            print("✅ Using YouTube Data API...")
            videos = fetch_youtube_api(query)
            if videos is not None:
                reduce_quota()
            else:
                print("⚠️ API 결과 없음, yt-dlp fallback 사용")
                videos = fetch_youtube_ytdlp(query)
        else:
            print("⚡ API 크레딧 부족, yt-dlp 사용")

            # quota 소진 시 클라이언트에게 알려주기
            socketio.emit("yt_status", {
                "status": "info",
                "message": "😮YouTube 무료 호출량을 초과했어요.\n\n자체 개발한 🔥 엔진으로 전환할게요^^.\n30초 이상 오래 걸릴 수 있어요.😂"
            }, to=socket_id)

            videos = fetch_youtube_ytdlp(query)

            # emit("yt_status", {
            #     "status": "done",
            #     "message": "다운로드 완료!"
            # }, to=socket_id)

        if not videos:
            print("❌ 유튜브 API 및 yt-dlp 모두 실패")
            return jsonify({'code': 502, 'message': '검색 결과를 가져올 수 없습니다.'}), 502

        # 3. 캐시에 저장
        save_to_cache(query, videos)

        return jsonify({'code': 200, 'videos': videos}), 200

    except Exception as e:
        print(f"❌ 검색 처리 오류: {e}")
        return jsonify({'code': 500, 'message': '서버 오류가 발생했습니다.'}), 500
