import client
import threading
import os
import webbrowser
from config import HOST, CLIENT_PORT


class ClientServer(threading.Thread):
    def run(self):
        client.run()


def create_servers():
    # try:
    #     _thread.start_new_thread(authorization_server.run, ())
    #     _thread.start_new_thread(resource_server.run, ())
    # except BaseException as be:
    #     print(be)
    # while 1:
    #     pass
    client_thread = ClientServer()

    client_thread.start()

    return client_thread,


if __name__ == '__main__':
    servers = create_servers()

    # visit localhost:8080
    chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    url = "http://%s:%d" % (HOST, CLIENT_PORT)
    if os.path.isfile(chromepath):
        webbrowser.get("{:s} %s".format(chromepath)).open(url)
    else:
        print('Please goto %s with your favorite browser.' % url)
    [server.join() for server in servers]
