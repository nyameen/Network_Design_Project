import socket 
import sys 
from socket import *
import os.path
import os


#Function to transfer text file 
def Transfer_Text_File():

	#Server Protocols 
	PORT = 5003
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	sock.bind(('',PORT))


	print("Server is waiting......")

	while(True):
					
		#Open new file and write to it messages from client file 			
		with open('C:\\Users\\Blaine\\Documents\\Network Design\\Phase_1_1\\new_file.txt','a') as f:   

			while(f):

				data,client = sock.recvfrom(1024) 
				
				message = list()  #Turn content into a string 
				message  = data.decode('ascii')  

				f.write(message)  

				f.close()

		sock.close()
		


def main():
	
	#Accept input from user 
	user = input("Hello would you like to create a new text file?  -> Y/N")

	if(user == 'Y'):

		Transfer_Text_File()  #File contents will be received via port 5000 and new file will be constructed 
		

	else:

		print("No files will be transfered")



if __name__ == "__main__":

	main()

