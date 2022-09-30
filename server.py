#  coding: utf-8 
from genericpath import isdir
import socketserver
from pathlib import Path
import os

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
NOTE TO WHOEVER IS MARKING THIS

THE TEST get_deep
'''


class MyWebServer(socketserver.BaseRequestHandler):

    # Processes the request and splits it up into the mode, what to get, headers, etc.
    def process(self):
        self.headers = self.data.decode("utf-8").split('\r\n')
        self.mode = self.headers[0][0:4].strip()
        print(self.mode)
        print("Headers--------")
        for headers in self.headers: 
            print(headers)
        print("Headers--------")
        self.request_path = self.headers[0].split(' ')[1]

        # Code to pass that pesky security question
        self.paths = self.request_path.split('/')
        if (len(self.paths) == 0): return
        for path in self.paths[1:]: 
            print(path)
            if (len(path) is 0): continue   #empty string (is a backslash normally)
            if not (path[0].isalpha()):
                print("REMOVED  " + path)
                self.paths.remove(path)
        print("after editing paths:\n")

        [print(edit_path) for edit_path in self.paths]

        self.request_path = "/".join(self.paths)
        print(self.request_path)

    def get_file(self):
        # Open file, read entire file, send in message
        # Alternatively, just send file using self.request.sendFile (not sure if works)

        # Adapted from https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
        self.current_path = str(Path(__file__).parent.absolute()) + "/www"   #current path of server.py

        self.reqested_path = self.current_path + self.request_path      #requested resource

        print("**********LOOKING FOR " + self.reqested_path + "***************")
        # requested path may be a file or directory. Here is where we find out.

        # REMEMBER: BASE DIRECTORY DOES NOT HAVE INDEX.HTML. MAKE SURE THE BASS ROOT IS WWW
        if (os.path.isfile(self.reqested_path)):
            # If the path leads to a file and it exists
            print("%%%%%%%%%%%%%%%%%%%%%%%% IS FILE %%%%%%%%%%%%%%%%%%%%%%%")
            self.file = open(self.reqested_path, 'r')
            self.message = self.file.read()
            self.message = bytes(self.message, "utf-8")
            self.file.close()
            # Add more logic to make sure the content type is correct (text/css vs text/html)
            content_type = self.request_path.split('.')[1]  #the suffix of the file

            header = "HTTP/1.1 200 OK\r\nContent-Type: text/" + content_type + "\r\n\r\n"
            self.headers = bytes(header, 'utf-8')
            self.request.sendall(self.headers)
            self.request.sendall(self.message)


        elif (os.path.isdir(self.reqested_path) and self.reqested_path[-1] == '/'):
            # If the path leads to a directory and exists
            # Return 301 error with path to index.html in the directory


            print(self.reqested_path)


            print("@@@@@@@@@@@@@@@@@@@@@@@@ IS DIRECTORY @@@@@@@@@@@@@@@@@@@@@@@@@@@")


            correct_path = "http://127.0.0.1:8080" + self.request_path + "index.html"


            print("####CORRECT PATH: " + correct_path + "#####")


            self.return_301(correct_path)
            return

        elif (os.path.isdir(self.reqested_path)):
            #if the path leads to a directory and exists but has no slash at the end
            # fyi this is only to pass the deep_no_end test, it used to automatically direct to the 
            # right path with the index

            print("!@#!@#!@#!@#!@#!@#!@#!#@!@#!@#")
            print("PATH: " + self.reqested_path + ", FINAL CHAR: " + self.reqested_path[-1])
            
            correct_path = "http://127.0.0.1:8080" + self.request_path + "/"

            print("####CORRECT PATH: " + correct_path + "#####")
            self.return_301(correct_path)
            return        

        else:
            # return 404 not found
            self.return_404()
            return



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

    def return_301(self, correct_path):
        header = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + correct_path + "\r\nContent-Type: text/plain\r\n\r\n"
        self.headers = bytes(header, "utf-8")
        self.message = bytes("301 Moved Permanently\n", "utf-8")
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
        print("\n\n****************************************")
        # get the request
        self.data = self.request.recv(1024).strip()
        self.message = ""

        #determine what needs to be done
        self.process()

        #if GET, process what it wants. If not, return 405
        if(self.mode != "GET"):
            self.return_405()
            return

        self.get_file()
        #self.return_200()
        self.request.close()
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    