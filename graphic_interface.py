from tkinter import *
import threading
from serverMachine import ServerMachine
import json 

global agreg_list_length, frames, checked
frames = []

agreg_list_length = 0

class GUI:
    def __init__(self):
        global checked
        self.root =Tk()
        #self.agreg_frame = None
        checked = StringVar()
        self.serverMachine = ServerMachine()
        #self.serverMachine.startServer('localhost',2500,self.serverMachine.receiveData)
        threading.Thread(target=self.serverMachine.startServer,args=['localhost',2500,self.serverMachine.receiveData]).start()
        #self.agregator_list = agregator_list
        self.init_root_widgets()
        self.root.mainloop()
    
    def update_agregator_list(self, agregator_list):
        self.agregator_list = agregator_list


    def init_root_widgets(self):
        global checked
        self.root.geometry('820x520')
        self.root.title('SensorsEveryWhere Interface')
        self.root_frame = LabelFrame(self.root)
        self.root_frame.pack(fill='both', expand='yes')
        welcome_label = Label(self.root_frame,text='Welcome to SensorEveryWhere\n please choose an agregator')
        welcome_label.pack()
        self.agreg_frame = LabelFrame(self.root_frame,text='Waiting agregators to connect .....',padx=5,pady=5,borderwidth=5) 
        self.agreg_frame.place(in_=self.root_frame, rely=0.0, y=50,relwidth=1,height=70)
        scrolaball_frame = Scrollbar(self.agreg_frame,orient='horizontal')
        scrolaball_frame.pack(side = BOTTOM, fill = X)
        self.sensors_frame = LabelFrame(self.root_frame,padx=5,pady=5,borderwidth=5)
        self.sensors_frame.place(in_=self.agreg_frame, rely=1.0, y=50, relwidth=1, height=300)
        self.request_frame = LabelFrame(self.sensors_frame,text='Send request to agregator',padx=5,pady=5,borderwidth=5)
        get_instant_data = Button(self.request_frame,text='GetInstantData',padx=5,command=lambda: self.resquest_callback(ServerMachine.REQUESTS_TO_AGREGATOR[1]))
        get_instant_data.place(in_=self.request_frame, relx=0.0, x=30, width=100)
        get_agreg_config = Button(self.request_frame,text='Configuration',padx=5)
        get_agreg_config.place(in_=get_instant_data, relx=1.0, x=30, relwidth=1, relheight=1)
    
        threading.Thread(target=self.create_radio_buttons).start()
        #self.create_radio_buttons()
    
    def create_radio_buttons(self):
        global agreg_list_length
        global checked
        self.agreg_frame['text'] = 'Connected Agregators'
        while True:
            if agreg_list_length == len(self.serverMachine.agregator_list) - 1:   
                #checked.set(str(self.agregator[0]))
                #for agreg in self.agregator:
                if agreg_list_length == 0:
                    radioButton = Radiobutton(self.agreg_frame,text=str(self.serverMachine.agregator_list[-1]),variable=checked,value=str(self.serverMachine.agregator_list[-1]),command=self.radioBtnCallback)
                    temp = radioButton
                    radioButton.pack()
                elif agreg_list_length > 0: 
                    radioButton = Radiobutton(self.agreg_frame,text=str(self.serverMachine.agregator_list[-1]),variable=checked,value=str(self.serverMachine.agregator_list[-1]),command=self.radioBtnCallback)
                    radioButton.place(in_=temp, relx=1.0, x=5, rely=0)
                    temp = radioButton
        
                agreg_list_length += 1 
    
    def radioBtnCallback(self):
        global frames
        global checked
        sensor_data = {}
        self.labels = {}  
        update_thread = threading.Thread() 
        checked_local = StringVar()
        checked_local.set(checked.get())
        self.sensors_frame['text'] = checked_local.get()  
        sensor_data = self.serverMachine.get_last_data(checked.get())
        self.request_frame.place(in_=self.sensors_frame, rely=0.0, y=10,relwidth=1,height=70)
        if len(frames) != 0:    
            for f in frames:
                f.destroy() 
        frames.clear()
        print('-----------------------------')
        temp = self.request_frame
        y = 10
        rely = 1.0
        for sensor in sensor_data.keys():
            print(sensor)
            frames.append(LabelFrame(self.sensors_frame,text=str(sensor),padx=5,pady=5,borderwidth=3))
            frames[-1].place(in_=temp, rely=rely, y=y, relwidth=1, height=80)
            y = 20
            rely = 1.0
            temp = frames[-1]
        i = 0
        for sensor, data in list(sensor_data.items()):    
            sensor_name = Label(frames[i],text=str(sensor))
            sensor_value = Label(frames[i],text=str(data['value']))
            unit = Label(frames[i],text=str(data['unit']))
            date = Label(frames[i],text=str(data['date']))
            time = Label(frames[i],text=str(data['time']))
            
            sensor_name.place(in_=frames[i], relx=0.0, x=30, width=80, relheight=1)
            sensor_value.place(in_=sensor_name, relx=1.0, x=40, width=80, relheight=1)
            unit.place(in_=sensor_value, relx=1.0, x=40, width=80, relheight=1)
            time.place(in_=date, relx=1.0, x=40, width=80, relheight=1)
            date.place(in_=unit, relx=1.0, x=40, width=80, relheight=1)
            i += 1
            self.labels[sensor]={'unit':unit, 'sensor_value':sensor_value, 'date':date, 'time':time}

        def update_data():    
            while(True):
                if checked_local.get() != checked.get():
                    break
                sensor_data = self.serverMachine.get_last_data(checked.get())
                for sensor, data in list(sensor_data.items()):
                    self.labels[sensor]['sensor_value']['text'] = data['value']
                    self.labels[sensor]['unit']['text'] = data['unit']
                    self.labels[sensor]['time']['text'] = data['time']
                    self.labels[sensor]['date']['text'] = data['date'] 

        update_thread = threading.Thread(target=update_data)
        update_thread.start()
    
    def resquest_callback(self,request):
        global checked
        #if self.serverMachine.request_result['agregator_id'] == :
        self.serverMachine.sendRequestToAgregator(request,checked.get())
        while True:
            if len(self.serverMachine.request_result.keys()) != 0:
                print(self.serverMachine.request_result.keys())
                if self.serverMachine.request_result['request_index'] == 0:
                    pass
                elif self.serverMachine.request_result['request_index'] == 1:
                    last_received_data = self.serverMachine.request_result['request_result']
                    for sensor, data in list(last_received_data.items()):
                        self.labels[sensor]['sensor_value']['text'] = data['value']
                        self.labels[sensor]['unit']['text'] = data['unit']
                        self.labels[sensor]['time']['text'] = data['time']
                        self.labels[sensor]['date']['text'] = data['date'] 
                self.serverMachine.request_result = {}
                break 

g = GUI()