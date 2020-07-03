import os.path
from os import listdir

import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
# import ssl

import sqlite3

from passlib.hash import pbkdf2_sha256

from ForEx import PlotCanvas

# standard settings for web server
hostName = "192.168.1.126"
serverPort = 8080

# Lubuntu
# index_file = os.path.join('/home', 'manuel', 'forex', 'index.html')
# main_folder = os.path.join('/home', 'manuel', 'forex')

# win
index_file = os.path.join('C:\\', 'Users', '41799', 'WebstormProjects', 'test', 'index.html')
main_folder = os.path.join('C:\\', 'Users', '41799', 'PycharmProjects', 'ForeignExchange', )


class MyServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.post_data = None
        self.image_path = None
        self.no_access_code = 200

    def do_GET(self):
        if self.path == '/favicon.ico':
            # no favicon available at the moment
            pass

        elif os.path.splitext(self.path)[1] == '.png':
            # get response for image
            self.send_response(200)
            self.send_header('Content-type', 'img/png')
            self.end_headers()

            f = open(self.path[1:], 'rb')
            self.wfile.write(f.read())
            f.close()

        elif os.path.splitext(self.path)[1] == '.html':
            # serve html requests
            self.send_response(200)
            self.send_header('Content-type', 'html')
            self.end_headers()

            html_path = os.path.dirname(index_file) + self.path
            f = open(html_path, encoding="utf8")
            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()

        elif len(os.path.splitext(self.path)[1]) != 0:
            # serve download requests
            self.send_response(200)
            self.send_header('Content-type', os.path.splitext(self.path)[1])
            self.end_headers()

            f = open(main_folder + self.path, 'rb')
            self.wfile.write(f.read())
            f.close()

        else:
            # standard get response (index file)
            f = open(index_file, encoding="utf8")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()

    def do_POST(self):
        # parse and retrieve properties from post
        length = int(self.headers['Content-Length'])

        # login or plot request
        self.post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        if 'bc1' not in self.post_data:
            self.login_request()
            return

        elif 'bc1' in self.post_data:
            self.data_request()
            return

    def data_request(self):
        self.image_path = str(PlotCanvas(post_data=self.post_data))

        # send standard response
        self.send_response(200)
        self.end_headers()

        # create output for response with image
        f = open(index_file, encoding="utf8")
        self.wfile.write(bytes(f.read()[:-16], "utf-8"))
        f.close()

        # if no option was enabled by the client or no image was processed
        try:
            self.wfile.write(bytes('\n<div class="container">', "utf-8"))
            self.wfile.write(bytes('\n<a href="' + self.image_path + '" download><img src="' + self.image_path +
                                   '" class="img-fluid" alt="exchange rates image"></a>', "utf-8"))

            # end html file with correct endings (otherwise not working on firefox)
            self.wfile.write(bytes("\n</div>", "utf-8"))
            self.wfile.write(bytes("\n</body>", "utf-8"))
            self.wfile.write(bytes("\n</html>", "utf-8"))
        except AttributeError:
            self.send_response(400)
            self.end_headers()
            return

    def login_request(self):
        connection = sqlite3.connect('Properties/users.db')
        cursor = connection.cursor()

        try:
            pass_db = cursor.execute('SELECT password FROM users WHERE username=?', [self.post_data['username'][0]])
        except KeyError:
            # if no username was given
            connection.close()

            self.no_access_code = 403
            self.no_access()
            return

        try:
            pass_hash = pass_db.fetchone()[0]
            connection.close()
            try:
                if pbkdf2_sha256.verify(self.post_data['password'][0], pass_hash):
                    self.send_response(200)
                    self.end_headers()

                    self.access()

                else:
                    # if wrong password was entered
                    connection.close()
                    self.no_access_code = 403
                    self.no_access()
                    return

            except KeyError:
                # if no password was given
                connection.close()
                self.no_access_code = 403
                self.no_access()
                return

        except TypeError:
            # if no valid username was given
            connection.close()
            self.no_access_code = 418
            self.no_access()
            return

    def no_access(self):
        self.send_response(self.no_access_code)
        self.end_headers()

        f = open(os.path.dirname(index_file) + '\\development.html', encoding="utf-8")
        self.wfile.write(bytes(f.read(), "utf-8"))
        f.close()

    def access(self):
        f_access = open(os.path.dirname(index_file) + '\\development_access.html', encoding="utf-8")
        output_start = f_access.read()
        f_access.close()

        self.wfile.write(bytes(output_start[:-22], "utf-8"))

        output = '<table class="table table-striped  table-hover">\n<thead>\n<tr>\n<th scope="col">Filename</th>\n<th '\
                 'scope="col">Size (bytes)</th>\n</tr>\n</thead>\n<tbody>\n'

        path = 'C:\\Users\\41799\\PycharmProjects\\ForeignExchange'
        files = [f for f in listdir(path) if os.path.isfile(os.path.join(path, f))]

        for file in files:
            if os.path.isfile(file):
                filename_path, file_extension = os.path.splitext(file)
                filename = os.path.basename(filename_path) + file_extension
                output += '<tr><td><a href="' + filename + '" download>' + filename + '</a></td><td>' + \
                          str(os.path.getsize(filename)) + '</td></tr>\n'
        output += '\n</tbody>\n</table>\n</div>\n</body>\n</html>'

        self.wfile.write(bytes(output, "utf-8"))


if __name__ == "__main__":
    # start web server with handler
    webServer = HTTPServer((hostName, serverPort), MyServer)

    # connect with ssl (lubuntu only)
    # webServer.socket = ssl.wrap_socket(webServer.socket, keyfile="/home/manuel/forex/SSL/key",
    #                                    certfile="/home/manuel/forex/SSL/certificate", server_side=True)

    # exec(open("updateData.py").read()) # update data before server start
    # print("data up to date")

    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # by keyboard events like Ctrl + C
    print("Server stopped.")
    webServer.server_close()
