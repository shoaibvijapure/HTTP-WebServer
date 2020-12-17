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

def head_method(protocol_version, if_modified_since_ret, request_url, connection_obj):
	'''
		Check if the file is present or nothing at the server side.
		Fetching the file path & file found flag.
	'''
	file_found, directory_path = sub_methods.file_exists(request_url)
	if file_found:
		'''
			If the file is found at the server side, then check for all the available mimetypes and then form the,
			response headers and the payload for the same.
		'''
		file_name, extension = os.path.splitext(request_url)
		if extension == ".html" or extension == ".txt" or extension == ".jpeg" or extension == ".pdf" or extension == ".png" or extension == ".jpg" or extension == ".mp3" or extension == ".css" or extension == ".gif" or extension == ".js" or extension == ".ico" or extension == ".php":
			''' Generating the response headers for the head method. '''
			modified_time, cookies, client_data, version_ret, status_code, phrase_value, connection, content_type, content_length = sub_methods.generate_response_headers(if_modified_since_ret, extension, file_name, protocol_version, directory_path)
			''' Generating the data headers and then encoding it into a payload and sending it at the client side. '''
			payload = sub_methods.generate_data_headers("", "", extension, version_ret, status_code, phrase_value, connection, content_type, content_length, "")
			try:
				connection_obj.send(payload.encode())
			except socket.error as e:
				print("Error: {}".format(e))
				sys.exit(1)
	else:
		'''
			If file is not present at the server/file doesn't exists then set the flag to false. 
		'''
		flag = False
		'''
			As the file is not present at the server side, generate the file response headers according to the,
			current status code at the server. 
		'''
		status_code, phrase_value, file_name, file_path = sub_methods.file_response_headers(flag)
		'''
			Generate the response & data headers for the error code like the 404. 
		'''
		phrase_value, connection, content_type, version_ret, status_code, content_length, client_data = sub_methods.generate_response_headers_errors(file_path, status_code, phrase_value, protocol_version, file_name)
		payload = sub_methods.generate_data_headers_errors(phrase_value, connection, content_type, version_ret, status_code, content_length, client_data)
		try:
			connection_obj.send(payload.encode())
		except socket.error as e:
			print("Error: {}".format(e))
			sys.exit(1)
