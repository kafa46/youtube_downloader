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


def get_audio_format_only(url:str) -> dict:
    '''m4a 파일 정보만 추출하여 리턴'''
    cmd = f'yt-dlp -F {url}'
    terminal_output = os.popen(cmd).readlines()
    m4a_audio_only = [x for x in terminal_output if 'm4a' in x and 'audio only' in x]
    m4a_audio_only = [x.split(' ') for x in m4a_audio_only]
    m4a_audio_only = [[word for word in word_list if word!=''] for word_list in m4a_audio_only]
    m4a_audio = {}
    audio_size_mb = float('-inf')
    for word_list in m4a_audio_only:
        if 'dash' in word_list[0]:
            continue
        size = None
        for x in word_list:
            if 'MiB' in x:
                size = float(x.replace('MiB', '').replace('~', ''))     
            elif 'GiB' in x:
                size = float(x.replace('GiB', '').replace('~', '')) * 1000
            elif 'KiB' in x:
                size = float(x.replace('KiB', '').replace('~', '')) / 1000                   
        if size > audio_size_mb:
            m4a_audio['id'] = int(word_list[0])
            m4a_audio['type'] = 'm4a'
            m4a_audio['resolution'] = '해당없음'
            m4a_audio['size_mb'] = size
    return m4a_audio

def get_all_format(url: str) -> list:
    ''' yt-dlp 옵션을 이용하여 다운로드 가능한 파일 리스트 추출
    -F, --list-formats   
        List available formats of each video. 
        Simulate unless --no-simulate is used
    '''
    cmd = f'yt-dlp -F {url}'
    terminal_output = os.popen(cmd).readlines()
    
    # 식별한 다운로드 가능 객체 정보를 리스트에 저장
    download_info = []
    
    # 터미널 출력 비디오 정보(text) 처리해서 저장
    mp4_video_only = [x for x in terminal_output if 'mp4' in x and 'video only' in x]
    mp4_video_only = [x.split(' ') for x in mp4_video_only]
    mp4_video_only = [[word for word in word_list if word!=''] for word_list in mp4_video_only]
    for word_list in mp4_video_only:
        if 'dash' in word_list[0]:
            continue        
        size = None
        for x in word_list:
            if 'MiB' in x:
                size = float(x.replace('MiB', '').replace('~', ''))
            elif 'GiB' in x:
                size = float(x.replace('GiB', '').replace('~', '')) * 1000
            elif 'KiB' in x:
                size = float(x.replace('KiB', '').replace('~', '')) / 1000
        download_info.append(
            {
                'id': word_list[0],
                'type': 'mp4',
                'resolution': word_list[2],
                'size_mb': size
            }
        )
    
    # 고화질 순서대로 정렬 
    download_info = sorted(download_info, key=lambda item: item['size_mb'], reverse=True)
    
    # 오디오 용량이 가장 큰 파일을 찾아서 저장
    m4a_audio_only = [x for x in terminal_output if 'm4a' in x and 'audio only' in x]
    m4a_audio_only = [x.split(' ') for x in m4a_audio_only]
    m4a_audio_only = [[word for word in word_list if word!=''] for word_list in m4a_audio_only]
    
    m4a_audio = {}
    audio_size_mb = float('inf')
    for word_list in m4a_audio_only:
        if 'dash' in word_list[0]:
            continue
        size = None
        for x in word_list:
            if 'MiB' in x:
                size = float(x.replace('MiB', '').replace('~', ''))
            elif 'GiB' in x:
                size = float(x.replace('GiB', '').replace('~', '')) * 1000
            elif 'KiB' in x:
                size = float(x.replace('KiB', '').replace('~', '')) / 1000                
        if size < audio_size_mb:
            m4a_audio['id'] = int(word_list[0])
            m4a_audio['type'] = 'm4a'
            m4a_audio['resolution'] = '해당없음'
            m4a_audio['size_mb'] = size
    
    # 추출한 정보를 리스트에 추가
    download_info.append(m4a_audio)
    
    # 예상되는 다운로드 사이즈 -> video_size + voice_size + overhead (10%)
    for x in download_info:
        if x['type'] == 'mp4':
            x['size_mb'] += m4a_audio['size_mb']
            # increase size 20% out of original file size
            x['size_mb'] = x['size_mb'] + x['size_mb'] * 0.1
    # pprint(download_info)
    
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
    
