from serverTCP import ServerTCP
from clientTCP import TCPClient
from clientTCP import TCPClient
from datetime import datetime
import socket
import threading
import json
from stableMemory import loadJsonFile, saveData
class AggregatorAgent(ServerTCP):
    def __init__(self,id):
        ServerTCP.__init__(self)
        self.aggregator_id = id
        self.path_sensor_metaData = '/home/moufdi/GitHubProjects/Projet_interaction_distribuee/' + str(id) + '.json'
        self.sensors_list = loadJsonFile(self.path_sensor_metaData)
        self.client = TCPClient() # to communicate with the server
        self.sensor_data = {}
        #self.sonsor_threads = {}

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
        
    def receive(self,connection,client_address):
        try:
            print('connection from', client_address)
            #sensor_info_received = False
            while True : #not sensor_info_received
                sensor_info = (connection.recv(128)).decode("utf-8")
                #print(sensor_info)
                if sensor_info != '':  
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
                    break

            while True:
                print("carrr")  
                data = (connection.recv(128)).decode("utf-8")  
                #print(data)
                if data != '':  
                    try:  
                        data = json.loads(data)
                        ident, value = data[0], data[1] 

                    except:
                        print("errrrrrrrrrrrrrrrrrreeeuuuur")
                
                try:  
                    value = float(value)
                    #print('value {}'.format(value))
                except:
                    pass

                #print(type(data))
                if(value.__class__ == float or value.__class__ == int):
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
                    print(self.sensor_data)
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

    def sendRequestToSensor(self):
        pass
    class ConnectionToServer(TCPClient):
        SERVER_REQUESTS = ['TURN_OFF','TURN_ON','SET_RATE']
        def __init__(self):
            pass

        def receive(self):
            pass

        def send(self):
            pass

#from sensor import VirtualSensor
agg = AggregatorAgent('agg1')
agg.startServer('localhost',3100,agg.receive)
#sensor1 = VirtualSensor('sensor1','Photometer',0.25,'lux','localisation')
#sensor2 = VirtualSensor('sensor2','Thermommter',0.3,'C°','localisation')
##sensor3 = VirtualSensor('sensor3','Baromètre',0.4,'bar','localisation')
#sensor1.start_threads()
#sensor2.start_threads()
#sensor3.start_threads()