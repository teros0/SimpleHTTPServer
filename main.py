import os
import sys
import socket
import mimetypes
import codecs


class SimpleHTTPServer:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("Server initialized on host {} port {}".format(self.host, self.port))

    def process_request(self):

        conn, addr = self.sock.accept()
        data = conn.recv(1024)
        request = data.decode('utf-8')
        print("Received: {}".format(request))
        file_path = request.split()[1] if request else '/'
        full_path = sys.path[0] + file_path
        print("Path:", full_path)
        try:
            response = self.create_response(full_path)
            conn.sendall(response[0])
            conn.sendall(response[1])
        finally:
            conn.close()

    def create_head(self, path):

        headers = "HTTP/1.1 200 OK\n"
        if os.path.isfile(path):
            type = mimetypes.guess_type(path)[0]
            headers += 'Content-Type: {}\n\n'.format(type)
        else:
            headers += 'Content-Type: text/html\n\n'
        return headers.encode('utf-8')

    def list_dirs(self, path):
        with open(path + '.temp_index.html', 'w+') as f:
            f.write("""<!DOCTYPE html>
                        <html>
                            <title>Directory listing for {0}</title>
                            <body>
                            <h2>Directory listing for {0}</h2>
                            <hr>
                            <ul>\n""".format(path))
            for entry in os.listdir(path):
                print("ENTRIES", entry)
                if entry == '.temp_index.html':
                    continue
                entry = entry + '/' if os.path.isdir(path + entry) else entry
                f.write("<li><a href='{0}'>{0}</a>\n".format(entry))
            print("TEMPORARY FILE", f.read())
        return path + '.temp_index.html'

    def create_body(self, path, make_list):
        with open(path, 'rb') as f:
            body = f.read()
        return body

    def create_response(self, path):

        make_list = 0
        if os.path.isdir(path):
            folder_content = os.listdir(path)

            if 'index.html' in folder_content:
                path += '/index.html'
            else:
                path = self.list_dirs(path)

        headers = self.create_head(path)
        body = self.create_body(path, make_list)
        response = (headers, body)
        return response

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
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\Keyboard interruption, exiting.")
        sys.exit(0)
