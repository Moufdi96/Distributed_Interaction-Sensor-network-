from tkinter import *
from tkinter import ttk
from tkinter import font
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
        self.title_font = font.Font(size=13,weight='bold')
        self.welcome_font = font.Font(size=13,weight='bold')
        self.normal_font = font.Font(size=10,weight='bold')
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
        self.root_frame = LabelFrame(self.root,bg='black',fg='white',padx=7,pady=7)
        self.root_frame.pack(fill='both', expand='yes')
        welcome_label = Label(self.root_frame,text='Welcome to SensorsEveryWhere\n Please select an agregator',bg='black',fg='white',font=self.welcome_font)
        welcome_label.pack()
        self.agreg_frame = LabelFrame(self.root_frame,text='Loading agregators .....',padx=10,pady=10,borderwidth=5,bg='black',fg='white',font=self.title_font) 
        self.agreg_frame.place(in_=self.root_frame, rely=0.0, y=50,relwidth=1,height=100)
        scrolaball_frame = Scrollbar(self.agreg_frame,orient='horizontal',bg='black')
        scrolaball_frame.pack(side = BOTTOM, fill = X)
        self.sensors_frame = LabelFrame(self.root_frame,padx=15,pady=15,borderwidth=2,bg='black',fg='white',font=self.title_font)
        self.sensors_frame.place(in_=self.agreg_frame, rely=1.0, y=50, relwidth=1, height=300)


        myCanvas = Canvas(self.sensors_frame,bg='black')
        myCanvas.pack(side=LEFT, fill="both",expand=1)
        scrollbar = ttk.Scrollbar(self.sensors_frame,orient='vertical',command=myCanvas.yview)
        scrollbar.pack(side = RIGHT, fill = "y")
        myCanvas.configure(yscrollcommand=scrollbar.set)
        myCanvas.bind('<Configure>',lambda e: myCanvas.configure(scrollregion=myCanvas.bbox('all')))
        self.second_frame = Frame(myCanvas,padx=5,pady=5,bg='black')
        myCanvas.create_window((0,0),window=self.second_frame, anchor='nw')


        self.request_frame = LabelFrame(self.second_frame,text='Send request to agregator',font=self.title_font,height=80,width=800,padx=10,pady=10,borderwidth=2,bg='black',fg='white')
        
        get_instant_data = Button(self.request_frame,text='Get instant data',font=self.normal_font,padx=5,bg='black',fg='white',command=lambda: self.resquest_callback(ServerMachine.REQUESTS_TO_AGREGATOR[1]))
        get_instant_data.place(in_=self.request_frame, relx=0.0, x=100)
        get_agreg_config = Button(self.request_frame,text='Get Agregator configuration',font=self.normal_font,padx=5,bg='black',fg='white',command=lambda: self.resquest_callback(ServerMachine.REQUESTS_TO_AGREGATOR[0]))
        get_agreg_config.place(in_=get_instant_data, relx=1.0, x=50, relheight=1)
    
        threading.Thread(target=self.create_radio_buttons).start()
        #self.create_radio_buttons()
    
    def create_radio_buttons(self):
        global agreg_list_length
        global checked
        
        while True:
            if agreg_list_length == len(self.serverMachine.agregator_list) - 1:   
                #checked.set(str(self.agregator[0]))
                #for agreg in self.agregator:
                if agreg_list_length == 0:
                    radioButton = Radiobutton(self.agreg_frame,text=str(self.serverMachine.agregator_list[-1]),variable=checked,bg='black',fg='white',value=str(self.serverMachine.agregator_list[-1]),command=self.radioBtnCallback,font=self.normal_font)
                    temp = radioButton
                    radioButton.place(in_=self.agreg_frame)
                    self.agreg_frame['text'] = 'Connected Agregators'
                elif agreg_list_length > 0: 
                    radioButton = Radiobutton(self.agreg_frame,text=str(self.serverMachine.agregator_list[-1]),variable=checked,bg='black',fg='white',value=str(self.serverMachine.agregator_list[-1]),command=self.radioBtnCallback,font=self.normal_font)
                    radioButton.place(in_=temp, relx=1.0, x=15)
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
        self.request_frame.pack() #place(in_=self.second_frame, rely=0.0, y=10,relwidth=1,height=80)
        if len(frames) != 0:    
            for f in frames:
                f.destroy() 
        frames.clear()
        print('-----------------------------')
        temp = self.request_frame
        y = 20
        rely = 1.0
        for sensor in sensor_data.keys():
            print(sensor)
            frames.append(LabelFrame(self.second_frame,text=str(sensor),font=self.normal_font,padx=5,height=80,width=800,pady=5,borderwidth=1,bg='black',fg='white'))
            frames[-1].pack()#place(in_=temp, rely=rely, y=y, relwidth=1, height=80)
            y = 20
            rely = 1.0
            temp = frames[-1]
        i = 0
        for sensor, data in list(sensor_data.items()):  
            sensor_name = Label(frames[i],text=str(sensor),bg='black',fg='white')
            sensor_value = Label(frames[i],text=str(data['value']),bg='black',fg='white')
            unit = Label(frames[i],text=str(data['unit']),bg='black',fg='white')
            date = Label(frames[i],text=str(data['date']),bg='black',fg='white')
            time = Label(frames[i],text=str(data['time']),bg='black',fg='white')
            
            sensor_name.place(in_=frames[i], relx=0.0, x=20, width=100, relheight=1)
            sensor_value.place(in_=sensor_name, relx=1.0, x=20, width=80, relheight=1)
            unit.place(in_=sensor_value, relx=1.0, x=20, width=80, relheight=1)
            time.place(in_=date, relx=1.0, x=20, width=80, relheight=1)
            date.place(in_=unit, relx=1.0, x=20, width=80, relheight=1)
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
        self.serverMachine.sendRequestToAgregator(request,checked.get())
        from tkinter import ttk 
        while True:
            if len(self.serverMachine.request_result.keys()) != 0:
                print(self.serverMachine.request_result.keys())
                if self.serverMachine.request_result['request_index'] == 0:
                    config_window = Toplevel(width=600,height=500,bg='black')
                    config_window.title('Agregator configuration')
                    wrapper = LabelFrame(config_window,bg='black')
                    wrapper.pack(fill="both",expand=1)
                    myCanvas = Canvas(wrapper,bg='black')
                    myCanvas.pack(side=LEFT, fill="both",expand=1)
                    scrollbar = ttk.Scrollbar(wrapper,orient='vertical',command=myCanvas.yview)
                    scrollbar.pack(side = RIGHT, fill = "y")
                    myCanvas.configure(yscrollcommand=scrollbar.set)
                    myCanvas.bind('<Configure>',lambda e: myCanvas.configure(scrollregion=myCanvas.bbox('all')))
                    myFrame = Frame(myCanvas,bg='black')
                    myCanvas.create_window((0,0),window=myFrame, anchor='nw')
                    

                    agreg_configuration = self.serverMachine.request_result['request_result']
                    temp = LabelFrame(myFrame,padx=5,pady=5,height=70,width=500,borderwidth=3,bg='black',fg='white')
                    temp.pack()#place(in_=myFrame, rely=0.0, y=5, relwidth=0.9,height=80)
                    agreg_lable = Label(temp,text='Agregator : ' + str(checked.get()),bg='black',fg='white',font=self.title_font)
                    agreg_lable.place(in_=temp,relx=0.0,x=70,relheight=1)
                    num_sensor = Label(temp,text='Sensor number : ' + str(len(agreg_configuration.keys())),bg='black',fg='white',font=self.title_font)
                    num_sensor.place(in_=agreg_lable,relx=1.0,x=30,relheight=1)
                    y = 10
                    rely = 0.0
                    relwidth = 0.9
                    temp = myFrame
                    for sensor, caracteristics in list(agreg_configuration.items()):
                        
                        temp_frame = LabelFrame(myFrame,padx=5,pady=5,height=150,width=500,font=self.normal_font,borderwidth=3,bg='black',fg='white')
                        temp_frame.pack()#place(in_=temp,rely=rely,y=y,relwidth=relwidth,height=150)
                        y = 20
                        rely = 1.0
                        relwidth = 1
                        temp = temp_frame
                        sensor_label = Label(temp_frame,text='Sensor : ' + str(sensor),bg='black',fg='white')
                        type_label = Label(temp_frame,text='Data type : ' + str(caracteristics['type']),bg='black',fg='white')
                        rate_label = Label(temp_frame,text='Sensor transmission rate : ' + str(caracteristics['rate'])+' hz',bg='black',fg='white')
                        unit_label = Label(temp_frame,text='Measurement unit : ' + str(caracteristics['unit']),bg='black',fg='white')
                        geolocalisation_label = Label(temp_frame,text='Sensor geolocalization : ' + str(caracteristics['geolocalisation']),bg='black',fg='white')

                        sensor_label.place(in_=temp_frame, rely=0.0, y=10)
                        type_label.place(in_=sensor_label, rely=1.0, y=10,relheight=1)
                        rate_label.place(in_=type_label, rely=1.0, y=10, relheight=1)
                        unit_label.place(in_=rate_label, rely=1.0, y=10, relheight=1)
                        geolocalisation_label.place(in_=unit_label, rely=1.0, y=10, relheight=1)
                    break

                elif self.serverMachine.request_result['request_index'] == 1:
                    last_received_data = self.serverMachine.request_result['request_result']
                    for sensor, data in list(last_received_data.items()):
                        self.labels[sensor]['sensor_value']['text'] = data['value']
                        self.labels[sensor]['unit']['text'] = data['unit']
                        self.labels[sensor]['time']['text'] = data['time']
                        self.labels[sensor]['date']['text'] = data['date'] 
                self.serverMachine.request_result = {}
                break 
    

if __name__ == '__main__':
    GUI()