from serverTCP import ServerTCP
import threading
from clientTCP import TCPClient 
import numpy as np
import json
from stableMemory import loadJsonFile, saveData

class ServerMachine(ServerTCP):
    def __init__(self):
        ServerTCP.__init__(self)
        self.last_received_data = {}

    #def store_acquired_data(self, path, newDataVector, mean):
    #    saveData(path, newDataVector, mean)

    def receiveData(self,connection,client_address):
        try:
            print('connection from', client_address)
            while True:  
                data = (connection.recv(4096)).decode("utf-8")
                #print('data string format {}'.format(data))  
                if data != '':
                    try:  
                        data = json.loads(data)
                        if data.__class__ == list:
                            agregator_id, value = data[0], data[1] 
                            self.last_received_data[agregator_id] = value
                            print('agregator id {} , value {}'.format(agregator_id, value))
                            #self.sendRequestToAgregator('Turnofffff',agregator_id)
                    except:
                        print("errrrrrrrrrrrrrrrrrror")   
        except:
            pass

    def sendRequestToAgregator(self,request,agregator_id):
        req = [agregator_id,request]
        req = json.dumps(req)
        self.sock.sendall(req.encode())
    
server = ServerMachine()
server.startServer('localhost',2500,server.receiveData)



    
     
