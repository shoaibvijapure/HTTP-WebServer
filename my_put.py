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

def put_method(protocol_version, request_url, connection_obj, post_data):
	CRLF, CRLF_FOR_PUT = "\r\n", "\r\n\r\n" 
	'''
		The extracted data from the client request is then splitted on the basis of 2 CRLF's at each line of
		the data.
	'''
	put_data = post_data.split(CRLF_FOR_PUT)
	''' The first value of the data list would be the file which is requested.'''
	data_to_be_modify = put_data[1]
	'''
		Checking if the file is present at the server side.
		If present, then open the file path/directory_path.
	'''
	file_found, directory_path = sub_methods.file_exists(request_url)			
	if file_found:
		'''
			Using the file path, opening the file and writing the data according to the 
			requested URI.
		'''
		file_ptr = open(directory_path, "w")
		''' writing the data alongside the CRLF to form the headers. '''
		file_ptr.write(str(data_to_be_modify) + CRLF)
		file_ptr.close()
		''' Setting up the status code to 200, as the file was already present at the server side.
			Ok phrase for the success response.
		'''
		status_code, phrase_value = "200", "Ok"
		''' Fetching the content length for the request file from the file path and using the getsize module. '''
		content_length = os.path.getsize(directory_path)
		'''
			Using the header values, generating the payload from the same and then sending it to the client. '''
		payload = sub_methods.generate_put_response_headers(protocol_version, status_code, phrase_value, directory_path, content_length)
		try:
			connection_obj.send(payload.encode())
		except socket.error as e:
			print("Error: {}".format(e))
			sys.exit(1)
	else:
		'''
			If the file asked by the client is not present at the server side, 
			then create the file at the request URI/URL or file path we got from the client request.
		'''
		file_ptr = open(request_url, "w+") # creating the file at request URI
		file_ptr.write(str(put_data) + CRLF) # writing the data into the file using the file pointer
		file_ptr.close() # closing the file
		''' Setting the status code to 201, as new file created. '''
		status_code, phrase_value = "201", "Created"
		'''
			Getting the size of the file using the directory_path and calculating the content length of the resource.
		'''
		content_length = os.path.getsize(directory_path)
		'''
			Generating the response headers for the put using the above calculated response header values, 
			and then forming it into the payload.
		'''
		payload = sub_methods.generate_put_response_headers(version, status_code, phrase_value, directory_path, content_length)
		try:
			connection_obj.send(payload.encode())
		except socket.error as e:
			print("Error: {}".format(e))
			sys.exit(1)
