# server/admin_tasks/cache_admin.py

from datetime import datetime, timedelta
from server.models import SearchCache
from server import db

def delete_old_cache(months: int = 6):
    """Delete cache records older than the specified number of months."""
    cutoff = datetime.now() - timedelta(days=30*months)
    deleted = SearchCache.query.filter(SearchCache.timestamp < cutoff).delete()
    db.session.commit()
    print(f"🧹 {deleted}개의 오래된 캐시 레코드를 삭제했습니다.")


def clear_all_cache():
    """Clear all cache records."""
    try:
        deleted = SearchCache.query.delete()
        db.session.commit()
        print(f"🧹 전체 캐시 {deleted}개 삭제 완료했습니다.")
        return deleted
    except Exception as e:
        db.session.rollback()
        print(f"❌ 캐시 삭제 실패: {e}")
        return 0

