### Project Title: HTTP WEBSERVER

##### MIS - 141808009
##### Name - Shoaib Vijapure


##### Preferred Browser: Mozilla FireFox

Resources Used - RFC 2616, https://www.tutorialspoint.com/http, StackOverFlow, Python Documentation.
Developer has very basic level of knowledge in python, so implementation is based on basic python programming and socket programming.
All parameters of the project and considerations are based on the RFC & resources mentioned. 

##### Server Supports:
1. HTTP Methods: GET, POST, PUT, DELETE, HEAD, CONNECT. (respective files)
2. Log file handling with levels of logging. (Filename - serverlog.log)
3. Server Configuration, config file to config server with DocumentRoot. (config.ini & config.py)
4. Max simulateneous connections. 
5. Automation Script for Testing the server. (automate.py)
6. Cookies, Multithreading.

##### Executing the Project:
host - localhost, port - 12001
1. python3 server.py start (For starting the server)
2. python3 automate.py (For testing the server, using the automation script)

For manually testing, enter in URL bar - localhost:12001/[any file present inside the folder]
example: localhost:12001/site.html

Current working directory + /index - DocumentRoot for the server.
Put files inside the [./index] to execute.

##### NOTE: USE OF INTERNET IS MUST TO LOAD THE WEBSITE BASED ON CSS, JS. Else site will not load properly.
Use Ctrl + C, to stop the server. (STOPPING/RESTARTING is not handled)


Regards.

