from server import db

from flask import request
from datetime import datetime
from request_analysis.demography import PacketAnalyzer, ClientDeviceAnalyzer
from server.models import VisitData, DownloadData

def round_size(size: float, digit:int = 2):
    '''소수점 2째 자리에서 반올림 3.14 -> 3.1'''
    return round(size, digit)


def save_client_packet_info(client_request: request) -> bool:
    '''클라이언트 패킷 정보 저장'''
    # Reference -> https://blogair.tistory.com/63
    client_url = client_request.remote_addr
    print(f'client_url: {client_url}')
    client_dic = PacketAnalyzer(client_url).analyzer() # client packet info
    device_dic = ClientDeviceAnalyzer('flask').analyzer(client_request) # client device info
    
    # create db object
    vd = VisitData() 
    
    # parse from client_dic <- PacketAnalyzer
    vd.url = client_url
    vd.ip = client_dic.get('ip')
    vd.city = client_dic.get('city')
    vd.region = client_dic.get('region')
    vd.country = client_dic.get('country')
    vd.org = client_dic.get('org')
    
    # parse from device_dic <- ClientDeviceAnalyzer
    vd.browser_type = device_dic.get('browser_type')
    vd.browser_version = device_dic.get('browser_version')
    vd.os_type = device_dic.get('os_type')
    vd.os_version = device_dic.get('os_version')
    vd.device_family = device_dic.get('device_family')
    vd.device_type = device_dic.get('device_type')
    vd.user_agent_string = device_dic.get('user_agent_string')
    vd.visit_date = datetime.now()
    
    db.session.add(vd)
    
    try: 
        db.session.commit()
        print('success commit to DB')
        return True
    except Exception as e:
        print(f'Error occurred: {e}')
        return False


def save_download_status(download_status: dict) -> bool:
    '''다운로드 상태 정보 저장'''
    dt = DownloadData()
    dt.referrer = download_status.get('referrer')
    dt.yt_url = download_status.get('yt_url')
    dt.yt_title = download_status.get('yt_title')
    dt.yt_type = download_status.get('yt_type')
    dt.yt_size = download_status.get('yt_size')
    dt.yt_resolution = download_status.get('yt_resolution')
    dt.download_date = datetime.now()
    
    db.session.add(dt)
    
    try: 
        db.session.commit()
        print('success commit to DB')
        return True
    except Exception as e:
        print(f'Error occurred: {e}')
        return False

    