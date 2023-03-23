import re
import json
from urllib.parse import urlparse
# from urllib3 import PoolManager
import requests
import socket
import ipaddress
import sys


def get_demography(ip: str):
    '''Args
        ip: must be string of numeric IP
    '''
    url = f'https://ipinfo.io/{ip}/json'
    response = requests.get(url)
    print(response)
    data = json.loads(response.text)
    result = {
        'ip': data.get('ip'),
        'city': data.get('country'),
        'region':data.get('region'),
        'country': data.get('country'),
        'org': ' '.join(data.get('org').split(' ')[1:]),
    }
    print(result)
    return result

def get_ip(url:str) -> str:
    '''Convert domain name -> numeric IP address'''
    hostname = socket.gethostbyname(urlparse(url).hostname)
    # print(f'Domain name: {url}')
    # print(f'IP: {hostname}')
    if hostname:
        return f'{hostname}'

def get_host_name(url:str) -> str:
    '''숫자 형태의 ip 주소 -> domain name
    For example, '223.130.195.200' -> 'https://www.naver.com'
    '''
    host_ip = socket.gethostbyname(url)
    return f'{host_ip}'

if __name__=='__main__':
    
    url = 'https://portal.cju.ac.kr/'
    ip = get_ip(url)
    
    # ip = '223.130.195.200'
    host_name = get_host_name(ip)
    
    get_demography(ip)
