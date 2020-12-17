import sys, os
import socket, threading
import time, urllib
import mimetypes
from urllib.parse import urlparse
import logging, configparser

'''
	This function checks for the file which is requested by the client,
	according to the URI, we will check the file name and extension, 
	and if the file is present, setting the flag to True.
'''
def file_exists(request_url):
	'''
		files will have the list of files we have at out server.
		file_found is the flag, directory is the list for filepaths.
	'''
	files, directory, file_found, file_path = [], [], False, os.getcwd()
	''' The os.walk method returns the components of the filepath. '''
	for root_directory, sub_directories, file_name in os.walk(file_path):
		'''
			The file path will be splitted on the basis of the root directory of the file.
			sub-directory and file name will be also splitted.
		'''
		for chunk in file_name:
			''' Here checking the MIME extensions for the file name we got at the server side. '''
			if ".html" or ".txt" or ".pdf" or ".png" or ".jpg" or ".mp3" or ".jpeg" or ".css" or ".js" or ".ico" or ".php" in chunk:
				''' If particular extension found, then add it to the files list. '''
				files.append(chunk)
				''' If the chunk is matching with the request URL/URI, then set the directory where the file is present at the 
					server side, and also setting up the Flag to True.
				'''
				if chunk == request_url:
					directory, file_found = os.path.join(root_directory, chunk), True
	''' return the flag, and file path where the resource is present. '''
	return file_found, directory
	
''' This function will send the responses for the success and 404 error. '''
def file_response_headers(flag):
	# if flag is True, i.e file is founded successfully at the server side.
	if flag:
		status_code, phrase_value = "200", "OK" # setting up the status_code & the phrase_value 
		file_name = "./index/success.html" # path for the page to show if request is successfully completed
		file_path = os.path.realpath(file_name) # fetching the file path 
		return status_code, phrase_value, file_name, file_path 
	else:
		'''
			This means the file requested is not present at the server.
			Setting up the status code, value, file name and it's path, 
			forming the response header values and sending to the response function.
		'''
		status_code, phrase_value,  = "404", "File not found" 
		file_name = "./index/error.html"
		file_path = os.path.realpath(file_name)
		return status_code, phrase_value, file_name, file_path

	
def generate_data_headers(cookies, client_data, extention, version, status_code, phrase_value, connection, content_type, content_length, last_modified):
	if extention == ".html":
		'''
			Forming the message template using the calculated response headers.
			setting the cookie value for the transaction, transforming the final payload.
		'''
		content_type, last_modified, CRLF, status_line, connection, content_length = message_template(phrase_value, connection, last_modified, extention, version, status_code, content_type, content_length)
		cookies = "Set-Cookie: " + cookies + CRLF
		payload = status_line + connection + content_length + content_type + last_modified + cookies + CRLF + client_data
		return payload
	else:
		'''
			If the MIMETYPES is of non - HTML, then form the message template, server won't be storing the cache,
			so no store, and transforming the final payload.
		'''
		content_type, last_modified, CRLF, status_line, connection, content_length = message_template(phrase_value, connection, last_modified, extention, version, status_code, content_type, content_length)
		cache_control = "Cache-Control: no-store" + cookies + CRLF
		payload = status_line + connection + content_length + content_type + last_modified + cache_control + CRLF
		return payload # return the final payload
		
''' 
	This method is used for generating the data headers if we haven't found requested resource
	at the server side. 
'''
def generate_data_headers_errors(phrase_value, connection, content_type, version, status_code, content_length, client_data):
	SP, CRLF = " ", "\r\n" # spaces, crlf values for the response 
	status_line = version + SP + status_code + SP + phrase_value + CRLF # setting the status line
	connection = "Connection: " + connection + CRLF # connection - alive/closed
	content_length = "Content-Length: " + str(content_length) + CRLF 
	content_type = "Content-Type: " + content_type + CRLF
	# transforming all the headers into a payload, returning payload.
	payload = status_line + connection + content_length + content_type + CRLF + client_data
	return payload

''' This method is used for generating the response headers for the errors like file not found etc.. '''
def generate_response_headers_errors(file_path, status_code, phrase_value, protocol_version, file_name):
	file_name, extention = os.path.splitext(file_name)
	try:
		content_length = os.path.getsize(file_path)
		content_type = "text/" + extention[1:] + ";" + "charset=UTF-8"
		connection, file_ptr = "Keep-Alive", open(file_path, "r") # reading the file and setting connection type as alive.
		client_data = file_ptr.read() # reading the client data from the file using file pointer, and close the file.
		file_ptr.close()
		# finally sending the header values to the payload function.
		return phrase_value, connection, content_type, protocol_version, status_code, content_length, client_data
	except:
		pass

''' This method generates response headers for all the methods for this server. '''
def generate_response_headers(if_modified_since, extention, file_name, version, directory_path):
	''' If the resource MIME type is HTML, then generate headers and transforming them to 
		final payload. 
	'''
	if extention == ".html":
		phrase_value = "OK"
		file_name, extention = os.path.splitext(file_name) 
		# setting up the length of the resource, type of the content requested
		content_length, content_type = os.path.getsize(directory_path), extention[1:]
		connection, file_ptr = "Keep-Alive", open(directory_path, "r") # connection type - alive, open file requested
		client_data = file_ptr.read() # read the file and then close it.
		file_ptr.close()	
		try:
			timestamp = os.path.getmtime(directory_path) # fetching the modification time for the request resource.
			# converting the time to string format and GMT Format, for the server and logging purpose.
			modified_time = time.strftime("%a, %d, %b, %Y %H:%M:%S GMT", time.gmtime(timestamp))
			if if_modified_since != modified_time:
				# if the file is modified, send the status_code of 200
				status_code = "200"
			else:
				# if the request resource is not modified, then send the code of 304 to the client in the response.
				status_code, client_data = "304", ""
			cookies = "asdflkjasfdkl1093482094" # cookie value - userid for each transaction through the server.
			# return the final header values and form the payload from these values.
			return modified_time, cookies, client_data, version, status_code, phrase_value, connection, content_type, content_length
		except os.error as e:
			print("Error: {}".format(e)) # catch if any errors
		except ValueError as v:
			print("Error: {}".format(v))
					
	else:
		# if the file MIME type is other/ non-HTML.
		content_list, phrase_value = [], "OK"
		# setting up the content length & also the content type for the request resource, using the guess_type()
		content_length, content_type = os.path.getsize(directory_path), str(mimetypes.guess_type(file_name))
		connection = "Keep-Alive" # setting up connection type to alive
		content_list.append(content_type) # forming the list of all the files asked 
		file_ptr = open(directory_path, "rb") # reading the bytes from the file
		client_data = file_ptr.read() # reading the file & closing it.
		file_ptr.close()
		try:
			timestamp = os.path.getmtime(directory_path) # modification time for the resource
			# converting time into the GMT format, and also into the string format.
			modified_time = time.strftime("%a, %d, %b, %Y %H:%M:%S GMT", time.gmtime(timestamp))
			if str(if_modified_since) == modified_time:
				status_code, client_data = "304", "" # if resource is not modified at the server, send 304 
			else:
				status_code = "200" # if the resource is modified
			cookies = ""
			return modified_time, cookies, client_data, version, status_code, phrase_value, connection, content_type, content_length
		except os.error as e:
			print("Error: {}".format(e))
		except ValueError as v:
			print("Error: {}".format(v))

'''
	This method is used for transforming all the response header values,
	and forming a single response payload.
'''
def message_template(phrase_value, connection, last_modified, extention, version, status_code, content_type, content_length):
	SP, CRLF = " " , "\r\n"
	status_line = version + SP + status_code + SP + phrase_value + CRLF
	connection = "Connection: " + connection + CRLF # connection - alive/closed
	content_length = "Content-Length: " + str(content_length) + CRLF
	content_type = "Content-Type: " + content_type + CRLF # type - text/plain/html
	last_modified = "Last-Modified: " + last_modified + CRLF # last modified time for the resource
	return content_type, last_modified, CRLF, status_line, connection, content_length
	
''' Managing the logs from the server, through the server. '''
def manage_logfile(ip_address, port_number, method_token, url_copy, logfile, request_line):
	logging.basicConfig(filename = logfile, level = logging.INFO, format = "%(asctime)s %(levelname)s %(message)s")
	logging.info("Client IP-Address: {} Request-URL: {} Request-Line: {} Port-Number: {}".format(ip_address, url_copy, request_line, port_number))

''' This function is the main function for extracting the request message values. '''
def extract_headers_data(client_data):
	try:
		if client_data:
			post_data, datalines = client_data, client_data.splitlines() # without splitting on "\n" for post, put.
			request_line = datalines[0].split() # first value is the request line
			# type of the method, request URI/URL, version number
			method_token = request_line[0] # method type
			request_url = request_line[1] # resource request URI
			protocol_version = request_line[2] # version number
			url_copy = request_url
			if_modified_since_ret = if_modified_since(datalines) # if modified since value for the resource
			for chunk in request_url:
				if chunk == "/":
					url_mod = request_url.split('/') # splitting the url on /
			request_url = url_mod[len(url_mod) - 1]		# request url with the resource, without the resource
			''' Return the method name, url with (/) and without (/), the version number, 
			and data lines we got from the http request. '''
			return url_copy, post_data, datalines[0], protocol_version, method_token, request_url, if_modified_since_ret
	except TypeError as t:
		pass
	except IndexError as i:
		pass		

'''
	This method calculates, if modified since time for the requested resource. 
'''
def if_modified_since(datalines):
	check_val, modified_flag, len = "If", False, 0 # val for checking If in the datalines
	for val in datalines:
		if check_val in val: 
			# If we got If in the datalines, then set the flag to True, As the resource is modified
			check_val_temp, modified_flag = check_val, True 
	if not modified_flag:
		# if flag is false, set the check val to False, so that the server will send that no modification is done on the resource.
		check_val_temp = False
		return check_val_temp		
	else:
		# if the flag is set, i.e resource is modified at the server side.
		for val in check_val_temp:
			# incrementing the len until we got the :, to fetch the exact values
			len += 1
			if val == ":": # if we got the chunk as ":", set the value till the ":", and break the loop.
				check_val_temp = check_val_temp[len + 1:]
				break
		return check_val_temp
		
''' This method generates the response for the put method. '''
def generate_put_response_headers(version, status_code, phrase_value, directory_path, content_length):
	SP, CRLF = " ", "\r\n"
	status_line = version + SP + status_code + SP + phrase_value + CRLF # status line, first line for response
	file_location = "Content-Location: " + SP + directory_path + CRLF # file location/path
	content_length_final = "Content-Length: " + SP + str(content_length) # length
	payload = status_line + file_location + content_length_final + CRLF + CRLF # transforming into final payload
	return payload
	
''' This method generates the payload for the Delete method. '''
def generate_payload_for_delete(phrase_value, date, content_type, version, status_code, content_length, file_data):
	SP, CRLF = " ", "\r\n"
	# combining the payload using the SPACES & CRLF lines, returning the final payload for the delete.
	payload = version + SP + status_code + SP + phrase_value + CRLF + date + CRLF + content_type + CRLF + content_length + CRLF + CRLF + file_data
	return payload

def generate_delete_response_headers(directory_path):
	# setting up the status code, value, and last modified time for the resource using the getmtime method.
	phrase_value, status_code, last_modified = "OK", "200", os.path.getmtime(directory_path)
	# converting the time into the GMT type for the server.
	modified = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(last_modified))
	# setting up the final date with time, and also the content type for the resource to be deleted.
	modified_date_time, content_type = "Date: " + modified, "Content-Type: text/html"
	content_length, file_ptr = "Content-Length: " + str(os.path.getsize(directory_path)), open(directory_path, 'r')
	os.remove(directory_path) # just removing the target/requested resource from the server side.
	file_data = file_ptr.read() # reading the file data
	file_ptr.close() # closing the file & returning the response headers.
	return modified_date_time, content_type, status_code, phrase_value, content_length, file_data

'''	This method is for sending the response message for the connect method. '''
def current_date():
	# converting the time from epoch to the local time and into string format.
	val = time.ctime().split(' ')
	val[0] = val[0] + ','
	date = "Date: " + (' ').join(val) # joining the string on the spaces
	return date
