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
		buffr = ""
		host = ""
		
		while(host == ""):
			buff = client.recv(32)
			buffr += buff
			if('\n' in buffr):
		#		print("Buffr before gettint host: %sNL"%buffr)
				indx = buffr.index('\n')
		#		print("indx: %d"%indx)
				host = buffr[:indx]
				buffr = buffr[indx+1:]
		#		print("Buffr: >%s<"%buffr)

		print("Host connected: %s"%host)
		client.send(str(time) + "\n")
#		print("Time sent %d"%time)

		while(True):
			buff = client.recv(32)
			if(not buff):
				break
			
			buffr += buff
			
			if('\n' in buff):	
				indx = buffr.index('\n')
	#			print("buffr: %s"%buffr)
#				print("data: %s"%buffr[:indx])
				data = fromJSON(buffr[:indx])
				buffr = buffr[indx+1:]
				processData(host,data)
	except Exception, e:
		print("\nSomething went wrong... %s"%e)
	finally:
		print("Closing socket: %s"%host)
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

def processData(host,data):
	print("%s\n%s\n"%(host,data))

if(__name__ == "__main__"):
	parser = argparse.ArgumentParser(description="Receives WiFi signal strength, mW and dBm, from multiple clients.")
	parser.add_argument("-t", help="Time in seconds to wait until the next signal is sent to the server. Default is 2 seconds.", dest="time", type=float, nargs=1, default=2.0)
	parser.add_argument("-i", help="Interface to listen on - IP. Default is all interfaces.", dest="LISTEN_IP", type=str, nargs=1, default="0.0.0.0")
	parser.add_argument("-p", help="Port number to listen on. Default is 12000. Need to adjust accordinlgy client side if this is changed.", dest="Port", type=int, nargs=1, default=12000)

	args = parser.parse_args()

	sock = createSocket(args.LISTEN_IP,args.Port)
#	atexit.register(cleanExit,sock)
	if(type(args.time) != float):
		args.time = float(args.time[0])
	listen(sock,args.time)
