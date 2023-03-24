from server  import db

class VisitData(db.Model):
    '''Packet analysis data'''
    id = db.Column(db.Integer, primary_key=True) 
    url = db.Column(db.String(500), nullable=True)      # client url
    ip = db.Column(db.String(500), nullable=True)       # client IP addr
    city = db.Column(db.String(100), nullable=True)     # client city
    region = db.Column(db.String(100), nullable=True)   # client region
    country = db.Column(db.String(100), nullable=True)  # client country
    org = db.Column(db.String(100), nullable=True)      # client organization
    
    browser_type = db.Column(db.String(100), nullable=True) 
    browser_version = db.Column(db.String(100), nullable=True)
    os_type = db.Column(db.String(100), nullable=True)
    os_version = db.Column(db.String(100), nullable=True)
    device_family = db.Column(db.String(100), nullable=True)
    device_type = db.Column(db.String(100), nullable=True)
    user_agent_string = db.Column(db.String(800), nullable=True)
    visit_date = db.Column(db.DateTime, nullable=True)


class DownloadData(db.Model):
    '''Download data'''
    id = db.Column(db.Integer, primary_key=True) 
    referrer = db.Column(db.String(500), nullable=True) # 다운로드 요청 클라이언트 url
    yt_url = db.Column(db.String(500), nullable=True)   # Youtube url
    yt_title = db.Column(db.String(500), nullable=True) # Youtube title
    yt_type = db.Column(db.String(50), nullable=True)   # download type (ex: mp4, m4a, mp3)
    yt_size_mb = db.Column(db.Integer, nullable=True)   # download size in Megabyte Integer
    yt_resolution = db.Column(db.String(50), nullable=True) # resolution (ex: 10)
    download_date = db.Column(db.DateTime, nullable=True)
    