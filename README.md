# Distributed interaction system : Sensor network

The aim of this project is to implement and simulate a distributed interaction system. the system is constituted of a sensor network connected to agregators which in turn connect to a final server.   

Each agregator receives data from a set of sensors (software simulated sensors) situated approximately in the same geolocalization.
All data transmisions are done via TCP/IP protocol using client/server architecture, messages are parsed into json strings before they are sent to agregators. 

Agregators send data updates to the server so that they are displayed in the graphic interface.

To create a new sensor go to file "launch_sensors.py", instantiate a new VirtualSensor object with :
- 1st param = sensor name (ex: barometer, thermometer...)
- 2nd param = measured data type (ex: heat, humidity, air pressure ...)
- 3rd param = transmission rate (hz)
- 4th param = measurement unit (ex: mbar, C°...)
- 5th param = geaolocalization
- 6th param = IP adresse of the agregator the sensor will send data to 
- 7th param = port of the agregator the sensor will send data to

then call the 'start_threads' function to launch sensor data acquisition. 

To create a new agregator create a new python file, include this code line "from aggregatorAgent import AgregatorAgent" then instantiate a new AgregatorAgent object with the agregator id as parameter

to start data reception from sensors call startAgregatorReception function with :

- 1st param : IP adresse of the agregator
- 2nd param : Port of the agregator
- 3rd param : AgregatorAgent class function 'receive'

to start data transmission from agregator to server call 'startTransmissionToServer' function.

To change transmission rate from agregator to server go to file "AgregatorAgent.py" line 156 
in "self.start_timer" function change the delay parameter (in seconds) to the suitable one (default rate = 20s).

Please check this Demo video https://drive.google.com/file/d/1I9h3oe62-oM6nfd9Ux5tS1PjYFd35qN-/view?usp=sharing

