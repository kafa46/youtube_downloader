from pytube import YouTube


class MyYouTube(YouTube):
    def __init__(
        self,
        download_dir: str = './download',
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.url = url # Youtube address
        self.download_dir = download_dir

    
    def download_video(self,):
        '''동영상 다운로드
        args:
            - quality: int, 고화질, 중간화질, 저화질
            - download_f_name (str): 다운로드 파일명
        return:

        '''
        pass
    
    def download_voice(self,):
        '''음성파일 다운로드'''
    

    def send_email(self, send_from: str, send_to:str):
        '''다운로드 받은 동영상을 이메일 전송
        args:
            - send_from: 발송자 이메일()
        '''

        pass

    


if __name__=='__name__':
    url = 'https://youtu.be/AYQ7wgthGAA'