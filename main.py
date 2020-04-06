# -*- coding : UTF-8 -*-
# ライブラリのインポートと変数定義
import socket
# サーバーのIPアドレス
server_ip = "127.0.0.1"
# サーバーのポート
server_port = 8080
listen_num = 5
buffer_size = 1024
# ソケットオブジェクトの作成
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 作成したソケットオブジェクトにIPアドレスとポートを紐づける
tcp_server.bind((server_ip, server_port))
# 作成したオブジェクトを接続可能状態にする
tcp_server.listen(listen_num)

class NotImplementedPath:
    def get(self, req, res):
        res.send(b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nnot implemented")
    def post(self, req, res):
        res.send(b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nnot implemented")

class DefaultPath(NotImplementedPath):
    def get(self, req, res):
        res.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhello world")

class HogePath(NotImplementedPath):
    def get(self, req, res):
        res.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhoge")

class HugaPath(NotImplementedPath):
    def get(self, req, res):
        res.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhuga")

class FormPath(NotImplementedPath):
    def get(self, req, res):
        resstr = b"""
            <form method=\"post\" action=\"/form\">
            <input type=\"text\" name=\"input1\" />
            <input type=\"text\" name=\"input2\" />
            <input type=\"submit\" />
            </form>
        """
        res.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"+resstr)
    def post(self, req, res):
        formdata = req.split("\r\n\r\n")[1]
        print("formdata =", formdata)
        inputdata1 = formdata.split("&")[0].split("=")[1]
        inputdata2 = formdata.split("&")[1].split("=")[1]
        output = "inputdata1 = {}, inputdata2 = {}".format(inputdata1, inputdata2)
        print(output)
        res.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{}".format(output).encode('utf-8'))

routes = {
    "/"     : DefaultPath,
    "/hoge" : HogePath,
    "/huga" : HugaPath,
    "/form" : FormPath
}

# ループして接続を待ち続ける
while True:
    # クライアント = ブラウザ
    # クライアントから接続される
    res, address = tcp_server.accept()
    print("[*] Connected!! [ Source : {}]".format(address))
    # クライアントからリクエストデータを受信する
    reqraw = res.recv(buffer_size)
    if len(reqraw) == 0:
        continue
    req = reqraw.decode('utf-8')
    # リクエストデータからパス、メソッドを得る
    firstline = req.split('\r\n')[0]
    method = firstline.split(' ')[0]
    path = firstline.split(' ')[1]
    # パス、メソッドを元にクラス、メソッドを呼び出す
    clazz = routes.get(path, None)
    if clazz is not None:
        print(clazz.__name__)
        pathclazz = clazz()
    else:
        pathclazz = NotImplementedPath()
    func = getattr(pathclazz, method.lower())
    func(req, res)
    # 接続を終了させる(ctrl + C)
    res.close()

