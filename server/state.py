# server/state_quota.py

from server.models import QuotaStatus
from server import db
from datetime import datetime, timezone

def get_quota() -> int:
    quota = QuotaStatus.query.first()
    if not quota:
        quota = QuotaStatus(remaining=10_000)
        db.session.add(quota)
        db.session.commit()
    return quota.remaining


def reduce_quota(amount=100):
    quota = QuotaStatus.query.first()
    if quota:
        quota.remaining = max(0, quota.remaining - amount)
        quota.last_updated = datetime.now(timezone.utc)
        db.session.commit()


def reset_quota():
    quota = QuotaStatus.query.first()
    if not quota:
        quota = QuotaStatus(remaining=10_000)
        db.session.add(quota)
    else:
        quota.remaining = 10000
    quota.last_updated = datetime.now(timezone.utc)
    db.session.commit()
