#  coding: utf-8 
import socketserver
from pathlib import Path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Modified my Cameron Matthew for the assignment
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

'''
Things to figure out:
- How to properly format headers
- How to serve files
- Where to put the logic for doing what tasks need to be done (ex. sending a 405 as a return)
- Flowchart of what a server does when it gets a request
'''


class MyWebServer(socketserver.BaseRequestHandler):

    def process_mode(self):
        self.headers = self.data.decode("utf-8").split('\r\n')
        self.mode = self.headers[0][0:4].strip()
        print(self.mode)
        print("Headers--------")
        for headers in self.headers: 
            print(headers)
        print("Headers--------")
        self.request_path = self.headers[0].split(' ')[1]
        print(self.request_path)

    def get_file(self):
        # Open file, read entire file, send in message
        # Alternatively, just send file using self.request.sendFile (not sure if works)

        # Adapted from https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
        self.current_path = Path(__file__).parent.absolute()



        try:
            self.file = open(self.file_name, 'r')
        except FileNotFoundError:
            #SomethingSomething Cant find file
            self.return_404()
            return

            
        self.headers = bytes("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n", 'utf-8')
        self.message = bytes(self.file.read(), 'utf-8')
        self.request.sendall(self.headers)
        self.request.sendall(self.message)



    def return_405(self):
        self.headers = bytes("HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\n", 'utf-8')
        self.message = bytes("405 Method Not Allowed\n", 'utf-8')
        self.request.sendall(self.headers)
        self.request.sendall(self.message)
        self.request.close()

    def return_404(self):
        self.headers = bytes("HTTP/1.1 404 File Not Found\r\nContent-Type: text/plain\r\n\r\n", 'utf-8')
        self.message = bytes("404 File Not Found\n", 'utf-8')
        self.request.sendall(self.headers)
        self.request.sendall(self.message)
        self.request.close()

    def return_200(self):
        self.headers = bytes("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n", 'utf-8')
        self.message = bytes("GET IS OK\n", 'utf-8')
        self.request.sendall(self.headers)
        self.request.sendall(self.message)

    # Do all of the handling of stuff
    def handle(self):
        # get the request
        self.data = self.request.recv(1024).strip()

        #determine what needs to be done
        self.process_mode()

        #if GET, process what it wants. If not, return 405
        if(self.mode != "GET"):
            self.return_405()
            return

        #self.get_file()
        self.return_200()
        self.request.close()
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    