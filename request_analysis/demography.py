import json
import re
import requests
import socket
from urllib.parse import urlparse
from flask import request

class PacketAnalyzer:
    def __init__(self, url:str) -> None:
        self.url = url

    def check_numeric_url(self, url_string:str):
        check = f'\d+.\d+.\d.+.\d'
        pattern = re.compile(check)
        result = pattern.match(url_string)
        return True if result else False
    
    def get_demography(self, ip: str):
        '''Args: ip -> must be string of numeric IP'''
        url = f'https://ipinfo.io/{ip}/json'
        response = requests.get(url)
        data = json.loads(response.text)
        result = {
            'ip': data.get('ip'),
            'city': data.get('country'),
            'region':data.get('region'),
            'country': data.get('country'),
            'org': ' '.join(data.get('org').split(' ')[1:]),
        }
        return result

    def get_ip(self, url:str) -> str:
        '''Convert domain name -> numeric IP address'''
        hostname = socket.gethostbyname(urlparse(url).hostname)
        if hostname:
            return f'{hostname}'
        return ''
            

    def get_host_name(self, url:str) -> str:
        '''숫자 형태의 ip 주소 -> domain name
        For example, '223.130.195.200' -> 'https://www.naver.com'
        '''
        host_ip = socket.gethostbyname(url)
        return f'{host_ip}'


    def analyzer(self,) -> dict:
        '''접속자 통계를 위한 정보 파싱(parsing)'''
        numeric_ip = self.check_numeric_url(self.url)
        ip = self.url
        if not numeric_ip:
            ip = self.get_ip(self.url)
        result = self.get_demography(ip)
        print(result)
        return result
        
class ClientDeviceAnalyzer:
    def __init__(self, client_request: request) -> dict:
        self.client_request = client_request
    
    def analyzer(self,):
        '''ref: 
        - stackoverflow -> https://stackoverflow.com/questions/9878020/how-do-i-get-the-user-agent-with-flask
        - ua-parser -> https://github.com/ua-parser/uap-python
        '''
        
            
        
if __name__=='__main__':
    
    url = 'https://realpython.com/'
    pa = PacketAnalyzer(url=url)
    pa.analyzer()
    
    
