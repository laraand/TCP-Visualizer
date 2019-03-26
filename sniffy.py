import pyshark
import webbrowser
import time
import sys
import re


#Variables
filename = "c:\\Users\\ZerkaX205TA\\Desktop\\pckts.txt"

# Windows - This can be used to open the chrome browser from this script with a specified link
# url = 'http://docs.python.org/'
# chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(url)
##################################################################################################


def parse():
	#array holding parsed data
	firstParse = []
	file = open(filename, "r")
	#content is an array that contains each line of the "pckts.txt" as its own element 
	contents = file.readlines()

	#Parse
	for line in contents:
		if "Time since previous frame:" in line:
			firstParse += re.findall(r'[-+]?\d*\.\d+|\d+', line)

	#Print
	print(firstParse)

	#*For Testing purposes*
	#-------------------------------------------------------------------------------------
	#this print statement prints an array that is lists each line of the "pckts.txt" file as an element in the array
	# print(contents)

	#This For-loop prints out the "pckts.txt" file
	# for line in contents:
	# 	print(line)

	file.close()

def main():

	#time
	#time to wait
	ttw = int(input("Enter time : "))
	t_end = time.time() + ttw		#60 * 15 #This will run for 15 min x 60 s = 900 seconds.
	print("Please wait while packets accumulate...")

	#Redirect all output from "prints" to a file called "pckts.txt" (change the path to work on your machine)
	file = open(filename, "w")
	sys.stdout = file

	
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

	file.close()
	sys.stdout = sys.__stdout__

	print ("Finished")
	parse()
	print("parse finsihed running")

#Start at main
if __name__ == '__main__':
	main()