Fast setup:
========================

```
$ pip install paho-mqtt
```

```
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto mosquitto-clients
```

```
sudo nano /etc/mosquitto/conf.d/myconfig.conf
```

Paste this:   
   
```
persistence false

# mqtt
listener 420
protocol mqtt

```
   
```     
sudo service mosquitto restart 
```

Now run Ardupilot SITL   

In new console:   

```     
python mqttClient.py
``` 
   
In another console:   

``` 
./mavlink_control
```
