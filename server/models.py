from server  import db

class VisitData(db.Model):
    '''Packet analysis data'''
    id = db.Column(db.Integer, primary_key=True) 
    url = db.Column(db.String(500), nullable=True)
    ip = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    org = db.Column(db.String(100), nullable=True)
    platform = db.Column(db.String(100), nullable=True)
    browser = db.Column(db.String(100), nullable=True)
    version = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(100), nullable=True)

class DownloadData(db.Model):
    '''Download data'''
    id = db.Column(db.Integer, primary_key=True) 
    referrer = db.Column(db.String(500), nullable=True) # 다운로드 요청 클라이언트 url
    yt_url = db.Column(db.String(500), nullable=True)   # Youtube url
    yt_title = db.Column(db.String(500), nullable=True) # Youtube title
    yt_type = db.Column(db.String(50), nullable=True)   # download type (ex: mp4, m4a, mp3)
    yt_size = db.Column(db.String(50), nullable=True)   # download size in Megabyte
    yt_resolution = db.Column(db.String(50), nullable=True) # resolution (ex: 10)
    