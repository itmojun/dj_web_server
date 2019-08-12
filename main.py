#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading


def web_serve(sock_conn):
    req = sock_conn.recv(1024)
    print(req)

    rsp = "HTTP/1.1 200 Ok\r\nContent-Type: text/html; charset=UTF-8\r\nConnection: Close\r\nServer: dj server\r\n\r\n<p style=\"color: red; font-size: 100px; font-weight: bold;\">Hello,中国！</p>"

    sock_conn.send(rsp.encode())

    sock_conn.close()


sock_listen = socket.socket(type=socket.SOCK_STREAM)

sock_listen.bind(("0.0.0.0", 9999))

sock_listen.listen(5)

while True:
    sock_conn, client_addr = sock_listen.accept()
    print(client_addr, "已连接！")
    threading.Thread(target=web_serve, args=(sock_conn, )).start()
