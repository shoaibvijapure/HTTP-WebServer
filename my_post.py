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

def post_method(protocol_version, post_data, connection_obj):
	CRLF, CRLF_FOR_POST = "\r\n", "\r\n\r\n"
	'''
		Fetching the data from the client request format.
		Splitting the data based on the CRLF, as we have two CRLF in post message.
	'''
	post_data_extracted = post_data.split(CRLF_FOR_POST)
	'''
		Opening the file if exists, or creating a new one and then appending the data, like the post data into it,
		and writing the data into the file using the file pointer, and then closing the file.
	'''
	file_ptr = open("post_data_logs.txt", 'a')
	file_ptr.write(str(post_data_extracted[1]) + CRLF)
	file_ptr.close()
	flag = True
	'''
		Fetching the file response headers to attach it to the payload.
	'''
	status_code, phrase_value, file_name, file_path	= sub_methods.file_response_headers(flag)
	'''
		Generating the response headers for the same. 
	'''
	phrase_value, connection, content_type, version_ret, status_code, content_length, client_data = sub_methods.generate_response_headers_errors(file_path, status_code, phrase_value, protocol_version, file_name)
	'''
		At the last, appending all the headers to form the actual format of the http response. 
	'''
	payload = sub_methods.generate_data_headers_errors(phrase_value, connection, content_type, version_ret, status_code, content_length, client_data)
	try:
		connection_obj.send(payload.encode())
	except socket.error as s:
		print("Error: {}".format(s))
		sys.exit(1)



