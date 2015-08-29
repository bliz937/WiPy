#!/usr/bin/python

"""
The client gets the WiFi signal strength and sends that over the network to the server part.
"""

import subprocess
import socket
import json
import argparse
from Signal import *

"""
Using the wavemon package, we get the signal strength - mW and dBm.
Return type is of type Signal.
"""
def getSignalWaveMon():
	query = "wavemon -d | grep signal"
	output = subprocess.check_output(query.split())
	output = output[output.index("signal")+14:]
	output = output[:output.index("mW)")+3]
	dBm = int(output[:output.index("dBm")])
	mW = float(output[output.index("(")+1:output.index(")")-3])
	return Signal(dBm,mW)

def createSocket(server,port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server[0],port))
	return sock
	

def send(sock):
	hostname = socket.gethostname()

	try:
		print("Sending hostname size")
		sock.send(str(hostname.__sizeof__()))
		print("Sending hostname")
		sock.send(hostname)
		print("Deleting hostname variable")
		del hostname
		print("Awaiting time")
		time = sock.recv(24)
		print("Received time of %s"%time)
		while(True):
			break
	finally:
		sock.shutdown(socket.SHUT_RDWR)
		sock.close()

if(__name__ == "__main__"):
	#print(fromJSON(getSignalWaveMon().toJSON()))
	parser = argparse.ArgumentParser(description="Sends WiFi signal strength, mW and dBm, to a given server.")
	parser.add_argument("-s", help="Server to use.", dest="server", nargs=1, required=True, type=str)
	parser.add_argument("-p", help="Port number to send to. Default is 12000 server side.", dest="port", type=int, nargs=1, default=12000)

	args = parser.parse_args()
	sock = createSocket(args.server,args.port)
	send(sock)
