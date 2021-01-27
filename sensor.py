import threading
import socket
import sys
import time
import os
from random import uniform
from clientTCP import TCPClient

AGGREGATOR_REQUESTS = ['TURN_OFF','TURN_ON','SET_RATE']

class Sensor(TCPClient) : 
    def __init__(self,sensor_id,sensor_type,sensor_rate,geolocalisation):
        TCPClient.__init__(self)
        self.sensor_id = sensor_id
        self.sensor_type =sensor_type
        self.sensor_rate = sensor_rate # rate (Hz)
        self.transmission_state = False
        self.geolocalisation = geolocalisation
        self.thread_client1 = threading.Thread(target=self.connectToServer,args=['localhost',2500])
        self.thread_send1 = threading.Thread(target=self.send)
        self.thread_receive1 = threading.Thread(target=self.receive)
        
    def send(self):
        while True :
            self.data =''
            if self.isConnected() == 0 and self.isDisconnected() == False:
                try:
                # Send data
                    data = str(SensorClient.dataAcquisition())
                    print('sending {!r} to {}'.format(data,self.port))
                    self.sock.sendall(data.encode())
                    
                except:
                    pass
            self.start_timer()

    def receive(self):
        while True:
            if self.isConnected() == 0 and self.isDisconnected() == False:
                self.data = self.sock.recv(16).decode("utf-8")
                if(self.data != '' and self.data in AGGREGATOR_REQUESTS):
                    if self.data == AGGREGATOR_REQUESTS[0]:
                        print('received turn off request from aggreagator {}'.format(self.port))
                        print('Turnning off sensor')
                        self.turn_off_sensor()
                    elif self.data == AGGREGATOR_REQUESTS[1]:
                        print('received turn on request from aggreagator {}'.format(self.port))
                        print('Turnning on sensor')
                        self.turn_on_sensor()
                    elif self.data[0:len(AGGREGATOR_REQUESTS)] == AGGREGATOR_REQUESTS[2]:
                        print('received rate setting request from aggreagator {}'.format(self.port))
                        print('Turnning off sensor')
                        rate = float(self.data[len(AGGREGATOR_REQUESTS):])
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


    @staticmethod
    def dataAcquisition():
        data = uniform(-10000,10000)
        return data