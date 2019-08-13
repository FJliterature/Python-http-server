from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/'><h2>What's your name?</h2><input type='text' name='message' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    '<html><body><h1>404</h1><br><h1>File not found......</h1></body></html>')
                return
        except:
            self.send_error(404, "File not found", self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # collect data from form

                messagecontent = fields.get('message')  # get specific datum and store in array
                output = ""
                output += "<html><body>"
                output += ("<h1 style=\'color:red;\'>" + "Welcome, " + messagecontent[0] + "</h1>")
                output += "<form method='POST' enctype='multipart/form-data' action='/'><h2>What's your name?</h2><input type='text' name='message' ><input type='submit' value='Submit'></form>"
                self.wfile.write(output)
        except:
            pass


def main():
    try:
        port = 3000
        server = HTTPServer(("", port), webserverHandler)
        print("Web server running on port: ", port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
