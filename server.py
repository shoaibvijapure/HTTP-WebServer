import os, sys, socket # to use basic functinalities like checking path, file, directory, arguments, exiting, socket handling
import threading, time # for handling multithreaded requests, for fetching the time related values
import mimetypes # for getting mimetypes, like the extension for the requested files
from urllib.parse import urlparse # for parsing/spliting the URL/URI
import logging # for logfile handling
import configparser # for config related handling
import sub_methods, my_get, my_post, my_put, my_delete, my_head, my_connect # method modules imported

'''
	This method is the basic socket connection method & threading.  
'''
def connect(socket_obj, buffer_size, logfile):
	connection_obj, address = socket_obj.accept()
	ip_address, port_number = address[0], address[1]	
	''' This line enabled threading on the handle function, arguments are passed for the same. ''' 		
	handle_thread = threading.Thread(target = handle, args = (port_number, buffer_size, logfile, connection_obj, ip_address))
	''' program will end at the shutdown. '''
	handle_thread.daemon = True
	handle_thread.start()
	return ip_address
		
''' 
	This method reads a config file and allocates the value according to the,
	configuration provided in the file. 
'''
def start_server():
	config_obj = configparser.ConfigParser()
	config_obj.read("conf.ini") # reading from the conf.ini file else creating the one using config.py
	documentroot = config_obj.get('config_details', 'DOCUMENT_ROOT') # setting up the document root for the server
	hostname = config_obj.get('config_details', 'HOSTNAME') # hostname
	port_number = int(config_obj.get('config_details', 'PORT_NUMBER')) 
	max_connections = config_obj.get('config_details', 'MAX_CONNECTIONS') # max no. of simultaneous connections
	buffer_size = int(config_obj.get('config_details', 'BUFFER_SIZE')) # buffer size for the server
	logfile = config_obj.get('config_details', 'LOGFILE_NAME') # setting up the logfile for the server activities
	''' Creating the connection socket object, to enable the socket programming. '''
	socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	''' This line does the job of continuously re-using the same address & port alloted to the server. '''
	socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	socket_obj.bind((hostname, port_number)) # binding the host to the port number
	socket_obj.listen(5)
	return socket_obj, buffer_size, logfile
	
'''
	This method is for initialising the server, setting according to the config values,
	setting up the sockets, ports and then starting it. 
'''
def initialise():
	socket_obj, buffer_size, logfile = start_server()
	while True:
		try:
			connect(socket_obj, buffer_size, logfile)
			''' On keyboard interrupt, stop the server and close the socket objects. '''
		except KeyboardInterrupt:
			print("\nServer is stopped!\n")						
			break
	socket_obj.close() # closing the connection socket.
					
'''
	This is the main method of the project. It is the multithreaded function for handling all the,
	server related tasks/requests. 
'''
def handle(port_number, buffer_size, logfile, connection_obj, ip_address):
	while True:
		try:
			''' Receiving the data from the clients connected to the server. Then printing the actual request message,
				sent by the client. 
			'''
			client_data = connection_obj.recv(buffer_size).decode("UTF-8") # decoding the client request, using the UTF-8
			print(client_data)
			if client_data:
				'''
					Extracting the headers, values, message body from the client request. 
					Maintaining the logs for each and every tasks/activities performed by/through the server. 
				'''
				url_copy, post_data, request_line, protocol_version, method_token, request_url, if_modified_since_ret = sub_methods.extract_headers_data(client_data)		
				sub_methods.manage_logfile(ip_address, port_number, method_token, url_copy, logfile, request_line)
				
				''' After extracting the request, just check the request on the basis of the method token. '''
				if method_token == "GET":
					'''
						1. This method retreives the information from the server using the given URI.
						2. This method should retrieve the data, and should have no effect on the data. 
					'''
						
					my_get.get_method(protocol_version, if_modified_since_ret, url_copy, request_url, connection_obj)
												
				elif method_token == "POST":
					''' This method is used to send the data to the server using the HTML forms etc. '''
					my_post.post_method(protocol_version, post_data, connection_obj)
					
					
				elif method_token == "PUT":
					'''
						This method replaces the data in the existing file at the server, 
						or may create new file at the server if there is no one existing.
					'''
					my_put.put_method(protocol_version, request_url, connection_obj, post_data)
					
				elif method_token == "DELETE":
					''' This method remove all current representations of the target resource given by URI. '''
					my_delete.delete_method(protocol_version, request_url, connection_obj)
					
				elif method_token == "HEAD":
					''' Same as the GET, but only transfers the status line and the header section, no body. '''
					my_head.head_method(protocol_version, if_modified_since_ret, request_url , connection_obj)

				elif method_token == "CONNECT":
					''' Establishes a tunnel/seperate path to the server identified by the given URI/URL. '''
					my_connect.connect_method(connection_obj)
			else:
				sys.exit(1)	
		except socket.error as error_value:
			if not client_data:
				print("Error while receiving the data from the client: {}".format(error_value))
				break
		
if __name__ == "__main__":
	if sys.argv[1] == 'start':
		''' when the server is requested for the starting, initialize it with the config values. '''
		initialise()
	else:
		print("Usage: python3 server.py [start]\n")
