'''run_server.py'''

import sys
import eventlet
import argparse
eventlet.monkey_patch()
from server import create_app, socketio


def parser() -> argparse.ArgumentParser:
    """
    ArgumentParser 객체를 생성하고, --debug 인자를 추가합니다.
    :return: ArgumentParser 객체
    """
    p = argparse.ArgumentParser(description='Flask-SocketIO 서버 실행')
    p.add_argument('--debug', '-d', action='store_true', help='디버그 모드 실행 (default: False)')
    return p.parse_args()

try:
    app = create_app()
except Exception as e:
    print(f"🚨 create_app() 오류: {e}")
    sys.exit(1)  # 반드시 종료


if __name__=='__main__':
    args = parser()
    if args.debug:
        print("🔧 [개발 모드] Flask-SocketIO 서버 실행 중 (http://localhost:5050)")
        socketio.run(
            app=app,
            host="0.0.0.0",
            port=5050,
            debug=True,
            use_reloader=True  # 개발 중 자동 재시작 허용
        )
    else:
        print("🚀 [운영 모드] Flask-SocketIO 서버 실행 중 (http://0.0.0.0:5050)")
        socketio.run(
            app=app,
            host="0.0.0.0",
            port=5050,
            debug=False,
            use_reloader=False
        )