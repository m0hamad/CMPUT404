#  coding: utf-8 
import os # For dealing with ./www and /deep folders
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


# https://docs.python.org/3/library/socketserver.html
class MyWebServer(socketserver.BaseRequestHandler):

    def error_404_not_found(self, content):

        status_code = "HTTP/1.1 404 Not Found\r\n"
        connection = "Connection: close\r\n\r\n"
        content = ("<html>\n<body>Error 404. Sorry, could not find the following content: "
                + content
                + " </body>\n</html>")

        self.request.send((status_code + connection + content).encode("utf-8"))

    def find_content_in_directory(self, content):

        print((os.path.relpath(os.curdir) + "/www" + content))
        return (os.path.abspath(os.curdir) + "/www" + content)

        # return os.getcwd() + "/www" + content

    #As per assignment requirements, only text/html and text/css are supported
    def get_mime_type(self, content):

        #https://www.tutorialspoint.com/python/string_endswith.htm
        if content.endswith(".css"):

            return "Content-Type: text/css\r\n"
        
        elif content.endswith(".html"):
            
            return "Content-Type: text/html\r\n"

    def return_405_error(self, content, data):
        
        print("405 FOUR OH FIVE")
        status_code = "HTTP/1.1 \r\n"
        print("405 FOUR OH FIVE")
        connection = data[-1] + "\r\n\r\n"
        print("405 FOUR OH FIVE")
        #content = print("<html>\n<body 405 Method not allowed to access " + content + ". </body>\n</html>")
        content = ("<html>\n<body> {'Message' :The requested resource does not support http method 'GET'.}"
                + " </body>\n</html>")

        self.request.send((status_code + connection + content).encode("utf-8"))
        
    def send_message_response(self, content, data):

        print(content)
        new_content = open(self.find_content_in_directory(content)).read()
        print(new_content)
        status_code = "HTTP/1.1 200 OK\r\n"
        print(status_code)
        mime_type = self.get_mime_type(content)
        print(mime_type)
        accept = data[1] + "\r\n"
        print(accept)
        host = data[2] + "\r\n"
        print(host)
        user_agent = data[3] + "\r\n"
        print(user_agent)
        connection = data[-1] + "\r\n\r\n"
        print(connection)
        
        self.request.send((status_code + mime_type + accept + host + user_agent + connection + new_content).encode("utf-8"))
    
    def handle(self):

        # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
        # split using \r\n to get appropriate headers
        self.data = self.request.recv(1024).strip().decode("utf-8").split("\r\n")
        print ("Got a request of: %s\n" % self.data)

        #self.request.sendall(bytearray("OK",'utf-8))

        # Get resource type
        content = self.data[0].split(" ")[1]
        print("THIS IS THE CONTENT: ", content)


        #in_directory_content = self.find_content_in_directory(content)
        if content.endswith("/"):
            self.return_405_error(content, self.data)
            s
        elif self.get_mime_type(content):
            self.send_message_response(content, self.data)
            
        else:
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