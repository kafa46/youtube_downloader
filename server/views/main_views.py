from flask import Blueprint, render_template, redirect, url_for, request
from ..forms import YoutubeSearchForm

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def index():
    '''Main function'''
    form = YoutubeSearchForm()
    if request.method=='POST':
        url = request.form.get('url')
        print(f'url: {url}')
        
    return render_template(
        'contents/index.html',
        context='test',
        form=form,
    )