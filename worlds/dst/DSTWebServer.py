from http.server import BaseHTTPRequestHandler, HTTPServer
import codecs
import json
import time

import logging
from typing import Any

interfacelog = logging.getLogger("DSTInterface")

hostName = "localhost"
serverPort = 8000

authname = "Nil"
authip = "Nil"
authpassword = "Nil"
authdirty = False
receivequeue = []
sendqueue = []
connected = False
serverstopsignel = False

lastping = time.time()
frozencheck = time.time()

class DSTServer(BaseHTTPRequestHandler):
    def log_error(self, format, *args):
        interfacelog.info("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def log_message(self, format, *args): #Just put a sock in it, and I mean that in the kindest way possible :3
        pass
        
    def do_POST(self):
        global sendqueue, authname, authip, authdirty, authpassword, lastping
        lastping = time.time()

        # response = None
        # interfacelog.info("Reading data...")
        # data = codecs.decode(self.rfile.read(-1))[0:] #Why is rfile.read so slow!!!
        data = ""
        currentline = 1
        while True:
            newdata = codecs.decode(self.rfile.readline(currentline))
            newdata
            if newdata.endswith("EOF"):
                newdata = newdata[:-3]
                data += newdata
                break
            else:
                data = data + newdata
            currentline += 1
        data = json.loads(data)

        datatype = dict.get(data, "datatype")
        if datatype == "Ping":
            if connected is not False:
                if sendqueue.__len__() > 0:
                    self.send_response(100)
                    self.end_headers()
                    event = sendqueue.pop(0)
                    # print(event)
                    self.wfile.write(bytes(event, "utf-8"))
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(bytes("Pong!", "utf-8")) # This line does nothing, it's just here out of formality
            else:
                self.send_response(100)
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"datatype": "State", "connected": False}), "utf-8"))
        else:
            if (datatype == "Chat" or datatype == "Join" or datatype == "Leave" or 
                datatype == "Death" or datatype == "Item" or datatype == "Hint"):

                receivequeue.append(data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes("Receaved " + datatype + " Signel", "utf-8"))
            elif datatype == "Connect":
                authname = dict.get(data, "name")
                authip = dict.get(data, "ip")
                authpassword = dict.get(data, "password")
                authdirty = True
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes("Receaved Connect Signel", "utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
            
        # interfacelog.info("Done reading data.")

#Why do I do this instead of something like import? because I tried it and couldn't get it to work.
def getvariables(): 
    return {'authname': authname,
            'authip': authip,
            'authpassword': authpassword,
            'authdirty': authdirty,
            'receivequeue': receivequeue,
            'sendqueue': sendqueue,
            'connected': connected,
            'serverstopsignel': serverstopsignel,
            'lastping': lastping,
            'frozencheck': frozencheck,
            }

#Why do I do this instead of something like import? because I tried it and couldn't get it to work.
def setvariables(dict: dict): 
    global authname, authip, authpassword, authdirty, receivequeue, sendqueue, connected, serverstopsignel, lastping, frozencheck
    authname = authname if dict.get('authname') is None else dict.get('authname')
    authip = authip if dict.get('authip') is None else dict.get('authip')
    authpassword = authpassword if dict.get('authpassword') is None else dict.get('authpassword')
    authdirty = authdirty if dict.get('authdirty') is None else dict.get('authdirty')
    receivequeue = receivequeue if dict.get('receivequeue') is None else dict.get('receivequeue')
    sendqueue = sendqueue if dict.get('sendqueue') is None else dict.get('sendqueue')
    connected = connected if dict.get('connected') is None else dict.get('connected')
    serverstopsignel = serverstopsignel if dict.get('serverstopsignel') is None else dict.get('serverstopsignel')
    lastping = lastping if dict.get('lastping') is None else dict.get('lastping')
    frozencheck = frozencheck if dict.get('frozencheck') is None else dict.get('frozencheck')

# def stopserver():
#     global serverstopsignel
#     serverstopsignel = True

def startWebServer():
    webServer = HTTPServer((hostName, serverPort), DSTServer)
    interfacelog.info("Started DST WebServer http://%s:%s" % (hostName, serverPort))

    while serverstopsignel != True and not (time.time() - frozencheck > 5):
        webServer.handle_request()
    if time.time() - frozencheck > 5:
        interfacelog.info("WebServer: Seems the client has frozen, panicing and shutting down!")
    else:
        interfacelog.info("WebServer: Client has told us to shut down, as they wish.")


