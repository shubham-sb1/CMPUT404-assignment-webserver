#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import os


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.p = self.data.decode("utf-8").split()[1]
        print ("Got a request of: %s\n" % self.data)
        # self.request.send(bytearray("OK",'utf-8'))



        if self.data.decode("utf-8").split()[0]!= "GET":
            self.request.send(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))

        elif self.data.decode("utf-8").split()[0] == "GET":
            if '/..' in self.p:
                response = os.getcwd() + '/www' +self.p
                ct = "Content-Type: text/html\r\n\r\n"
                self.request.send(bytearray("HTTP/1.1 404 Page Not Found\r\n" + ct,'utf-8'))

            elif self.p[-1] == "/":
                try:
                    response = os.getcwd() + "/www" + self.p +"index.html"
                    ct = "Content-Type: text/html\r\n\r\n"
                    File = open(response,"r")
                    Content = File.read()
                    self.request.send(bytearray( "HTTP/1.1 200 OK\r\n"+ ct + Content,'utf-8'))
                except:
                    ct = "Content-Type: text/html\r\n\r\n"
                    self.request.send(bytearray("HTTP/1.1 404 Page Not Found\r\n" + ct,'utf-8'))
            elif self.p[-4:] == '.css':
                try:
                    response = os.getcwd() + '/www' + self.p
                    ct = "Content-Type: text/css\r\n\r\n"
                    File = open(response,"r")
                    Content = File.read()
                    self.request.send(bytearray("HTTP/1.1 200 OK\r\n" + ct + Content,'utf-8'))
                except:
                    ct = "Content-Type: text/html\r\n\r\n"
                    self.request.send(bytearray("HTTP/1.1 404 Page Not Found\r\n"+ ct,'utf-8'))


            elif self.p[-5:] == '.html':
                try:
                    response = os.getcwd() + '/www' + self.p
                    ct = "Content-Type: text/html\r\n\r\n"
                    File = open(response,"r")
                    Content = File.read()
                    self.request.send(bytearray("HTTP/1.1 200 OK\r\n" + ct + Content,'utf-8'))
                except:
                    ct = "Content-Type: text/html\r\n\r\n"
                    self.request.send(bytearray("HTTP/1.1 404 Page Not Found\r\n"+ ct,'utf-8'))
            else:
                try:
                    response = os.getcwd() + '/www' + self.p + "/index.html"
                    ct = "Content-Type: text/html\r\n\r\n"
                    File = open(response,"r")
                    Content = File.read()
                    # ct = "Content-Type: text/html\r\n"
                    Location = f'Location: {self.p}/ \r\n'
                    header = "HTTP/1.1 301 Moved Permanently\r\n"
                    self.request.send(bytearray( header + ct + Location,'utf-8'))
                except:
                    ct = "Content-Type: text/html\r\n\r\n"
                    header = "HTTP/1.1 404 Page Not Found\r\n" 
                    self.request.send(bytearray(header + ct,'utf-8'))
 



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


