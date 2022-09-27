#  coding: utf-8 
import socketserver

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
    
    def handle(self):
        
        self.data = self.request.recv(1024).strip()
        process_request(self)
        
        self.message = bytes("reply", 'utf-8')
        self.headers = bytes("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n", 'utf-8')
        self.request.sendall(self.headers)
        
        self.request.sendall(self.data)
        #self.send_response(200)
        self.request.close()
        
        
#determine what needs to be done
def process_request(self):
    self.data = self.request.recv(1024).strip()
    self.moder = self.data.decode("utf-8")
    print(self.moder)
        
        
#find and serve the file (200)
def serve_file(self):
    self.data
    
#if the file cannot be found (404 error)
def file_not_found_response(self):
    self.data
    
#correct wrong path (301 error)
def fix_path_ending(self):
    self.data
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    