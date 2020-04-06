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
# ループして接続を待ち続ける
while True:
    # クライアント = ブラウザ
    # クライアントから接続される
    client,address = tcp_server.accept()
    print("[*] Connected!! [ Source : {}]".format(address))
    # クライアントからデータを受信する
    data = client.recv(buffer_size)
    print("[*] Received Data : {}".format(data))
    requestdata = data.decode('utf-8')
    print(requestdata)
    if requestdata.startswith("GET /hoge"):
        client.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhoge")
    elif requestdata.startswith("GET /huga"):
        client.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhuga")
    elif requestdata.startswith("GET /form"):
        response = b"""
<form method=\"post\" action=\"/form\">
<input type=\"text\" name=\"input1\" />
<input type=\"text\" name=\"input2\" />
<input type=\"submit\" />
</form>
        """
        client.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"+response)
    elif requestdata.startswith("POST /form"):
        formdata = requestdata.split("\r\n\r\n")[1]
        print("formdata =", formdata)
        inputdata = formdata.split("=")[1]
        print("inputdata =", inputdata)
        client.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\npost")
    else:
        client.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhello world")

    
    
    # 接続を終了させる(ctrl + C)
    client.close()