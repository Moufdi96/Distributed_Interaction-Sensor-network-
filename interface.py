import tkinter as tk
from tkinter import *
from aggregatorAgent import AggregatorAgent
from sensor import VirtualSensor

win=Tk()
win.title("Sensors EveryWhere")
win.configure(background="light blue")

#agrégateur 1 :
agg1 = AggregatorAgent('agg1')
agg1.startServer('localhost',3100,agg1.receive)
#sensor1 = VirtualSensor('sensor1','Photometer',0.25,'lux','localisation','localhost',3100)
#sensor2 = VirtualSensor('sensor2','Thermometer',3,'C°','localisation')
#sensor3 = VirtualSensor('sensor3','Baromètre',0.4,'bar','localisation')
#sensor1.start_threads()
#sensor2.start_threads()
#sensor3.start_threads()

#agrégateur 2 :
agg2 = AggregatorAgent('agg2')
agg1.startServer('localhost',3200,agg2.receive)  # à voir le port du serveur
#sensor3 = VirtualSensor('sensor3','Photometer',0.4,'lux','localisation','localhost',3200)
#sensor2 = VirtualSensor('sensor2','Thermometer',20,'C°','localisation')
##sensor3 = VirtualSensor('sensor3','Baromètre',0.4,'bar','localisation')
#sensor3.start_threads()
#sensor2.start_threads()
##sensor3.start_threads()


List_agregator= [agg1,agg2]

#try:
#    mode=int(raw_input('agrégateur N°:'))
#except ValueError:
#    print ("Not a number")

#print("Vous avez choisi l'agrégateur N° ",mode)



frame1=LabelFrame(win,width=5000,height=5000,bg="light blue")
frame1.grid(row=0,column=0)


l1=Label(frame1,text="TEMPERATURE",fg="black",font=25,bg="light blue")
l1.grid(row=1,column=0,padx=20,pady=20)
l11=Label(frame1,text="TEMPERATURE",fg="black",font=25,bg="light blue")
l11.grid(row=1,column=1,padx=20,pady=20)
#temperature()


l2=Label(frame1,text="Pression",fg="black",font=12,bg="light blue")
l2.grid(row=2,column=0,padx=10,pady=10)
l22=Label(frame1,text="Pression",fg="black",font=12,bg="light blue")
l22.grid(row=2,column=1,padx=10,pady=10)
#pression()



l3=Label(frame1,text="Volume",fg="Black",font=12,bg="light blue")
l3.grid(row=3,column=0,padx=10,pady=10)
l33=Label(frame1,text="Volume",fg="Black",font=12,bg="light blue")
l33.grid(row=3,column=1,padx=10,pady=10)
#volume()

# main loop #
win.mainloop()
