# server/utils/cache.py

import json
import difflib
from server.models import SearchCache
from server import db

# 유사도 비교 함수
def compute_similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

# 검색어로 캐시 조회 (정확 일치 또는 유사 검색)
def load_from_cache(query):
    try:
        record = SearchCache.query.filter(SearchCache.query_string == query).first()
        if record:
            print(f"🔵 정확 일치 캐시 히트: '{query}'")
            return json.loads(record.response_json)

        all_records = SearchCache.query.all()
        if not all_records:
            return None

        similarities = [
            (compute_similarity(query, rec.query), rec)
            for rec in all_records
        ]
        similarities.sort(reverse=True, key=lambda x: x[0])

        best_match, best_record = similarities[0]

        if best_match >= 0.6:
            print(f"🟡 유사 캐시 히트: 입력 '{query}' vs 저장 '{best_record.query}' (유사도 {best_match:.2f})")
            return json.loads(best_record.response_json)
        
        return None

    except Exception as e:
        print(f"❌ 캐시 조회 오류: {e}")
        return None

# 검색어와 결과를 캐시에 저장
def save_to_cache(query_string, videos):
    try:
        json_data = json.dumps(videos, ensure_ascii=False)
        record = SearchCache(
            query_string=query_string, 
            response_json=json_data
        )
        db.session.merge(record)  # INSERT or UPDATE
        db.session.commit()
        print(f"📝 캐시 저장: '{query_string}'")
    except Exception as e:
        db.session.rollback()
        print(f"❌ 캐시 저장 오류: {e}")
