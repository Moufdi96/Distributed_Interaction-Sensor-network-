import threading
import socket
import sys
import time
import os
from random import uniform
from clientTCP import TCPClient
import json

REQUESTS_FROM_AGGREGATOR = ['TURN_OFF','TURN_ON','SET_RATE']

class VirtualSensor(TCPClient) : 
    def __init__(self,sensor_id,data_type,sensor_rate,measurement_unit,geolocalisation,serverIP,serverPort):
        TCPClient.__init__(self)
        self.sensor_id = sensor_id
        self.data_type =data_type
        self.sensor_rate = sensor_rate # rate (Hz)
        self.measurement_unit = measurement_unit
        self.transmission_state = False
        self.geolocalisation = geolocalisation
        self.thread_client1 = threading.Thread(target=self.connectToServer,args=[serverIP,serverPort])
        self.thread_send1 = threading.Thread(target=self.send)
        self.thread_receive1 = threading.Thread(target=self.receive)
        
    def send(self):
        sensor_info = json.dumps({'id':self.sensor_id,'type':self.data_type,'rate':self.sensor_rate,'unit':self.measurement_unit,'geolocalisation':self.geolocalisation})
        while True:
            if self.isConnected() == 0 and self.isDisconnected() == False:
                
                try:
                    self.sock.sendall(sensor_info.encode())
                    time.sleep(1)
                    break
                except:
                    pass
            else:
                continue

        while True :
            self.data = ''
            if self.isConnected() == 0 and self.isDisconnected() == False:
                try:
                # Send data
                    value = str(self.dataAcquisition())
                    data = [self.sensor_id,value]
                    data = json.dumps(data)
                    print('sending {!r} to {}'.format(data,self.port))
                    self.sock.sendall(data.encode())
                    
                except Exception as e:
                    print(e)
            self.start_timer()

    def receive(self):
        while True:
            if self.isConnected() == 0 and self.isDisconnected() == False:
                self.data = self.sock.recv(4096).decode("utf-8")
                print(self.data)
                if(self.data != '' and self.data in REQUESTS_FROM_AGGREGATOR):
                    if self.data == REQUESTS_FROM_AGGREGATOR[0]:
                        print('received turn off request from aggreagator {}'.format(self.port))
                        print('Turnning off sensor')
                        self.turn_off_sensor()
                    elif self.data == REQUESTS_FROM_AGGREGATOR[1]:
                        print('received turn on request from aggreagator {}'.format(self.port))
                        print('Turnning on sensor')
                        self.turn_on_sensor()
                    elif self.data[0:len(REQUESTS_FROM_AGGREGATOR)] == REQUESTS_FROM_AGGREGATOR[2]:
                        print('received rate setting request from aggreagator {}'.format(self.port))
                        print('Turnning off sensor')
                        rate = float(self.data[len(REQUESTS_FROM_AGGREGATOR):])
                        self.setRate(rate)    

    def start_timer(self):
        time.sleep(1/self.sensor_rate)

    def setRate(self,rate):
        self.sensor_rate = rate
    
    def getRate(self):
        return self.sensor_rate

    def turn_off_sensor(self): # turn off data transmission 
        self.transmission_state = False 
    
    def turn_on_sensor(self): # turn on data transmission
        self.transmission_state = True

    def setGeolocalisation(self, geolocalisation):
        self.geolocalisation = geolocalisation
    
    def getGeolocalisation(self):
        return self.geolocalisation 
    
    def start_threads(self):
        self.thread_client1.start()
        #self.thread_receive1.start()
        self.thread_send1.start()
        #self.thread_receive1.start()

    def dataAcquisition(self):
        print(self.data_type)
        if self.data_type == 'Humidity':
            data = round(uniform(80,86),2) 
        elif self.data_type == 'Heat':
            data = round(uniform(10,13),2)
        elif self.data_type == 'Air pressure':
            data = round(uniform(1015,1020),2)
        return data
