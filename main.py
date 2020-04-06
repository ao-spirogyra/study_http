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
    else:
        client.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nhello world")

    # クライアントにレスポンスを送信する
    
    # 接続を終了させる(ctrl + C)
    client.close()