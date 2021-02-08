from sensor import VirtualSensor

sensor1 = VirtualSensor('Hygrometer','Humidity',0.25,'lux','localisation','localhost',3100)
sensor2 = VirtualSensor('Thermometer','Heat',0.3,'C°','localisation','localhost',3100)
sensor3 = VirtualSensor('Barometer','Air pressure',0.4,'bar','localisation','localhost',3200)

sensor1.start_threads()
sensor2.start_threads()
sensor3.start_threads()