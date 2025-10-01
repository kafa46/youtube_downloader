# server/views/tube_download_views.py

from asyncio import sleep
import os
import shutil
from subprocess import Popen, PIPE, STDOUT
import re
import tempfile
from flask import Blueprint, jsonify, render_template, redirect, send_file, url_for, request
from flask_socketio import emit

from config import DOWNLOAD_PATH, FILE_TYPE, REG_REPLACE
from server import socketio
from server.utils.download_utils import save_client_packet_info, save_download_status
from server.utils.sanitizer_utils import sanitize_json_or_dict, sanitizer
from tube_downloader.yt_dl import get_all_format, get_audio_format_only
from yt_dlp import YoutubeDL

bp = Blueprint('download', __name__, url_prefix='/download')

@bp.route('/check_downloadable', methods=['POST'])
def check_downloadable():
    params = request.json
    url = sanitizer(params['url'])
    try:
        ydl = YoutubeDL()
        info_dic = ydl.extract_info(url, download=False)
    except Exception as e:
        print(f'\nerror: {e}')
        return jsonify({'code': '400', 'error': str(e)})

    downloadables = get_all_format(url)
    data = {
        'code': '200' if downloadables else '400',
        'files': downloadables,
        'title': info_dic.get('title'),
        'thumbnail_url': info_dic.get('thumbnail'),
        'duration': info_dic.get('duration_string'),
        'video_id': info_dic.get('id'),
        'filesize_approx': info_dic.get('filesize_approx'),
        'is_live': info_dic.get('live_status')
    }

    save_ok = save_client_packet_info(request)
    data['db_stored'] = 'True' if save_ok else 'False'

    return jsonify(data)

@bp.route('/downloading', methods=['POST'])
@bp.route('/downloading', methods=['POST'])
def downloading():
    # 0) 파라미터 파싱
    params_original = request.get_json(force=True) or {}
    params = sanitize_json_or_dict(params_original)
    socket_id = params_original.get("socket_id")

    url = params.get('url', '').strip()
    if not url:
        return jsonify({'code': '400', 'error': 'url missing'}), 400

    # ✅ 포맷 ID는 무조건 문자열로 (하이픈 포함 가능)
    video_idx = str(params.get('video_idx', '')).strip()
    file_type = FILE_TYPE.get(str(params.get('type')))
    try:
        file_size_approx_from_js = int(params.get('file_size', 0))
    except Exception:
        file_size_approx_from_js = 0

    if not file_type:
        return jsonify({'code': '400', 'error': 'invalid type'}), 400

    # 1) 메타 및 파일명
    info_dic = YoutubeDL().extract_info(url, download=False)
    video_title = (info_dic.get('title') or 'video').strip()
    resolution = info_dic.get('resolution') or 'audio'

    for old, new in REG_REPLACE:
        video_title = video_title.replace(old, new)

    # 2) 오디오 포맷 추출 (문자열 ID)
    m4a_audio = get_audio_format_only(url) or {}
    audio_idx = str(m4a_audio.get('id', '')).strip()

    # (선택) 간단한 화이트리스트 검증
    import re
    FORMAT_ID_RE = re.compile(r'^[0-9A-Za-z_.:-]*$')
    if video_idx and not FORMAT_ID_RE.fullmatch(video_idx):
        return jsonify({'code': '400', 'error': 'invalid video format id'}), 400
    if audio_idx and not FORMAT_ID_RE.fullmatch(audio_idx):
        return jsonify({'code': '400', 'error': 'invalid audio format id'}), 400

    # 3) -f 인자와 출력 템플릿(절대경로) 구성
    if file_type == 'mp4':
        if not video_idx:
            return jsonify({'code': '400', 'error': 'video format id missing'}), 400
        if not audio_idx:
            return jsonify({'code': '400', 'error': 'audio format not found'}), 400
        fmt = f'{video_idx}+{audio_idx}'
        file_name = f'{video_title}_({resolution}).mp4'
        out_tmpl = os.path.join(DOWNLOAD_PATH, f'{video_title}_({resolution}).%(ext)s')
        popen_cmd = ['yt-dlp', '-f', fmt, '-o', out_tmpl, url]

    elif file_type == 'm4a':
        fmt = audio_idx or video_idx
        if not fmt:
            return jsonify({'code': '400', 'error': 'audio format id missing'}), 400
        file_name = f'{video_title}.m4a'
        out_tmpl = os.path.join(DOWNLOAD_PATH, f'{video_title}.%(ext)s')
        popen_cmd = ['yt-dlp', '-f', fmt, '-o', out_tmpl, url]

    elif file_type == 'mp3':
        fmt = audio_idx or video_idx
        if not fmt:
            return jsonify({'code': '400', 'error': 'audio format id missing'}), 400
        file_name = f'{video_title}.mp3'
        out_tmpl = os.path.join(DOWNLOAD_PATH, f'{video_title}.%(ext)s')
        popen_cmd = ['yt-dlp', '-x', '--audio-format', 'mp3', '-o', out_tmpl, url]

    else:
        fmt = video_idx or audio_idx
        if not fmt:
            return jsonify({'code': '400', 'error': 'no valid format id'}), 400
        file_name = f'{video_title}.mp4'
        out_tmpl = os.path.join(DOWNLOAD_PATH, f'{video_title}.%(ext)s')
        popen_cmd = ['yt-dlp', '-f', fmt, '-o', out_tmpl, url]

    # ✅ 정수/소수 모두 매칭
    progress_pattern = re.compile(r"\[download\]\s+(\d{1,3}(?:\.\d+)?)%")

    progress_info = {
        'download_type': file_type,
        'current_ext': None,
        'progress': 0,
        'status': 'preparing',
        'file_name': file_name
    }
    if socket_id:
        socketio.emit('progress', progress_info, to=socket_id)

    # 4) 실행 + 진행률 파싱
    try:
        result = 1
        with Popen(popen_cmd, stdout=PIPE, stderr=STDOUT, text=True, bufsize=1) as process:
            for line in process.stdout:
                m_ext = re.search(r'Destination:\s+.+(\.\w+)$', line)
                if m_ext:
                    progress_info['current_ext'] = m_ext.group(1)

                m = progress_pattern.search(line.strip())
                if m:
                    progress_info['progress'] = m.group(1)
                    progress_info['status'] = 'downloading'
                    if socket_id:
                        socketio.emit('progress', progress_info, to=socket_id)

            result = process.wait()
    except Exception as e:
        progress_info['status'] = 'error'
        if socket_id:
            socketio.emit('complete', progress_info, to=socket_id)
        return jsonify({'code': '400', 'error': str(e)})

    progress_info['status'] = 'completed' if result == 0 else 'error'
    if socket_id:
        socketio.emit('complete', progress_info, to=socket_id)

    # 5) 결과 저장
    file_path = os.path.join(DOWNLOAD_PATH, file_name)
    try:
        file_size_real = int(os.path.getsize(file_path) / (1000 * 1000))
    except Exception as e:
        print(f'filesize read error: {e}')
        file_size_real = -1

    save_download_status({
        'referrer': sanitizer(request.remote_addr),
        'yt_url': sanitizer(url),
        'yt_title': sanitizer(video_title),
        'yt_type': file_type,
        'yt_size_mb': file_size_real,
        'yt_resolution': resolution,
    })

    return jsonify({'code': '200', 'file_path': file_path, 'file_name': file_name})

@bp.route('/request_file', methods=['GET'])
def request_file():
    file_path = request.args.get('file')
    file_name = file_path.split('/')[-1]
    final_path = os.path.join(DOWNLOAD_PATH, file_name)

    cache = tempfile.NamedTemporaryFile()
    with open(final_path, 'rb') as fp:
        shutil.copyfileobj(fp, cache)
        cache.flush()
    cache.seek(0)
    os.remove(final_path)

    return send_file(cache, as_attachment=True, download_name=file_name)

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)
