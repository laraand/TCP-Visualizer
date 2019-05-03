import pyshark
import webbrowser
import time
import sys
import re


#Variables
#filename = "c:\\Users\\Mytchell\\Desktop\\pckts.txt"

# Windows - This can be used to open the chrome browser from this script with a specified link
# url = 'http://docs.python.org/'
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(url)
##################################################################################################


def parse():
    #array holding parsed data
    firstParse = []
    file = open("pckts.txt", "r")
    #content is an array that contains each line of the "pckts.txt" as its own element 
    contents = file.readlines()

    #Parse
    for line in contents:
        firstParse.append(line.strip()) # add line to array as we pass through (strip removes newline)
<<<<<<< HEAD
        print(line.strip()) # print lines as we're going through file
=======
        #print(line.strip()) # print lines as we're going through file
        print(line)
>>>>>>> 7c694684b63d77a0125ffdf4db4822fbab856c16

    file.close()

# Main starts here
numPackets = int(input("Enter # packets to capture : "))
print("Please wait while packets accumulate...")

#Redirect all output from "prints" to a file called "pckts.txt" (change the path to work on your machine)
file = open("pckts.txt", "w")
sys.stdout = file

#LiveCapture with the selected interface : 'Wi-Fi'
capture = pyshark.LiveCapture(interface='Wi-Fi')
capture.sniff(packet_count=numPackets)

#Printing (stdout being directed to file 'pckts.txt')
print(capture)
for pkt in capture:
    #this allows for the for loop to be exectued until the counter reaches our desired time limit
    #if(time.time() < t_end):
<<<<<<< HEAD
    print (pkt)
=======
    if (pkt.transport_layer != "UDP"):
        print (pkt.transport_layer)
    else:
        print("Thats UDP Garbage\n")
        numPackets += 1
>>>>>>> 7c694684b63d77a0125ffdf4db4822fbab856c16

file.close()
sys.stdout = sys.__stdout__

print ("Capture Data Finished")
parse()
<<<<<<< HEAD
=======
print(numPackets)
>>>>>>> 7c694684b63d77a0125ffdf4db4822fbab856c16
print("parse finished running")
