from serverTCP import ServerTCP
import threading
from clientTCP import TCPClient 
import numpy as np
import json
from stableMemory import loadJsonFile, saveData

class ServerMachine(ServerTCP):
    REQUESTS_TO_AGREGATOR = ['GET_AGREGATOR_CONFIGURATION','GET_LAST_DATA']
    def __init__(self):
        ServerTCP.__init__(self)
        self.connections = {}
        self.last_received_data = {}
        self.agregator_list = []
        self.request_result = {}

    def receiveData(self,connection,client_address):
        try:
            print('connection from', client_address)
            while True:  
                data = (connection.recv(4096)).decode("utf-8")
                #print('data string format {}'.format(data))  
                if data != '':
                    try:
                        data = json.loads(data)
                        if data.__class__ == dict:
                            print('!!!!!!!!!!!!! {}'.format(data))  
                            if list(data.keys())[0] == 'request_index':
                                self.request_result = data
                                self.set_last_data(data['agregator_id'],data['request_result']) 
                                #request_index, agregator_id, value = data['request_index'], data['agregator_id'], data['request_result']
                                #print('request_index {}, agregator_id {}, value {}'.format(request_index, agregator_id, value))
                                continue    
                        elif data.__class__ == list:
                            agregator_id, value = data[0], data[1]
                            self.connections[agregator_id] = connection 
                            if agregator_id not in self.last_received_data.keys():
                                self.agregator_list.append(agregator_id)
                                #self.graphic_interface.update_agregator_list(self.agregator_list)
                            self.last_received_data[agregator_id] = value
                            #print('agregator id {} , value {}'.format(agregator_id, value))

                    except Exception as e:
                        print("errrrrrrrrrrrrrrrrrror {}".format(e)) 
        except:
            pass

    
    # send a specific request to a specific agregator defined by its id  
    def sendRequestToAgregator(self,request,agregator_id):
        if request in ServerMachine.REQUESTS_TO_AGREGATOR:
            req = [agregator_id,request]
            req = json.dumps(req)
            self.connections[agregator_id].sendall(req.encode())   

    def get_last_data(self,agregator_id):
        return self.last_received_data[agregator_id]
    
    def set_last_data(self,agregator_id,last_data):
        self.last_received_data[agregator_id] = last_data