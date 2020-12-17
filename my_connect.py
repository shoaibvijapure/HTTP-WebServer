import os  
import sys
import socket
import threading
import time
import urllib
import mimetypes
from urllib.parse import urlparse
import logging
import configparser
import server, sub_methods

def connect_method(connection_obj):
	'''
		Establishing a tunnel along to the server,
		generating the payload format and then sending it to the client. 
	'''
	socket_obj, buffer_size, logfile = server.start_server()
	ip_address = server.connect(socket_obj, buffer_size, logfile)
	CRLF, SP = "\r\n", " "
	status_code = "204" + SP
	message = "HTTP/1.1 204 No Content" + CRLF
	server = "Server: " + ip_address + CRLF
	connection = "Connection: Keep-Alive" + CRLF
	date = sub_methods.current_date() + CRLF
	'''
		Forming the actual payload/response message by attaching the header values. 
	'''
	payload = status_code + message + server + connection + date
	try:
		connection_obj.send(payload.encode())
	except socket.error as e:
		print("Error: {}".format(e))
		sys.exit(1)
		

