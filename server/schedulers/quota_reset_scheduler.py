# server/schedulers/quota_reset_scheduler.py
# 다른 예약 작업(예: 캐시 삭제, 통계 저장 등)을 추가할 때도 확장하는 모듈입니다.

from apscheduler.schedulers.background import BackgroundScheduler
import atexit

def create_quota_scheduler(reset_func, interval_hour=0, interval_minute=0):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=reset_func, trigger="cron", hour=interval_hour, minute=interval_minute)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return scheduler
