from flask import Blueprint, render_template, redirect, url_for, request
from ..forms import YoutubeSearchForm

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def index():
    '''Main function'''
    form = YoutubeSearchForm()
    if request.method=='POST' and form.validate_on_submit():
        url = request.form.get('url')
        print(f'url: {url}')
        
    return render_template(
        'contents/index.html',
        context='test',
        form=form,
    )
    
# 예: main_views에 임시 추가
@bp.route("/healthz")
def healthz():
    from flask import request
    print("remote_addr:", request.remote_addr)
    return "ok"
    