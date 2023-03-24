import os
import hashlib
from secret import db, seed_for_secret, BASE_DIR

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{db["user"]}:{db["passwd"]}@{db["host"]}:{db["port"]}/{db["database"]}?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create secrete key
SECRET_KEY = hashlib.sha256(seed_for_secret.encode()).hexdigest()

# Video download path
DOWNLOAD_PATH = os.path.join(BASE_DIR, 'download')

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
    (' ', '_'),
    ('/', '_'),
    (r'\\', '_'),
    ('"', ''),
    ("'", ''),
}

# 접속자의 기기 환경
# DEVICE_TYPE = {
#     'mobile': 1,
#     'tablet': 2,
#     'pc': 3,
#     'bot': 4
# }