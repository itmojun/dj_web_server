#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
import os
import urllib.parse

web_root_path = "./wwwroot"  # 指定一个用于存放所有网页文件的路径，即所谓的Web服务器根目录

def web_serve(sock_conn):
    req = sock_conn.recv(1024)
    req = req.decode()
    print(req)

    path_args = req.split("\r\n")[0].split(" ")[1]
    path_args = urllib.parse.unquote(path_args)  # URL解码
    path_args = path_args.split("?")
    path = path_args[0]
 
    if path == "/":
        file_path = os.path.join(web_root_path, "index.html")
        path = "/index.html"
    else:
        file_path = os.path.join(web_root_path, path[1:])
    
    file_ext = path.split("/")[-1].split(".")[-1]

    if file_ext in ("ico", ):
        content_type = "image/x-icon"
    elif file_ext.lower() in ("jpg", "jpeg"):
        content_type = "image/jpeg"
    elif file_ext.lower() in ("png", ):
        content_type = "image/png"
    elif file_ext.lower() in ("html", "htm"):
        content_type = "text/html; charset=UTF-8"
    elif file_ext.lower() in ("js", ):
        content_type = "text/javascript"
    elif file_ext.lower() in ("css", ):
        content_type = "text/css"

    if os.path.exists(file_path):
        rsp = "HTTP/1.1 200 Ok\r\nContent-Type: %s\r\nConnection: Close\r\nServer: dj server\r\n\r\n" % content_type
        sock_conn.send(rsp.encode())

        with open(file_path, "rb") as f:
            html_text = f.read()
        sock_conn.send(html_text)
    else:
        rsp = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nConnection: Close\r\nServer: dj server\r\n\r\n"
        sock_conn.send(rsp.encode())

        file_path = os.path.join(web_root_path, "404.html")
        with open(file_path, "rb") as f:
            html_text = f.read()
        sock_conn.send(html_text)

    sock_conn.close()


sock_listen = socket.socket(type=socket.SOCK_STREAM)

sock_listen.bind(("0.0.0.0", 9999))

sock_listen.listen(5)

while True:
    sock_conn, client_addr = sock_listen.accept()
    print(client_addr, "已连接！")
    threading.Thread(target=web_serve, args=(sock_conn, )).start()
