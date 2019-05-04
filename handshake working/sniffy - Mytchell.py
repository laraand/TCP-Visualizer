<<<<<<< HEAD
import pyshark
import webbrowser
import time
import sys
import re


#Variables
#filename = "c:\\Users\\Mytchell\\Desktop\\pckts.txt"
packetSeqAck = []  
seqAck = (0,0) 
# Windows - This can be used to open the chrome browser from this script with a specified link
# url = 'http://docs.python.org/'
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(url)
##################################################################################################

def parseSeqAck(sequence,acknowledgment):
    # store tuple
    seqAck = (("SEQ: "+ str(sequence)),("ACK: " + str(acknowledgment)))
    # print (str(seq) + " , " + str(ack))
    packetSeqAck.append(seqAck)

    return(packetSeqAck)


def parse():
    #array holding parsed data
    timeBetweenTCP = []
    seq = 0
    ack = 0
    file = open("pckts.txt", "r")
    #content is an array that contains each line of the "pckts.txt" as its own element 
    contents = file.readlines()

        #Parse
    for line in contents:
        if "Time since previous frame in this TCP stream:" in line:
            timeBetweenTCP += re.findall(r'[-+]?\d*\.\d+|\d+', line)

    # for line in contents:
        if "Sequence number:" in line:
            seq = re.findall(r'\d+', line)

        if "Acknowledgment number:" in line:
            ack = re.findall(r'\d+', line)

            parseSeqAck(seq,ack)
        # # store tuple
        #     seqAck = (seq,ack)
        # # print (str(seq) + " , " + str(ack))
        #     packetSeqAck.append(seqAck)

    print(packetSeqAck)


    print(timeBetweenTCP)
    #Parse
    # for line in contents:
    #     firstParse.append(line.strip()) # add line to array as we pass through (strip removes newline)
    #     print(line.strip()) # print lines as we're going through file

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
    print (pkt)

file.close()
sys.stdout = sys.__stdout__

print ("Capture Data Finished")
parse()
=======
import pyshark
import webbrowser
import time
import sys
import re


#Variables
#filename = "c:\\Users\\Mytchell\\Desktop\\pckts.txt"
packetSeqAck = []  
seqAck = (0,0) 
# Windows - This can be used to open the chrome browser from this script with a specified link
# url = 'http://docs.python.org/'
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(url)
##################################################################################################

def parseSeqAck(sequence,acknowledgment):
    # store tuple
    seqAck = (("SEQ: "+ str(sequence)),("ACK: " + str(acknowledgment)))
    # print (str(seq) + " , " + str(ack))
    packetSeqAck.append(seqAck)

    return(packetSeqAck)


def parse():
    #array holding parsed data
    timeBetweenTCP = []
    seq = 0
    ack = 0
    file = open("pckts.txt", "r")
    #content is an array that contains each line of the "pckts.txt" as its own element 
    contents = file.readlines()

        #Parse
    for line in contents:
        if "Time since previous frame in this TCP stream:" in line:
            timeBetweenTCP += re.findall(r'[-+]?\d*\.\d+|\d+', line)

    # for line in contents:
        if "Sequence number:" in line:
            seq = re.findall(r'\d+', line)

        if "Acknowledgment number:" in line:
            ack = re.findall(r'\d+', line)

            parseSeqAck(seq,ack)
        # # store tuple
        #     seqAck = (seq,ack)
        # # print (str(seq) + " , " + str(ack))
        #     packetSeqAck.append(seqAck)

    print(packetSeqAck)


    print(timeBetweenTCP)
    #Parse
    # for line in contents:
    #     firstParse.append(line.strip()) # add line to array as we pass through (strip removes newline)
    #     print(line.strip()) # print lines as we're going through file

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
    print (pkt)

file.close()
sys.stdout = sys.__stdout__

print ("Capture Data Finished")
parse()
<<<<<<< HEAD
>>>>>>> 7c694684b63d77a0125ffdf4db4822fbab856c16
=======
>>>>>>> 217299bcd017fb1a3dad6d3907531874df0bdf22
>>>>>>> a3e5d35ab46bc10c5554a438b7ed2ae4f884c767
print("parse finished running")