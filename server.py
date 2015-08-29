#!/usr/bin/python

import argparse
import socket
import atexit
import threading
from Signal import *
from time import sleep
import sys
import json

"""
Creates the socket.
"""

def createSocket(interface,port):
#	print("Interface: %s\nPort: %d"%(interface,port))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((interface,port))
	return sock

"""
Listens for incoming connections.
"""
def listen(sock,time):
	sockets = []
	atexit.register(closeSocket,sock,sockets)
	bufsize = sock.getsockopt( socket.SOL_SOCKET, socket.SO_SNDBUF )
	print("Bufsize: " + str(bufsize) )
	sock.listen(5)
	
	try:	
		while(True):
			client,address = sock.accept()
			sockets.append(client)
			client.settimeout(60)
			threading.Thread(target=clientListen,args=(client,address,sockets,time)).start()
	except KeyboardInterrupt:
		sys.exit(0)

def clientListen(client,address,sockets,time):
#	atexit.register(closeClient,sock)
	print("Opening connection %s"%str(address))

	try:
		print("Getting hostname length")
		hostLen = client.recv()
		print("Hostname length: " + str(hostLen))
		host = client.recv(hostLen)
		del hostLen
		print("host %s"%host)
		client.send(time)		
		print("Time sent %d"%time)
		while(True):
			data = client.recv(55)
			if(not data):
				break
			print(fromJSON(data))			
	except:
		print("Something went wrong... %s"%sys.exc_info()[0])
	finally:
		client.shutdown(socket.SHUT_RDWR)
		client.close()

	sockets.remove(client)
	return False

def closeSocket(sock,sockets):
	print("\nClosing sockets")
	for sok in sockets:
		sok.shutdown(socket.SHUT_RDWR)
		sok.close()
	sock.close()
	print("Done")

def closeClient(sock):
	print("Closing client socket")
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

if(__name__ == "__main__"):
	parser = argparse.ArgumentParser(description="Receives WiFi signal strength, mW and dBm, from multiple clients.")
	parser.add_argument("-t", help="Time in seconds to wait until the next signal is sent to the server. Default is 2 seconds.", dest="time", type=int, nargs=1, default=2)
	parser.add_argument("-i", help="Interface to listen on - IP. Default is all interfaces.", dest="LISTEN_IP", type=str, nargs=1, default="0.0.0.0")
	parser.add_argument("-p", help="Port number to listen on. Default is 12000. Need to adjust accordinlgy client side if this is changed.", dest="Port", type=int, nargs=1, default=12000)

	args = parser.parse_args()

	sock = createSocket(args.LISTEN_IP,args.Port)
#	atexit.register(cleanExit,sock)
	listen(sock,args.time)
