# server/views/admin_views.py

from flask import Blueprint, render_template, jsonify, redirect, url_for, flash
from datetime import datetime, timedelta
from server.models import SearchCache
from server import db
from server.state import get_quota, reset_quota


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def admin_index():
    return render_template('admin/index.html')


@bp.route('/quota/reset', methods=['POST'])
def reset_quota_admin():
    reset_quota()
    flash("✅ 크레딧이 10,000으로 초기화되었습니다.")
    return redirect(url_for('admin.admin_index'))


@bp.route('/quota')
def show_quota():
    return jsonify({'remaining_quota': get_quota()})


@bp.route('/cache')
def show_cache():
    records = SearchCache.query.order_by(SearchCache.timestamp.desc()).all()
    return render_template('admin/cache_list.html', records=records)


@bp.route('/cache/clear', methods=['POST'])
def clear_all_cache():
    deleted = SearchCache.query.delete()
    db.session.commit()
    flash(f"🧹 전체 캐시 {deleted}개 삭제 완료되었습니다.")
    return redirect(url_for('admin.show_cache'))


@bp.route('/cache/old', methods=['POST'])
def delete_old_cache():
    cutoff = datetime.utcnow() - timedelta(days=30)
    deleted = SearchCache.query.filter(SearchCache.timestamp < cutoff).delete()
    db.session.commit()
    flash(f"🧼 30일 이상 지난 캐시 {deleted}개 삭제 완료되었습니다.")
    return redirect(url_for('admin.show_cache'))