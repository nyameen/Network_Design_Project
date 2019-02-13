import _thread
from tkinter import *
from PIL import Image, ImageTk


class Main():

	def Client():
		from UDPclient import main
		thread.start_new__thread(main)
	def Server():
		from UDPserver import main
		main()
	def Exit():
		exit()
	


	#### main
	window = Tk()
	window.title("UDP Server")
	window.configure(background = "black")
	window.geometry("300x450") 

	#### photo 
	photol = PhotoImage(file = "C:\\Users\\Blaine\\Documents\\Network Design\\server.png")
	image_1 = Label(window, image = photol, bg = "black") .grid(row =0, column = 0,sticky = W)

	#### buttons for server, client, exit 
	Button (window, text = "Client", width = 6, command =  Client) .grid(row = 4, column = 0, padx = 5, pady= 5)
	Button (window, text = "Server", width = 6, command = Server) .grid(row = 3, column = 0)
	Button (window, text = "Exit", width = 6, command = Exit) .grid(row = 6, column = 0)
	
	#### run the main loop
	window.mainloop()

