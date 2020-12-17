import os, sys, socket
import threading
import time, mimetypes
from urllib.parse import urlparse
import logging, configparser
import server, sub_methods

def get_method(protocol_version, if_modified_since_ret, url_copy, request_url, connection_obj):
	''' urlparse() splits the url format like 
		---- scheme://netloc/path;parameters?query#fragment ----
		into separate components. 
	'''  
	url_components = urlparse(url_copy)
	if url_components[4] == "":
		'''
			Checking if the file requested is present at the server side or not.
			If present, file_found is set to True, else False.
		'''
		file_found, directory_path = sub_methods.file_exists(request_url)
		if file_found:
			'''
				Extracting the filename and it's type of MIME, i.e file extension.
			'''
			file_name, extension = os.path.splitext(request_url)
			if extension == ".html":
				'''
					Generating the response headers for the .html MIME format, 
					then generating the data headers, merging them to form the actual payload.
				'''
				modified_time, cookies, client_data, version_ret, status_code, phrase_value, connection, content_type, content_length = sub_methods.generate_response_headers(if_modified_since_ret, extension, file_name, protocol_version, directory_path)
				payload = sub_methods.generate_data_headers(cookies, client_data, extension, version_ret, status_code, phrase_value, connection, content_type, content_length, modified_time)
				try:
					''' Encoding the payload, and sending it to the client. '''
					connection_obj.send(payload.encode())
					''' Sending the actual data fetched from the requested file, and sending it. '''
					connection_obj.send(client_data)
				except socket.error as e:
					print("Error: {}".format(e))
					sys.exit(1)
				except TypeError as t:
					sys.exit(1)
			else:
				'''
					Generating the response headers for the other types of MIME formats, 
					then generating the data headers, merging them to form the actual payload.
				'''	
				modified_time, cookies, client_data, version_ret, status_code, phrase_value, connection, content_type, content_length = sub_methods.generate_response_headers(if_modified_since_ret, extension, file_name, protocol_version, directory_path)
				payload = sub_methods.generate_data_headers("", "", extension, version_ret, status_code, phrase_value, connection, content_type, content_length, "")
				if client_data:
					''' Encoding the payload & client data, and sending it to the client. '''
					try:
						connection_obj.send(payload.encode())
						connection_obj.send(client_data)
					except socket.error as e:
						print("Error: {}".format(e))
						sys.exit(1)
				else:
					''' Encoding the payload, and sending it to the client. '''
					try:
						connection_obj.send(payload.encode())
					except socket.error as e:
						print("Error: {}".format(e))
						sys.exit(1)
		else:
			'''
				The file, client is requesting is not found at the server side,
				generate the response headers for the error response, and same for the data headers.
			'''
			flag = False
			status_code, phrase_value, file_name, file_path = sub_methods.file_response_headers(flag)
			''' Generate the error headers. '''
			phrase_value, connection, content_type, version_ret, status_code, content_length, client_data = sub_methods.generate_response_headers_errors(file_path, status_code, phrase_value, protocol_version, file_name)
			''' Generate the payload and then send it back to the client. '''
			payload = sub_methods.generate_data_headers_errors(phrase_value, connection, content_type, version_ret, status_code, content_length, client_data)
			try:
				connection_obj.send(payload.encode())
			except socket.error as t:
				print("Error: {}".format(t))
				sys.exit(1)

	else:
		'''
			Open a file for appending new info in it. 
			New file is created if one with the same name don't exits.
		'''
		client_data = str(urllib.parse.parse_qs(url_components[4], keep_blank_values = "True", strict_parsing = "False"))
		CRLF, file_ptr = "\r\n", open("shoaib.txt", "a")	
		file_ptr.write(client_data + CRLF)
		file_ptr.close()
		'''
			Applying the changes/transformations according to the file response headers. 
		'''
		status_code, phrase_value, file_name, file_path = sub_methods.file_response_headers(flag)
		'''
			Generating the error headers, for the client request and then sending back the response,
			in the form of the payload.
		'''
		phrase_value, connection, content_type, version_ret, status_code, content_length, client_data = sub_methods.generate_response_headers_errors(file_name, version_ret, file_path, status_code, phrase_value)
		payload = sub_methods.generate_data_headers_errors(phrase_value, connection, content_type, version_ret, status_code, content_length, client_data)
		try:
			connection_obj.send(payload.encode())
		except socket.error as e:
			print("Error: {}".format(e))
			sys.exit(1)
		
		
