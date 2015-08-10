
import SimpleHTTPServer, BaseHTTPServer
import socket
import thread

import sys, os, shutil, glob, webbrowser

from string import Template










class StoppableHTTPServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True

    def get_request(self):
        while self.run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self.run = False

    def serve(self):
        while self.run:
            self.handle_request()






def launchWebBrowser(PORT):
    chrome = webbrowser.get('google-chrome')
    address = Template("http://localhost:$port/app").substitute(port=PORT)
    chrome.open_new(address)



def getPort():
    port = 0

    if sys.argv[1:]:

        port = int(sys.argv[1])

    else:
        port = 8000

    return port

def main():

    PORT = getPort()
    HandlerClass = SimpleHTTPServer.SimpleHTTPRequestHandler

    print PORT

    httpd = StoppableHTTPServer(("",PORT), HandlerClass)


    thread.start_new_thread(httpd.serve, ())

    launchWebBrowser(PORT)
    raw_input("press <Enter> to stop server\n")
    httpd.stop()


if __name__ == '__main__':
    main()
