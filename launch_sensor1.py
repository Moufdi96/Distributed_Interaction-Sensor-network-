from sensor import VirtualSensor

sensor1 = VirtualSensor('sensor1','Humidity',0.25,'lux','localisation','localhost',3100)
sensor2 = VirtualSensor('sensor2','Thermometer',0.3,'C°','localisation','localhost',3100)
sensor3 = VirtualSensor('sensor3','Barometer',0.4,'bar','localisation','localhost',3200)

sensor1.start_threads()
sensor2.start_threads()
sensor3.start_threads()