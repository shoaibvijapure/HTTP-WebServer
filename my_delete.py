import os, sys
import socket, threading
import time, urllib
import mimetypes
from urllib.parse import urlparse
import logging, configparser
import server, sub_methods


def delete_method(protocol_version, request_url, connection_obj):
	file_found, directory_path = sub_methods.file_exists(request_url)
	if file_found:
		'''
			If the file is present at the server side, then generate the respective response headers,
			payload for the delete and then sending back to the client.
		'''
		date, content_type, status_code, phrase_value, content_length, file_data = sub_methods.generate_delete_response_headers(directory_path)
		'''
			Generating the payload by combining the response headers. 
		'''
		payload = sub_methods.generate_payload_for_delete(phrase_value, date, content_type, protocol_version, status_code, content_length, file_data)
		try:
			connection_obj.send(payload.encode())
		except socket.error as e:
			print("Error: {}".format(e))
			sys.exit(1)
	else:
		'''
			Setting up the flag to false. According to the flag values, generate the file response headers,
			and generating the data header errors and then sending them. 
		'''
		flag = False
		status_code, phrase_value, file_name, file_path = sub_methods.file_response_headers(flag)
		'''
			Generating the error headers for the post also, it the requested form/file is not present 
			at the server side. 
		'''
		phrase_value, connection, content_type, version_ret, status_code, content_length, client_data = sub_methods.generate_response_headers_errors(file_path, status_code, phrase_value, protocol_version, file_name)
		'''
			Generating the payload & then send it to the client side. 
		'''
		payload = sub_methods.generate_data_headers_errors(phrase_value, connection, content_type, version_ret, status_code, content_length, client_data)
		try:
			connection_obj.send(payload.encode())
		except socket.error as s:
			print("Error: {}".format(s))
			sys.exit(1)
