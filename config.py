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