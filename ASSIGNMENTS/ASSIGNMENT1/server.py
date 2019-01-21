#  coding: utf-8 
import os # For dealing with ./www folder
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

# try: curl -v -X GET http://127.0.0.1:8080/nc local


# https://docs.python.org/3/library/socketserver.html
class MyWebServer(socketserver.BaseRequestHandler):

    def error_404_not_found(self, content):

        status_code = "HTTP/1.1 404 Not Found\r\n"
        connection = "Connection: close\r\n\r\n"
        body = ("<html>\n<body>404 - Sorry, could not find the following content: "
                + content
                + " </body>\n</html>")

        self.request.send((status_code + connection + body).encode("utf-8"))

    def find_content_in_directory(self, content):

        pass

    #As per assignment requirements, only text/html and text/css are supported
    def get_mime_type(self, content):

        #https://www.tutorialspoint.com/python/string_endswith.htm
        if content.endswith(".css"):

            return "Content-Type: text/css"
        
        elif content.endswith(".html"):
            
            return "Content-Type: text/html"

    def send_message_response(self, content):

        pass
    
    def handle(self):

        # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
        # split using \r\n to get appropriate headers
        self.data = self.request.recv(1024).strip().decode("utf-8").split("\r\n")
        print ("Got a request of: %s\n" % self.data)

        #self.request.sendall(bytearray("OK",'utf-8'))

        content = self.data[0].split(" ")[1]
        #in_directory_content = self.find_content_in_directory(content)

        self.error_404_not_found(content)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print("Starting server...")
    server.serve_forever()