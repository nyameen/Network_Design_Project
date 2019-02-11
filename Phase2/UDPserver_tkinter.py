import socket
import select
import time
from tkinter import *
from PIL import Image, ImageTk

# Had error with ImageTk


# function to send an image
# insert file name in sendto and open functions
def sendImg(socket, client):
	# send name of file
    socket.sendto('file.png'.encode('utf-8'), client)
    
    print ("Sending...")

	# open that image for reading binary
    f = open("file.png", "rb")
	
	# read 1024 bytes
    data = f.read(1024)

	# while theres data keep sending
    while(data):
		# send 1024 bytes to client
        if(socket.sendto(data, client)):
			# read another 1024
            data = f.read(1024)
			# slight delay
            time.sleep(0.02)


def main():


    UDP_IP = "127.0.0.1"    # Server IP
    IN_PORT = 12001         # port
    timeout = 3				# timeout


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# open a UDP socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# set the socket options to reuse address and port
    sock.bind((UDP_IP, IN_PORT))								# bind to address and port

    # forever
    while True:
        data, addr = sock.recvfrom(1024)		# receive from client
        if data:
            data.decode
            print ("File name:", data)			# print file received
            file_name = data.strip()			# strip the header

        f = open(file_name, 'wb')				# open that file for writing binary

        while True:
            ready = select.select([sock], [], [], timeout) # wait until sock is ready for I/O
            if ready[0]:
                data, addr = sock.recvfrom(1024)	# receive 1024 from client
                f.write(data)						# write it to a file
            else:
                print ("%s Finish!" % file_name)	# finished writing 
                f.close()							# close file
                break

       

        sendImg(sock, addr)



if __name__ == "__main__":


    #key down function
    def click():
               
        for widget in window.winfo_children():
            widget.destroy()

        Label (window, text="Waiting for Client to be started....",bg ="black", fg ="white", font = "none 12 bold") .grid(row = 1, column = 0,)
       
        Label(window, image = photol2) .grid(row = 0, column = 0)

        main()

    #### main
    window = Tk()
    window.title("UDP Server")
    window.configure(background = "black")
    window.geometry("350x400") 
    #### photo 
    photol = PhotoImage(file = "C:\\Users\\Blaine\\Documents\\Network Design\\server.png")
    photol2 = PhotoImage(file = "C:\\Users\\Blaine\\Documents\\Network Design\\l.png")
    image_1 = Label(window, image = photol, bg = "black") .grid(row = 0, column = 0)

    #### create a label
    Label (window, text="Would you like to receive images from client? ",bg ="black", fg ="white", font = "none 12 bold") .grid(row = 1, column = 0, sticky = W)

    #### add a submit button
    Button(window, text = 'RUN', width = 6, command=click) .grid(row = 8, column = 0,)

    #### run the main loop
    window.mainloop()

  

