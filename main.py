import os
import sys
import socket
import mimetypes


class SimpleHTTPServer:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("Server initialized on port {} host {}".format(self.port, self.host))

    def process_request(self):

        conn, addr = self.sock.accept()
        data = conn.recv(1024)
        request = data.decode('utf-8')
        print("Received: {}".format(request))
        path = sys.path[0] + (request.split()[1] if data else '/')
        print("Path:", path)
        response = self.create_response(path)
        conn.sendall(response)
        conn.close()

    def create_response(self, path):
        headers = "HTTP/1.1 200 OK\n"

        if os.path.isdir(path):
            folder_content = os.listdir(path)

            if 'index.html' in folder_content:
                headers += 'Content-Type: text/html\n\n'
                with open(path + '/index.html', 'r') as html:
                    body = html.read()

            else:
                pass
        else:
            type = mimetypes.guess_type(path)[0]
            headers += 'Content-Type: {}\n\n'.format(type)
            with open(path, 'r') as file:
                    body = file.read()

        response = headers + body
        byte_resp = response.encode('utf-8')
        return byte_resp

    def serve_forever(self):

        while True:
            self.process_request()


host = ''

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000

if __name__ == "__main__":
    server = SimpleHTTPServer(host, port)
    server.serve_forever()
