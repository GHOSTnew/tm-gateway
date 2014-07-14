#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyleft 2014 GHOSTnew 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socks
import socket
import ssl
import asyncore
import asynchat
from threading import Thread
import security
import random
import os

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

def getOnion():# currently useless 
    onion = ["oghzthm3fgvkh5wo.onion"] # currently useless 
    return random.choice(onion)

class proxy_server (asyncore.dispatcher):
    
    def __init__ (self, _SSL=False):
        asyncore.dispatcher.__init__ (self)
        self.ssl = _SSL
        if self.ssl:
            here = ('', 6697)
        else:
            here = ('', 6667)
        if self.ssl:
           s= socket.socket()
           s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
           s =  ssl.SSLSocket(s, "my.key", "my.crt", True)
           self.set_socket(s)
        else:
            self.create_socket (socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
        self.bind (here)
        self.listen (5)

    def handle_accept (self):
        sockAccept = self.accept()
        conn, addr = sockAccept
        if security.IPisBanned(addr[0]):
            conn.send("ERROR :Closing link: (user@" + str(addr[0]) + ") [Error you are banned: " + security.getReason(addr[0]) + "]\r\n")
            conn.close()
        else:
            conn.send("Welcome on our network, please help us to maintain the clearnet access\nOur Dogecoin address : \002DMP3meY5fy2ydX45qyXoexw1oLKkSpJYbG\r\n")
            proxy_receiver (self, sockAccept, self.ssl)

class proxy_sender (asynchat.async_chat):

    def __init__ (self, receiver, _SSL=False):
        asynchat.async_chat.__init__ (self)
        self.receiver = receiver
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
        socket.socket = socks.socksocket
        self.tsock = socket.socket()
        self.buffer = ''
        self.ssl = _SSL
        self.nick = None

    def connect(self):
        if self.ssl == True:
            self.tsock.connect((getOnion(), 6697))
            try:
                self.tsock = ssl.wrap_socket(self.tsock)
                self.tsock.do_handshake()
            except:
                if self.nick:
                  self.receiver.push(":Info!r00t@r00t NOTICE " + self.nick + "  :\002[\0034-\003]\002 Failed to do ssl handshake")
        else:
            self.tsock.connect((getOnion(), 6667))
    def recv(self):
        while True:
            block = self.tsock.recv(1024)
            if not block:
               break
            self.buffer += block
            while self.buffer.find('\n') != -1:
                line, self.buffer = self.buffer.split('\n', 1)
                self.receiver.push(line + "\n")
    
    def send(self, msg):
        self.tsock.send(msg + '\r\n')
    
    def setnick(self, nick):
        self.nick = nick
    def die(self):
        self.tsock.close()

class proxy_receiver (asynchat.async_chat):

    def __init__ (self,server, (conn, addr), _SSL=False):
        asynchat.async_chat.__init__ (self, conn)
        self.set_terminator ('\r\n')
        if _SSL:
            self.sender = proxy_sender(self,True)
        else:
            self.sender = proxy_sender(self)
        self.sender.connect()
        Thread(target=self.sender.recv).start()
        self.buffer = ''

    def collect_incoming_data (self, data):
        self.buffer = self.buffer + data
        
    def found_terminator (self):
        data = self.buffer
        self.buffer = ''
        if data.find('NICK') != -1:
          arg = data.split(" ")
          if len(arg) <= 2:
            self.sender.setnick(arg[1])
        self.sender.send (data)

    def handle_close (self):
         self.sender.die()
         self.close()

if __name__ == "__main__":
    if os.path.isfile("my.crt") and os.path.isfile("my.key"):
        f = open("tm_gateway.pid", "w")
        f.write(str(os.getpid()))
        f.close()
        proxy_server()
        proxy_server(True)
        asyncore.loop()
    else:
        print "Error les certificats sont introuvable"
        print "Utiliser : ./genSSLcert.sh"
        print "Pour les générer"
