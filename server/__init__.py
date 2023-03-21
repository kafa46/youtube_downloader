from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

# # Initialize Login Manager
# login_manager = LoginManager()

import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY
    
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    
    # Init LoginManager Object
    # login_manager.init_app(app)
    
    # Blue-print 등록
    from . import models
    from .views import main_views, tube_download_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(tube_download_views.bp)
    
    
    # Filters 등록
    # from .filters import format_datetime
    # app.jinja_env.filters['datetime'] = format_datetime # '%Y년 %m월 %d일 %H:%M'
    
    # 템플릿에서 continue, break 사용할 수 있도록 익스텐션 추가
    # 참고 블로그: https://blog.weirdx.io/post/53619
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')      
    return app
    
    