# gunicorn.conf.py

import multiprocessing

bind = "0.0.0.0:5000"
workers = 1
worker_class = "eventlet"
threads = 1

timeout = 120
keepalive = 5

loglevel = "info"
accesslog = "-"
errorlog = "-"

# 앱 엔트리포인트 (run_server.py 에서 app을 가져옴)
# 이건 CLI에서 설정하면 됨. 여기선 안 써도 됨
