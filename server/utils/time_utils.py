# server/utils/time_utils.py

def seconds_to_hhmmss(seconds: int) -> str:
    """초 단위를 HH:MM:SS 또는 MM:SS 문자열로 변환"""
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}" if h > 0 else f"{m:02}:{s:02}"