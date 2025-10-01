'''yt_dlp를 이용한 유튜브 다운로더
처음에는 pytube를 이용하여 구현하였으나, 에러가 계속 발생하여 yt_dlp로 변경하여 구현

2023. 3월 현재 상황
    - youtube-dl 2021년 6월 6일 이후 업데이트 없음
        Github (youtube-dl): https://github.com/ytdl-org/youtube-dl/
    - youtube-dl을 포크 하여 yt-dlp프로젝트로 계속 진행 중
        -> 대부분 yt-dlp를 youtube_dl 이라는 이름으로 임포트하면
            과거 youtube_dl 코드를 사용할 수 있음

        Comparison Dated on 2023.03.18.(Sat.)
        -------------------------------------------
        Description     youtube-dl      yt-dlp
        -------------------------------------------
        Releases        341             69
        Final release   2021.12.17.     2023.04.04.
        Contributors    789             1,105
        Stars           119k            43.1k
        -------------------------------------------

- References
    - yt_dlp ()
        - Github: https://github.com/yt-dlp/yt-dlp
        - PyPI: https://pypi.org/project/yt-dlp/
    - Related wiki KO
        - Namu wiki: https://namu.wiki/w/youtube-dl
'''

import os
from pprint import pprint
from yt_dlp import YoutubeDL

def get_yt_info(url: str) -> dict:
    '''Extract YouTube information'''
    ydl = YoutubeDL()
    info_dic = ydl.extract_info(url, download=False)
    title = info_dic.get('title')
    thumbnail = info_dic.get('thumbnail')
    duration = info_dic.get('duration_string')
    video_id = info_dic.get('id')


def get_audio_format_only(url: str) -> dict:
    """
    yt-dlp -F 출력에서 audio(m4a) 포맷 중 하나(보통 가장 작은 용량)를 골라 반환
    반환 예: {'id': '140-0', 'type': 'm4a', 'resolution': '해당없음', 'size_mb': 23.53}
    """
    cmd = f'yt-dlp -F {url}'
    lines = os.popen(cmd).read().splitlines()

    best = {}
    min_size = float('inf')

    for line in lines:
        # m4a audio only 라인만 대상
        if 'm4a' not in line or 'audio only' not in line:
            continue

        # 공백 다중 분리
        parts = [p for p in line.split(' ') if p]
        if not parts:
            continue

        fmt_id = parts[0]                 # ✅ 문자열 그대로 (예: '140-0')
        # dash/drc 등 스킵(필요시 규칙 조정)
        if 'dash' in fmt_id or 'drc' in fmt_id:
            continue

        # 크기 파싱 (MiB/GiB/KiB 모두 처리)
        size_mb = None
        for tok in parts:
            try:
                if 'MiB' in tok:
                    size_mb = float(tok.replace('MiB', '').replace('~', ''))
                elif 'GiB' in tok:
                    size_mb = float(tok.replace('GiB', '').replace('~', '')) * 1000
                elif 'KiB' in tok:
                    size_mb = float(tok.replace('KiB', '').replace('~', '')) / 1000
            except ValueError:
                pass

        if size_mb is None:
            continue

        if size_mb < min_size:
            min_size = size_mb
            best = {
                'id': fmt_id,             # ✅ int() 제거
                'type': 'm4a',
                'resolution': '해당없음',
                'size_mb': size_mb
            }

    return best

# File: tube_downloader/yt_dl.py

def get_all_format(url: str) -> list:
    """
    yt-dlp를 이용하여 다운로드 가능한 mp4/m4a 포맷 정보 추출
    """
    cmd = f'yt-dlp -F {url}'
    terminal_output = os.popen(cmd).readlines()

    download_info = []

    # ✅ mp4 비디오 목록 추출
    for line in terminal_output:
        if 'mp4' in line and 'video only' in line:
            parts = [p for p in line.split(' ') if p]
            if 'dash' in parts[0]:
                continue

            format_id = parts[0]  # 문자열 그대로 사용
            resolution = parts[2] if len(parts) > 2 else '알 수 없음'

            size = None
            for token in parts:
                try:
                    if 'MiB' in token:
                        size = float(token.replace('MiB', '').replace('~', ''))
                    elif 'GiB' in token:
                        size = float(token.replace('GiB', '').replace('~', '')) * 1000
                    elif 'KiB' in token:
                        size = float(token.replace('KiB', '').replace('~', '')) / 1000
                except ValueError:
                    continue

            if size is None:
                continue

            download_info.append({
                'id': format_id,  # 🔑 int() 변환 제거
                'type': 'mp4',
                'resolution': resolution,
                'size_mb': size
            })

    # ✅ m4a 오디오 목록에서 하나 선택
    m4a_audio = {}
    min_size = float('inf')

    for line in terminal_output:
        if 'm4a' in line and 'audio only' in line:
            parts = [p for p in line.split(' ') if p]
            if 'dash' in parts[0] or 'drc' in parts[0]:
                continue

            size = None
            for token in parts:
                try:
                    if 'MiB' in token:
                        size = float(token.replace('MiB', '').replace('~', ''))
                    elif 'GiB' in token:
                        size = float(token.replace('GiB', '').replace('~', '')) * 1000
                    elif 'KiB' in token:
                        size = float(token.replace('KiB', '').replace('~', '')) / 1000
                except ValueError:
                    continue

            if size and size < min_size:
                min_size = size
                m4a_audio = {
                    'id': parts[0],   # 🔑 문자열 그대로
                    'type': 'm4a',
                    'resolution': '해당없음',
                    'size_mb': size
                }

    # ✅ mp4 사이즈 보정
    if m4a_audio:
        for item in download_info:
            if item['type'] == 'mp4':
                item['size_mb'] += m4a_audio['size_mb']
                item['size_mb'] *= 1.1

        download_info.append(m4a_audio)

    # ✅ 정렬
    download_info = [item for item in download_info if item.get('size_mb') is not None]
    download_info = sorted(download_info, key=lambda item: item['size_mb'], reverse=True)

    pprint(download_info)
    return download_info



def get_downloadable_list(url: str, ) -> dict:
    '''Extract possible formats'''
    options = {
        '-F',
    }
    ydl = YoutubeDL(options)
    ydl.filter_requested_info()


def download_mp3(url: str, filename:str, save_path:str = './') -> None:
    # Reference: https://blog.amaorche.com/142
    result = os.system(
        f'yt-dlp --extract-audio --audio-format mp3 -o "./download/%(title)s.%(ext)s" {url}'
    )


if __name__=='__main__':
    url = 'https://youtu.be/eYtSJdQIsB4'
    get_yt_info(url)
    # download_mp3(url, 'test')
    # get_all_format(url)

