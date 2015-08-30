# WiPy

WiPy is a simple project written in Python that sends the WiFi signal strength, currently obtained using the ```wavemon``` package client side, to a central server. This was build for Arch Linux ARM running on the Raspberry Pi 2.

# Requirements

* Python 2.7+
* wavemon - ```pacman -S wavemon```

# Usage

### Server
On the server side, simply run ```server.py``` by either
```bash
chmod +x server.py
./server.py
```
or
```bash
python server.py
```

### Client
On the client side, as the server, either run

```bash
chmod +x client.py
./client.py -s server
```
or
```bash
python client.py -s server
```

where ```server``` is the server's hostname or IP address.


To manipulate the data, simply edit the ```processData(host,data)``` method.
The host parameter is a string containing the hostanme of the associated data.
The data parameter is of type ```Signal``` from ```Signal.py```.
