import fetch_save
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        '处理跨域请求'
        self.send_response(200)
        self.send_header('Allow', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'X-Request, X-Requested-With')
        self.end_headers()

    def do_POST(self):
        '接收到客户端信息的时候'
        js = fetch_save.fetch_song('wasesong.songlist.cc')
        js = js['data']['songs']
        self.reply(data=json.dumps(js))

    def reply(self, code=200, message='Mua!\n', data=''):
        '回复'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        data = {
            "code": code,
            "message": message,
            "data": data,
        }
        self.wfile.write(json.dumps(data).encode())

def main():
    addr = ("0.0.0.0", 63104)
    server = HTTPServer(addr, RequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
