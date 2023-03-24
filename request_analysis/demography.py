import json
import re
import requests
import socket
from urllib.parse import urlparse
from flask import request
from pprint import pprint
from user_agents import parse


class PacketAnalyzer:
    '''서버 접속량 및 활용 지역 분석을 위한 패킷 정보 추출'''
    
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
        pprint(result)
        return result

        
class ClientDeviceAnalyzer:
    '''안전한 클라이언트인지 -> 접속 정보를 확인하여 리턴 
        주의: 'client_request' 파라미터는 반드시 
              flask에서 지원하는 'request' 객체이어야 함.
              'Django'의 'request' 객체일 경우 별도 메서드로 구현해야 함.
    '''
    
    def __init__(self, web_framework: str = 'flask') -> None:
        self.web_framework = web_framework
    

    def analyzer(self, client_request: request)-> dict:
        '''ref: 
        - stackoverflow -> https://stackoverflow.com/questions/9878020/how-do-i-get-the-user-agent-with-flask
        - ua-parser -> https://github.com/ua-parser/uap-python
        - ua 보는 법 -> https://wormwlrm.github.io/2021/10/11/Why-User-Agent-string-is-so-complex.html
        '''
        
        if self.web_framework == 'flask':
            '''플라스크 프레임워크를 사용하는 경우'''
            ua_string = client_request.user_agent.string
            ua = parse(ua_string)
            
            # check mobile type
            device_type = None
            if ua.is_mobile:
                device_type = 'mobile'
            elif ua.is_tablet:
                device_type = 'tablet'
            elif ua.is_pc:
                device_type = 'pc'
            elif ua.is_bot:
                device_type = 'bot'
            
            
            client_data = {
                'browser_type': ua.browser.family,
                'browser_version': ua.browser.version_string,
                'os_type': ua.os.family,
                'os_version': ua.os.version_string,
                'device_family': ua.device.family,
                'device_brand': ua.device.brand,
                'device_type': device_type,
                'user_agent_string': ua_string,
            }
            pprint(client_data)
            return client_data
        
        elif self.web_framework == 'django':
            '''장고 프레임워크를 사용하는 경우 
                -> 향후 코딩 추가 영역...
            '''
            pass


if __name__=='__main__':
    url = 'https://realpython.com/'
    pa = PacketAnalyzer(url=url)
    pa.analyzer()
    
    
