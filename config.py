# /home/workspace/web-apps/yt_downloader/config.py

import os
import hashlib
from secret import seed_for_secret
from pathlib import Path

# MySQL 사용할 경우
# from secret import db, BASE_DIR
# SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{db["user"]}:{db["passwd"]}@{db["host"]}:{db["port"]}/{db["database"]}?charset=utf8'

# SQLite 사용하는 경우
# BASE_DIR = os.path.dirname(__file__)
# path_to_db = os.path.join(BASE_DIR, 'yt_downloader.db')
# SQLALCHEMY_DATABASE_URI = f'sqlite:///{path_to_db}'
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# create secrete key
# SECRET_KEY = hashlib.sha256(seed_for_secret.encode()).hexdigest()

# Video download path
# DOWNLOAD_PATH = os.path.join(BASE_DIR, 'download')


# 프로젝트 루트 절대경로를 코드에서 안전하게 계산
BASE_DIR = Path(__file__).resolve().parent

# 데이터 디렉터리(권장): ./data  (없으면 만들어 쓰자)
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # 폴더만 생성 (파일은 SQLite가 생성)

# SQLite DB 절대경로 (오타 수정: yt_downloader.db)
SQLALCHEMY_DATABASE_URI = f"sqlite:///{(DATA_DIR / 'yt_downloader.db').as_posix()}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create secret key
SECRET_KEY = hashlib.sha256(seed_for_secret.encode()).hexdigest()

# Video download path
DOWNLOAD_PATH = (BASE_DIR / 'download').as_posix()


# File type index
FILE_TYPE = {
    '1': 'mp4',
    '2': 'm4a',
    '3': 'mp3',
    '4': 'optimal',
}

# 안전한 파일 이름으로 변경 - file_name 특수문자 처리 처리
REG_REPLACE = {
    (',', '_'),
    ('#', '_'),
    ('/', '_'),
    (r'\\', '_'),
    (' ', '_'),
    ('"', '_'),
    ("'", '_'),
    ("?", '_'),
    ("&", '_'),
    ("+", '_'),
    ("|", '_'),
}

# 접속자의 기기 환경
# DEVICE_TYPE = {
#     'mobile': 1,
#     'tablet': 2,
#     'pc': 3,
#     'bot': 4
# }

# 유튜브 검색 관련 설정
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
MAX_SEARCH_RESULTS = 10     # 검색 결과 최대 개수
SIMILARITY_THRESHOLD = 0.6  # 유사도 기준