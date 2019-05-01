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

def parseUDP():
	#array holding parsed data
    timeBetweenUDP = []
    totalTimeUDP = 0
    file = open("pcktsUDP.txt", "r")
    #content is an array that contains each line of the "pckts.txt" as its own element 
    contents = file.readlines()
    for line in contents:
        # if "Time since first frame:" in line:
        # 	totalTimeUDP += re.findall(r'[-+]?\d*\.\d+|\d+', line)

        if "Time since previous frame:" in line:
        	timeBetweenUDP += re.findall(r'[-+]?\d*\.\d+|\d+', line)

    file.close()

    for i in timeBetweenUDP:
        totalTimeUDP += float(i)

    print("UDP time data :")
    print(timeBetweenUDP)
    print("total time: \n")
    print(totalTimeUDP)

def parseSeqAck(sequence,acknowledgment):
    # store tuple
    seqAck = (("SEQ: "+ str(sequence)),("ACK: " + str(acknowledgment)))
    # print (str(seq) + " , " + str(ack))
    packetSeqAck.append(seqAck)

    return(packetSeqAck)


def parse():
    #array holding parsed data
    timeBetweenTCP = []
    totalTimeTCP = 0
    seq = 0
    ack = 0
    file = open("pcktsTCP.txt", "r")
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

    # print(packetSeqAck)
    for i in timeBetweenTCP:
        totalTimeTCP += float(i)

    print("TCP time timeBetweenTCP")
    print(timeBetweenTCP)

    print("total time TCP: \n")
    print(totalTimeTCP)
    #Parse
    # for line in contents:
    #     firstParse.append(line.strip()) # add line to array as we pass through (strip removes newline)
    #     print(line.strip()) # print lines as we're going through file

    file.close()

# Main starts here

print("Starting with TCP")

numPackets = int(input("Enter # packets to capture : "))
print("Please wait while packets accumulate...")

#Redirect all output from "prints" to a file called "pckts.txt" (change the path to work on your machine)
file = open("pcktsTCP.txt", "w")
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
print("parse finished running")

print("Now parsing UDP")

numPackets = int(input("Enter # of UDP packets to capture : "))
print("Please wait while packets accumulate...")

#Redirect all output from "prints" to a file called "pckts.txt" (change the path to work on your machine)
file = open("pcktsUDP.txt", "w")
sys.stdout = file

#LiveCapture with the selected interface : 'Wi-Fi'
capture = pyshark.LiveCapture(interface='Wi-Fi')
capture.sniff(packet_count=numPackets)

print(capture)
for pkt in capture:
    #this allows for the for loop to be exectued until the counter reaches our desired time limit
    #if(time.time() < t_end):
    print (pkt)

file.close()
sys.stdout = sys.__stdout__


print ("Capture Data Finished")
parseUDP()
print("UDP parse finished running")
