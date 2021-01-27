import threading
import socket
import sys
import time
import os

class TCPClient :
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._opened = -1 
        self.port = 0
        self.data = ''
        
    def connectToServer(self,IP,port):
        # Connect the socket to the port where the server is listening
        print('connecting to {} port {}'.format(IP,port))
        while(True):
            server_address = (IP, port)
            self.port = port
            self._opened = self.sock.connect_ex(server_address)
            if (self._opened == 0):
                print('connecting to {} port {} has been successful'.format(IP,port))
                break
            #print(self.isConnected())   
        
    def disconnectFromServer(self):
        #self.sock.shutdown()   
        self._opened = -1
        self.sock.close()
        TCPClient.freeServerAddress(self.port)
        #os.system('fuser -k '+ str(self.port)+'/tcp')
    
    def isDisconnected(self):
        return self.sock._closed
    
    def isConnected(self):
        return self._opened

    def receive(self):
        while True:
            if self.isConnected() == 0 and self.isDisconnected() == False:
                self.data = self.sock.recv(16).decode("utf-8")
                if(self.data != ''):   
                    print('received {!r} from {}'.format(self.data,self.port))    

    def send(self,msg):
        if self.isConnected() == 0 and self.isDisconnected() == False:
            message = msg  
            try: 
                self.sock.sendall(message.encode())
            except:
                pass

    @staticmethod
    def freeServerAddress(port):
        os.system('fuser -k '+ str(port)+'/tcp')
                
