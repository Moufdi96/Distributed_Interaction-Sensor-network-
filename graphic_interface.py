from tkinter import *
import threading
from serverMachine import ServerMachine
import json 

global agreg_list_length, frames
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
        self.agreg_frame = LabelFrame(self.root_frame,text='Loading agregators .....',padx=5,pady=5,borderwidth=5) 
        self.agreg_frame.place(in_=self.root_frame, rely=0.0, y=50,relwidth=1,height=70)
        scrolaball_frame = Scrollbar(self.agreg_frame,orient='horizontal')
        scrolaball_frame.pack(side = BOTTOM, fill = X)
        self.sensors_frame = LabelFrame(self.root_frame,text=checked,padx=5,pady=5,borderwidth=5)
        self.sensors_frame.place(in_=self.agreg_frame, rely=1.0, y=50, relwidth=1, height=300)
        
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
        sensor_data = {}
        #labels = {}   
        global checked
        checked_local = StringVar()
        checked_local.set(checked.get())
        #print('checked {}'.format(checked.get()))
        #print('checked_local {}'.format(checked_local.get())) 
        sensor_data = self.serverMachine.get_last_data(checked.get())

        if len(frames) != 0:
            for f in frames:
                f.destroy() 
        frames.clear()
        print('-----------------------------')
        temp = self.sensors_frame
        y = 10
        rely = 0.0
        for sensor in sensor_data.keys():
            print(sensor)
            frames.append(LabelFrame(self.sensors_frame,text=str(sensor),padx=5,pady=5,borderwidth=3))
            frames[-1].place(in_=temp, rely=rely, y=y, relwidth=1, height=80)
            y = 20
            rely = 1.0
            temp = frames[-1]
        i = 0
        sensor_name = Label(frames[0],text="Moufdi")
        #sensor_name.place(relx=1.0, relwidth=1, relheight=1)
        for sensor, data in list(sensor_data.items()):    
            sensor_value = Label(frames[i],text=str(data['value']))
            unit = Label(frames[i],text=str(data['unit']))
            date = Label(frames[i],text=str(data['date']))
            time = Label(frames[i],text=str(data['time']))
            
            print(data['value'])
            sensor_name = Label(frames[i],text=str(sensor))
            sensor_name.place(in_=frames[i], relx=0.0, x=10, width=70, relheight=1)
            sensor_value.place(in_=sensor_name, relx=1.0, x=10, width=70, relheight=1)
            unit.place(in_=sensor_value, relx=1.0, x=10, width=70, relheight=1)
            date.place(in_=unit, relx=1.0, x=10, width=70, relheight=1)
            time.place(in_=date, relx=1.0, x=10, width=70, relheight=1)
            i += 1

        #def update_thread():    
        #    while(True):
        #        if checked.get() != checked_local.get():
        #            print('checked_local {}'.format(checked_local.get()))
        #            
        #            for s in list(labels.keys()):
        #                labels[s][0].destroy()
        #                labels[s][1].destroy()
        #                labels.clear() 
        #            break
#
        #        sensor_data = self.serverMachine.get_last_data(checked.get())
        #        print(sensor_data)
        #        print(labels.keys())
        #        for s in list(labels.keys()) :
        #            labels[s][1]['text'] = str(sensor_data[s])
#
        #threading.Thread(target=update_thread).start()

g = GUI()