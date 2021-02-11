from sensor import VirtualSensor


sensor1 = VirtualSensor('Hygrometer','Humidity',3,'%','Rangueil','localhost',3100)
sensor2 = VirtualSensor('Thermometer1','Heat',2.6,'C°','Rangueil','localhost',3100)
sensor3 = VirtualSensor('Thermometer2','Heat',1.9,'C°','Rangueil','localhost',3100)
sensor4 = VirtualSensor('Barometer','Air pressure',0.4,'mbar','Rangueil','localhost',3100)
sensor5 = VirtualSensor('Thermometer','Heat',0.35,'C°','Ramonville','localhost',3200)
sensor6 = VirtualSensor('Barometer','Air pressure',0.35,'mbar','Ramonville','localhost',3200)
sensor7 = VirtualSensor('Hygrometer','Humidity',0.2,'%','Ramonville','localhost',3200)
sensor8 = VirtualSensor('Thermometer','Heat',3.8,'C°','Capitole','localhost',3300)
sensor9 = VirtualSensor('Barometer1','Air pressure',2.35,'mbar','Capitole','localhost',3300)
sensor10 = VirtualSensor('Barometer2','Air pressure',4,'mbar','Capitole','localhost',3300)

sensor1.start_threads()
sensor2.start_threads()
sensor3.start_threads()
sensor4.start_threads()
sensor5.start_threads()
sensor6.start_threads()
sensor7.start_threads()
sensor8.start_threads()
sensor9.start_threads()
sensor10.start_threads()

