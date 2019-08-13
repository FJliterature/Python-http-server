import http.server
import socketserver
import cgi


class webserverHandler(http.server.BaseHTTPRequestHandler):
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
                self.wfile.write(output.encode("utf-8"))
                # print(output)
                return
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    '<html><body><h1>404</h1><br><h1>File not found.....</h1></body></html>'.encode("utf-8"))
                return
        except:
            self.send_error(404, "File not found", self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            print("yes1")
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type').decode('utf-8'))
            print("yes2")
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # collect data from form
                messagecontent = fields.get('message')  # get specific datum and store in array

                output = ""
                output += "<html><body>"
                output += "<h2> Welcome: </h2>"
                output += ("<h1>", messagecontent[0].deocde('utf-8'), "</h1>")
                output += "<form method='POST' enctype='multipart/form-data' action='/'><h2>What's your name?</h2><input type='text' name='message' ><input type='submit' value='Submit'></form>"
                self.wfile.write(output.encode("utf-8"))
                print(output)
        except:
            pass


def main():
    try:
        port = 7777
        server = socketserver.TCPServer(("", port), webserverHandler)
        print("Web server running on port: ", port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
