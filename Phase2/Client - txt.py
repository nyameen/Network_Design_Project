import socket
import random
import select
import sys
import os 
from os import path

from socket import *



def send_file():
	
	#First verify file is available 
	print(os.listdir("C:\\Users\\Blaine\\Documents\\Network Design\\Phase_1_1"))
	check = os.path.isfile('C:\\Users\\Blaine\\Documents\\Network Design\\Phase_1_1\\yo.txt.txt')
	

	if (check):

		#Perform Client Protocols 
		HOST = '127.0.0.1'
		PORT = 5003
		server = (HOST,PORT)
		
		
		#Create the client socket 
		sock = socket(AF_INET, SOCK_DGRAM)
		destination = (HOST,PORT)
		sock.connect(destination)

		#Send contents from text file 
		while (True):
						
			f = open("C:\\Users\\Blaine\\Documents\\Network Design\\Phase_1_1\\yo.txt.txt",'rb')

			bytesToSend = f.read(1024)
			print(bytesToSend)
			
			sock.sendto(bytesToSend,destination)
			sock.close()			


def main():

	send_file()



if __name__ == "__main__":

	main()



	