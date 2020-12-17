import os
import sys
import configparser
import parser

config_obj = configparser.ConfigParser() 	# creating the config object of the ConfigParser Class
config_obj.read('conf.ini') 	# reading the .ini file for applying the config values/settings to the server.
documentroot = config_obj.get('config_details', 'DOCUMENT_ROOT')
hostname = config_obj.get('config_details', 'HOSTNAME')
port_number = config_obj.get('config_details', 'PORT_NUMBER')
max_connections = config_obj.get('config_details', 'MAX_CONNECTIONS')
buffer_size = config_obj.get('config_details', 'BUFFER_SIZE')
server_logfile = config_obj.get('config_details', 'LOGFILE_NAME')

'''
	If there is no config.ini/any config file is present at the server. 
	Then, applying the values and then creating the config file corresponding to those values. 
'''
config_obj['config_details'] = {
	'DOCUMENT_ROOT': os.getcwd() + '/index',
	'HOSTNAME': hostname,
	'PORT_NUMBER': port_number,
	'MAX_CONNECTIONS': max_connections,
	'BUFFER_SIZE': buffer_size,
	'LOGFILE_NAME': server_logfile,
} 
with open('./conf.ini', 'w') as file_ptr:
	config_obj.write(file_ptr)

