from serverTCP import ServerTCP
import threading
from clientTCP import TCPClient 
import numpy as np
from stableMemory import loadJsonFile, saveData

PATH_STABLE_MEMORY = "/home/moufdi/GitHubProjects/Projet_mutlithreading/stableMemory.json"

class ServerMachine(ServerTCP):
    def __init__(self, serverID):
        ServerTCP.__init__(self)
        self.server1ID = serverID
        self.priority = ''  #primary or backup 
        self.recover_data()
        #self.thread_process_data = threading.Thread(target=self.process_data)
        #self.thread_process_data.start()

    def process_data(self):
        #while True:
        if len(self.data) == ServerTCP.SLIDING_WINDOW_LENGHT:
            # ensuring Temporal redundancy
            print('\n')
            print('-----------------------first run of the service------------------------')
            res_1 = self.computeMean(self.data)
            print('-----------------------------------------------------------------------')
            print('\n')
            print('-----------------------second run of the service------------------------')
            res_2 = self.computeMean(self.data)
            print('-----------------------------------------------------------------------')
            print('\n')
            if res_1 == res_2:
                print('mean value of the last {} acquired data is {} :'.format(ServerTCP.SLIDING_WINDOW_LENGHT,res_1))
                self.store_acquired_data(PATH_STABLE_MEMORY, self.data, res_1)
            else: 
                print('\n')
                print('-----------------------third run of the service------------------------')
                res_3 = self.computeMean(self.data)
                print('-----------------------------------------------------------------------')

                # majority voting
                print('\n')
                print('-----------------------------Majority voting----------------------------')
                if res_3 == res_1:
                    print('mean value of the last {} acquired data is {} :'.format(ServerTCP.SLIDING_WINDOW_LENGHT,res_1))
                    self.store_acquired_data(PATH_STABLE_MEMORY, self.data, res_1)
                elif res_3 == res_2:
                    print('mean value of the last {} acquired data is {} :'.format(ServerTCP.SLIDING_WINDOW_LENGHT,res_2))
                    self.store_acquired_data(PATH_STABLE_MEMORY, self.data, res_2)
                else: # server failed to obtain the correct value
                    print('Cannot judge which value is correct since all outputs of the three diffrent execution have same votes number')
                    print("Service failed to produce the correct values..... " + self.server1ID + " needs to be repaired !!!")
                    print("shutting down " + self.server1ID + ".....")
                    self.sock.close()
                    TCPClient.freeServerAddress(self.server_address[1])
                print('-----------------------------------------------------------------------')
                    

            #print(self.data)
            
    
    def store_acquired_data(self, path, newDataVector, mean):
        saveData(path, newDataVector, mean)
        
    def set_priority(self, priority):
        self.priority = priority

    def recover_data(self):
        dataBase = loadJsonFile(PATH_STABLE_MEMORY)
        if len(dataBase) > 0: 
            self.data = dataBase[len(dataBase)-1][0]
            self.data.pop(0)

    def receiveData(self,connection,client_address):
        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            while True:  
                temp = (connection.recv(32)).decode("utf-8")  
                #print(temp)
                
                try:  
                    data = float(temp)
                except:
                    data = temp

                #print(type(data))
                if(data!= None):
                    if data.__class__ == str:
                        #data = data.lower()
                        print('\n')
                        print('------------------------Received from Watchdog-----------------------')
                        print('received from {} : {}'.format(client_address,data))
                        print('\n')
                        if data == 'Are you still alive ?':
                            response = 'i am alive'
                            print('sending {!r}'.format(response))
                            connection.sendall(response.encode())
                        print('----------------------------------------------------------------------')
                        print('\n')
                    else:
                        print('\n')
                        print('------------------------Received from Sensor-----------------------')
                        print('received from {} : {}'.format(client_address,data))
                        response = 'data received'
                        print('sending {!r}'.format(response))
                        connection.sendall(response.encode())
                        self.data.append(data)
                        print(self.data)
                        print('----------------------------------------------------------------------')
                        print('\n')
                        if len(self.data) >= ServerTCP.SLIDING_WINDOW_LENGHT: 
                            self.process_data()
                            self.data.pop(0)      
        except:
            pass
    
    ''' 
    This the function represents the service provided by the server. 
    It calculates the mean value of the n last received values, n can be set using 'ServerTCP.SLIDING_WINDOW_LENGHT'  
    We can choose or not to include fault injection (in case we want to test the TR module)    
    '''
    def computeMean(self,data,faulInjection=False):
        if faulInjection == True:
            alteredData = self.faulInjector(data)
           
            print('values to be processed {}'.format(alteredData))
            mean = np.mean(alteredData)
            print('mean {}'.format(mean))
            return mean
        print('values to be processed {}'.format(data))
        mean = np.mean(data)
        print('mean {}'.format(mean))
        return mean

    '''
    this function can be used to test the TR mudule (temporal redundancy) 
    it generates a random fault value to alterate the received data (to simulate for example the effects of bit-flips)
    '''
    def faulInjector(self, receivedData):     
        from random import randint
        d = self.data.copy()
        print('list {}'.format(d))
        d[2] += randint(0,2)
        #print('rand {}'.format(rand))
        return d 

    
     
