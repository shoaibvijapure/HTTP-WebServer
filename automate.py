import webbrowser, os, sys # importing for opening the browser for testing the server.
from socket import * # for socket programming
s = socket(AF_INET, SOCK_DGRAM)
try:
	s.connect(("", "12001"))   # localhost and port will be 12001.
except:
	pass
s.close()

request_url = "http://" + "localhost:12001/"
def test(url = (request_url)):
    webbrowser.open_new_tab(url)

'''
	By using the test fuction in python to automatically opening the URL passed to the function.
	This will open the browser, which is the default one at the system on which this code is to be executed. 
	Preferred browser will be MOZILLA FIREFOX. 
'''
test(request_url + "link.html")
test(request_url + "") 
test(request_url + "home.html")
test(request_url + "login.html")
test(request_url + "demo.txt")
test(request_url + "sports.jpeg")
test(request_url + "timetable.pdf")
test(request_url + "site.html")
test(request_url + "post.html")
