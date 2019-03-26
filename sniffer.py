import pyshark
import webbrowser
import time
import sys


#Variables
# Windows - This can be used to open the chrome browser from this script with a specified link
# url = 'http://docs.python.org/'
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(url)

#time
t_end = time.time() + 20		#60 * 15 #This will run for 15 min x 60 s = 900 seconds.

#Redirect all output from "prints" to a file called "pckts.txt" (change the path to work on your machine)
sys.stdout = open("c:\\Users\\Andrea\\Desktop\\pckts.txt", "w")

#LiveCapture with the selected interface : 'Wi-Fi'
capture = pyshark.LiveCapture(interface='Wi-Fi')

#Printing (stdout being directed to file 'pckts.txt')
print(capture)
for pkt in capture:
	#this allows for the for loop to be exectued until the counter reaches our desired time limit
	if(time.time() < t_end):
		print (pkt)
		print("----------------------------")
		#For testing purposes
		print(time.time())
		print(t_end)
	else:
		break

print ("Finished")
