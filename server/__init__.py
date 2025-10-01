# ''' server/__init__.py '''

# import eventlet
# eventlet.monkey_patch()

# import config

# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import CSRFProtect
# from flask_socketio import SocketIO

# db = SQLAlchemy()
# migrate = Migrate()
# csrf = CSRFProtect()

# # async_mode는 생성 시 한 번만 명시
# socketio = SocketIO(cors_allowed_origins='*', async_mode='eventlet')

# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)
#     app.config.from_object(config)
#     app.secret_key = config.SECRET_KEY

#     db.init_app(app)
#     migrate.init_app(app, db, render_as_batch=True)

#     # Blue-print 등록
#     from . import models
#     from .views import main_views, tube_download_views
#     app.register_blueprint(main_views.bp)
#     app.register_blueprint(tube_download_views.bp)


#     # Filters 등록
#     # from .filters import format_datetime
#     # app.jinja_env.filters['datetime'] = format_datetime # '%Y년 %m월 %d일 %H:%M'

#     # 템플릿에서 continue, break 사용할 수 있도록 익스텐션 추가
#     # 참고 블로그: https://blog.weirdx.io/post/53619
#     app.jinja_env.add_extension('jinja2.ext.loopcontrols')

#     # Refence on Flask-SocketIO documentation - 맨 아래 부분 참고
#     # https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent/page/16
#     # socketio.init_app(app, debug=True, cors_allowed_origins='*', async_mode='eventlet')
#     socketio.init_app(app)  # debug, async_mode는 생략

#     return app


#  server/__init__.py
import eventlet
eventlet.monkey_patch()

import config

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_socketio import SocketIO
from werkzeug.middleware.proxy_fix import ProxyFix # Flask가 nginx → gunicorn 뒤에 있어서 실제 접속자의 IP 대신 프록시 서버의 IP만 보이는 문제 해결

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

# async_mode는 생성 시 한 번만 명시
socketio = SocketIO(cors_allowed_origins='*', async_mode='eventlet')

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY

    # 플러그인 초기화
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    socketio.init_app(app)  # debug, async_mode는 생략

    # ✅ ProxyFix 적용 (nginx → gunicorn 뒤에 있을 때 클라이언트 실제 IP 사용)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    # 블루프린트 등록
    from . import models
    from .views import (
        main_views,
        tube_download_views,
        tube_search_views,
        admin_views,
    )
    app.register_blueprint(main_views.bp)
    app.register_blueprint(tube_download_views.bp)
    app.register_blueprint(tube_search_views.bp)
    app.register_blueprint(admin_views.bp)

    # 템플릿 필터와 옵션 설정
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    return app
