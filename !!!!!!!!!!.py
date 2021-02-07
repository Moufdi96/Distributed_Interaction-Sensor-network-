from serverTCP import ServerTCP
from clientTCP import TCPClient
from clientTCP import TCPClient
from datetime import datetime
import socket
import threading
import json
import time
from stableMemory import loadJsonFile, saveData

REQUESTS_TO_SENSOR = ['TURN_OFF','TURN_ON','SET_RATE']
REQUESTS_FROM_SERVER = ['GET_AGREGATOR_CONFIGURATION','GET_LAST_DATA']


class AggregatorAgent(ServerTCP):
    def __init__(self,id):
        ServerTCP.__init__(self)
        self.aggregator_id = id
        self.path_sensor_metaData = '/home/moufdi/GitHubProjects/Projet_interaction_distribuee/' + str(id) + '.json'
        self.sensors_list = loadJsonFile(self.path_sensor_metaData)
        self.client = TCPClient() # to communicate with the server
        self.sensor_data = {}
        self.connection_to_server = self.ConnectionToServer(self.aggregator_id,self.sensors_list,self.sensor_data)
        #self.connection_to_server.startTransmissionToServer()
        #self.sendToServer_thread = None
        #self.receptionFromServer_thread = None
        self.receptionFromSensor_thread = None
    
    def receptionFromSensor(self, IP, port, receiveFunc):      
        # Bind the socket to the port
        #os.system('fuser -k '+ str(port)+'/tcp')
        self.server_address = (IP, port)
        print('starting up on {} port {}'.format(*self.server_address))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        # Listen for incoming connections
        self.sock.listen(5)
        # Wait for a connection
        print('waiting for a connection')
        while True:
            #connection, client_address = self.sock.accept()
            receptionFromSensorThread = threading.Thread(target=receiveFunc,args=self.sock.accept())
            receptionFromSensorThread.start()
        
    def receive(self,connection,client_address):
        print('connection from', client_address)
        self.connection_to_server.startTransmissionToServer()
        try:
            #sensor_info_received = False
            while True : #not sensor_info_received
                sensor_info = (connection.recv(4096)).decode("utf-8")
                #print(sensor_info)
                if sensor_info != '': 
                    print(sensor_info) 
                    try:  
                        sensor_info = json.loads(sensor_info)
                    except:
                        print("errrrrrrrrrrrrrrrrrror")
                    #print(type(sensor_info))
                if sensor_info.__class__ == dict:
                    #print(sensor_info)
                    id = sensor_info['id']
                    sensor_info = self.add_new_sensor(sensor_info)
                    self.sensor_data[id] = loadJsonFile('/home/moufdi/GitHubProjects/Projet_interaction_distribuee/' + str(id) + '.json')
                    #print(self.sensor_data)
                    break

            while True:
                data = (connection.recv(4096)).decode("utf-8")  
                #print(data)
                if data != '':  
                    try:  
                        data = json.loads(data)
                        ident, value = data[0], data[1] 

                    except:
                        print("errrrrrrrrrrrrrrrrrreeeuuuur")
                
                try:  
                    value = float(value)
                except:
                    pass

                #print(type(data))
                if(value.__class__ == float or value.__class__ == int):
                    #self.sendRequestToSensor(REQUESTS_TO_SENSOR[0],id)
                    print('\n')
                    print('------------------------Received from Sensor-----------------------')
                    print('received from {} : {}'.format(client_address,data))
                    #response = 'data received'
                    #print('sending {!r}'.format(response))
                    #connection.sendall(response.encode())
                    receive_date = datetime.now().strftime("%d/%m/%Y")
                    receive_time = datetime.now().strftime("%H:%M:%S")
                    data_info = {"date":receive_date,"time":receive_time,"value":value,"unit":sensor_info["unit"]}
                    self.sensor_data[ident].append(data_info)
                    #print('sensor id {}'.format(sensor_info))
                    #print(self.sensor_data)
                    #saveData(sensor_info['/home/moufdi/GitHubProjects/Projet_interaction_distribuee/' + str(ident) + '.json'],self.sensor_data)
                    saveData('/home/moufdi/GitHubProjects/Projet_interaction_distribuee/' + str(ident) + '.json', self.sensor_data[ident])    
                        #print(self.sensor_data) 
                    print('----------------------------------------------------------------------')
                    print('\n')     
        except:
            pass

    def add_new_sensor(self,sensor_info):
        print('\n')
        print('------------------------ Sensor info-----------------------')
        print('Sensor info {}'.format(sensor_info))
        sensor_info['json_file_path'] = '/home/moufdi/GitHubProjects/Projet_interaction_distribuee/' + str(sensor_info['id'])  +'.json'
        id = sensor_info.pop('id') 
        #print(id)
        self.sensors_list[id] = sensor_info
        
        #print(self.path_sensor_metaData)
        saveData(self.path_sensor_metaData,self.sensors_list)
        return sensor_info
        #self.sonsor_threads[id] = threading.Thread(target=self.sendRequestToSensor)


    #def sendRequestToSensor(self, request, sensor_id,*args):
    #    if request in REQUESTS_TO_SENSOR:
    #        if request == REQUESTS_TO_SENSOR[0]:
    #            print('Sending turn off request to {}'.format(sensor_id))
    #            print('Turnning off {}'.format(sensor_id))
    #            self.sock.sendall(request.encode())
    #        elif request == REQUESTS_TO_SENSOR[1]:
    #            print('Sending turn on request to {}'.format(sensor_id))
    #            print('Turnning on {}'.format(sensor_id))
    #            #TODO
    #        elif request == REQUESTS_TO_SENSOR[2]:
    #            print('Sending rate setting request to {}'.format(sensor_id))
    #            print('Resetting {} rate'.format(sensor_id))
    #            #TODO
    
    #def sendDataToServer(self):
    #    while(True):
    #        last_received_data = [self.aggregator_id,self.get_last_received_data()]
    #        self.connection_to_server.send(last_received_data)
    #        self.start_timer(5) # send last received data to the server each minute
    
    #def startTransmissionToServer(self):
    #    self.connection_to_server.thread_client.start()
    #    self.sendToServer_thread = threading.Thread(target=self.sendDataToServer)
    #    self.receptionFromServer_thread = threading.Thread(target=self.connection_to_server.receive) 
    #    self.sendToServer_thread.start()
    #    self.receptionFromServer_thread.start()
    
    def respondToServerRequest(self):
        pass

    class ConnectionToServer(TCPClient):
        SERVER_REQUESTS = ['TURN_OFF','TURN_ON','SET_RATE']
        def __init__(self,agregator_id,agreg_sensor_list,sensor_data):
            TCPClient.__init__(self)
            self.agregator_id = agregator_id
            self.agreg_sensor_list = agreg_sensor_list
            self.sensor_data = sensor_data
            self.thread_client = threading.Thread(target=self.connectToServer,args=['localhost',2500])
            self.sendToServer_thread = threading.Thread(target=self.send,args=self.sensor_data)
            self.receptionFromServer_thread = threading.Thread(target=self.receive) 

        def send(self,data):
            if self.isConnected() == 0 and self.isDisconnected() == False:
                while(True):
                    print(data)
                    last_received_data = [self.agregator_id,self.get_last_received_data()]
                    try:
                        last_received_data = json.dumps(last_received_data)
                        #print('len {}'.format(len(data)))
                        print('sending {!r} to {}'.format(last_received_data,self.port))
                        self.sock.sendall(last_received_data.encode())
                        self.start_timer(5) # send last received data to the server each minute
                    except:
                        pass

        def get_last_received_data(self):
            last_received_data = {}
            sensors = list(self.sensor_data.keys())
            for s in sensors:
                last_received_data[s] = self.sensor_data[s][-1]
            return last_received_data

        def startTransmissionToServer(self):
            self.thread_client.start()
            self.sendToServer_thread.start()
            self.receptionFromServer_thread.start()
        
        def start_timer(self,t):
            time.sleep(t)
        #def receive(self):
        #    while True:
        #        if self.isConnected() == 0 and self.isDisconnected() == False:
        #            receivedFromServer = self.sock.recv(4096).decode("utf-8")
        #            if(receivedFromServer != ''):
        #                try:
        #                    receivedFromServer = json.loads(receivedFromServer)
        #                    if (receivedFromServer.__class__ == list):
        #                        agreg_id, request = receivedFromServer[0], receivedFromServer[1]
        #                        if agreg_id == self.agregator_id:
        #                            self.send(request)
        #                except:
        #                    pass
        #                print('received {!r} from {}'.format(self.data,self.port))
        
    #def start_timer(self,t):
    #    time.sleep(t)

    #def get_last_received_data(self):
    #    last_received_data = {}
    #    sensors = list(self.sensor_data.keys())
    #    for s in sensors:
    #        last_received_data[s] = self.sensor_data[s][-1]
    #    return last_received_data
    
    def startAgregatorReception(self, IP, port, receiveFunc):
        self.receptionFromSensor_thread = threading.Thread(target=self.receptionFromSensor,args=[IP, port, receiveFunc])
        self.receptionFromSensor_thread.start()

#agg = AggregatorAgent('agg1')
#agg.startAgregatorReception('localhost',3100,agg.receive)
#
#agg2 = AggregatorAgent('agg2')
#agg2.startAgregatorReception('localhost',3200,agg2.receive)
#
#agg.startTransmissionToServer()
#agg2.startTransmissionToServer()

