from serverTCP import ServerTCP
import threading
from clientTCP import TCPClient 
import numpy as np
import json
from stableMemory import loadJsonFile, saveData


REQUESTS_TO_AGREGATOR = ['GET_AGREGATOR_CONFIGURATION','GET_LAST_DATA']

class ServerMachine(ServerTCP):
    def __init__(self):
        ServerTCP.__init__(self)
        self.last_received_data = {}
        self.agregator_list = []
        #self.graphic_interface = GUI(self.agregator_list)
        #self.graphic_interface.init_root_widgets()
        print('hello')
        

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
                            if len(data) == 3:
                                request_index, agregator_id, value = data[0], data[1], data[2]
                                #print('request_index {}, agregator_id {}, value {}'.format(request_index, agregator_id, value))
                                continue    
                            agregator_id, value = data[0], data[1] 
                            if agregator_id not in self.last_received_data.keys():
                                self.agregator_list.append(agregator_id)
                                #self.graphic_interface.update_agregator_list(self.agregator_list)
                            self.last_received_data[agregator_id] = value
                            #print('agregator id {} , value {}'.format(agregator_id, value))

                    except:
                        print("errrrrrrrrrrrrrrrrrror")
                try:
                    self.sendRequestToAgregator(REQUESTS_TO_AGREGATOR[0],connection,agregator_id)
                except:
                    print("request error")   
        except:
            pass

    
    # send a specific request to a specific agregator defined by its id  
    def sendRequestToAgregator(self,request,connection,agregator_id):
        if request in REQUESTS_TO_AGREGATOR:
            req = [agregator_id,request]
            req = json.dumps(req)
            connection.sendall(req.encode())

    def get_last_data(self,agregator_id):
        return self.last_received_data[agregator_id]
    
#server = ServerMachine()
#server.startServer('localhost',2500,server.receiveData)



    
     
