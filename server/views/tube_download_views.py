import os
import subprocess
from flask import Blueprint, jsonify, render_template, redirect, send_file, url_for, request
from pytube import YouTube
from config import DOWNLOAD_PATH, FILE_TYPE
from tube_downloader.yt_dl import get_all_format, get_audio_format_only
from yt_dlp import YoutubeDL

# from request_analysis.demography import get_demography

bp = Blueprint('download', __name__, url_prefix='/download')


@bp.route('/check_downloadable', methods=['POST'])
def check_downloadable():
    '''다운로드 가능한 주소인지 확인하고 해당 결과를 리턴'''
    params = request.json
    url = params['url']
    # print(f'youtube url: {url}')
    
    try:
        ydl = YoutubeDL()
        info_dic = ydl.extract_info(url, download=False)
    except Exception as e:
        print(f'\nerror: {e}')
            
    downloadables = get_all_format(url)
    
    # print(f'str(request.remote_addr): {str(request.remote_addr)}')
    
    data = {
        'code': '200' if downloadables else '400',
        'files': downloadables,
        'title': info_dic.get('title'),
        'thumbnail_url': info_dic.get('thumbnail'),
        'duration': info_dic.get('duration_string'),
        'video_id':info_dic.get('id'),
        'filesize_approx': info_dic.get('filesize_approx'),
        'is_live': info_dic.get('live_status')
    }
    return jsonify(data)

    
@bp.route('/downloading', methods=['POST'])
def downloading():
    '''요청 받은 파일을 생성하여 다운로드 - yt_dlp 활용 버전'''
    params =  request.json
    url = params['url']
    index = int(params['index'])
    video_idx = int(params['video_idx'])
    file_type = str(params['type'])
    file_type = FILE_TYPE.get(file_type)
    file_size = int(params['file_size'])
    info_dic = YoutubeDL().extract_info(url, download=False)
    video_title = info_dic.get('title')
    resolution = info_dic.get('resolution')
    
    
    # print(f'url: {url}')
    # print(f'index: {index}')
    # print(f'video_idx: {video_idx}')
    # print(f'file type: {file_type}')
    # print(f'file size: {file_size}')
    
    # 객체 생성 및 필요한 정보 추출
    m4a_audio = get_audio_format_only(url)
    audio_idx = m4a_audio.get('id')
    
    # 안전한 파일 이름으로 변경
    video_title = video_title.replace(',', '_').replace('#', '_').replace(' ', '')
    
    try:
        if file_type == 'optimal':
            cmd = f'yt-dlp -f best -o "./download/{video_title}_({resolution}).%(ext)s" {url}'
            file_name = f'{video_title}_({resolution}).mp4'
        elif file_type == 'mp4':
            cmd = f'yt-dlp -f {video_idx}+{audio_idx} -o "./download/{video_title}_({resolution}).%(ext)s" {url}'
            file_name = f'{video_title}_({resolution}).mp4'
        elif file_type == 'm4a':
            cmd = f'yt-dlp -f {audio_idx} -o "./download/{video_title}.%(ext)s" {url}'
            file_name = f'{video_title}.m4a'
        elif file_type == 'mp3':
            cmd = f'yt-dlp -x --audio-format mp3 -o "./download/{video_title}.%(ext)s" {url}'
            file_name = f'{video_title}.mp3'
    except Exception as e:
        print(f'Error occurred: {e}')
    
    
    result = os.system(cmd)
    print(f'output_path: {os.path.join(DOWNLOAD_PATH, file_name)}')
    
    data = {
        'code': '200' if result == 0 else '400',
        'output_path': DOWNLOAD_PATH,
        'file_name': file_name,        
        'file_path': os.path.join(DOWNLOAD_PATH, file_name),
        'error':'',
    }
    
    return jsonify(data)

@bp.route('/request_file', methods=['GET','POST'])
def request_file():
    '''사용자 요청에 따라 파일 전송'''
    file_path =  request.args.get('file')
    filename = file_path.split('/')[-1]
    # print(f'request_file(file_path) >>>')
    # print(f'file_path: {file_path}')
    # print(f'filename: {filename}')
    return send_file(
            path_or_file=file_path,
            as_attachment=True,
            download_name=filename,
        )
    