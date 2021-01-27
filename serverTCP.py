import threading
import socket
import sys
import os
import time

class ServerTCP :
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = []
        self.data = ''
    
    def startServer(self, IP, port, receiveFunc):      
        # Bind the socket to the port
        #os.system('fuser -k '+ str(port)+'/tcp')
        self.server_address = (IP, port)
        print('starting up on {} port {}'.format(*self.server_address))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        # Listen for incoming connections
        self.sock.listen(3)
        # Wait for a connection
        print('waiting for a connection')
        while True:
            #connection, client_address = self.sock.accept()
            serverThread = threading.Thread(target=receiveFunc,args=self.sock.accept())
            serverThread.start()
            if port == 2550:
                print('breaking')
                break

    def startServer1(self, IP, port):        
        # Bind the socket to the port
        os.system('fuser -k '+ str(port)+'/tcp')
        server_address = (IP, port)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)
        # Listen for incoming connections
        self.sock.listen(2)
        conn, addr = self.sock.accept()
        return conn
       
    
    def receive(self,conn):
        #while(True):         
        currentRunningServer = (conn.recv(32)).decode("utf-8") 
        self.data = currentRunningServer
        return currentRunningServer

    def getData(self):
        return self.data







