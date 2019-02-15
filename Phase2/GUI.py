import threading
from tkinter import *
from PIL import Image, ImageTk
from _thread import *
import os 


def Client(cb):
	from UDPclient import UDPclient
	entered_text = textentry.get()
	f = None
	if entered_text:
		f = os.path.join(current_dir, entered_text)
		print(f'Client to send file: {f}')
	client = UDPclient(f, cb)
	t1 = threading.Thread(target = client.start_send)
	t1.start()

def Server():
	from UDPserver import UDPserver 
	entered_text = textentry.get()
	f = None
	if entered_text:
		f = os.path.join(current_dir, entered_text)
		print(f'Server response file is {f}')
	server = UDPserver(f)
	t2 = threading.Thread(target = server.listen)
	t2.start()

def Exit():
	exit()

server_png = 'server.png'
current_dir = os.getcwd()
server_photo_path = os.path.join(current_dir, server_png)

#### main
window = Tk()
window.title("UDP Server")
window.configure(background = "black")
window.geometry("550x450") 

#### add server photo 
pil_img = Image.open(server_photo_path)
server_photo = ImageTk.PhotoImage(pil_img)
image_1 = Label(window, image = server_photo, bg = "black").grid(row =0, column = 0,sticky = W)

server_text = StringVar()
Label (window, textvariable=server_text, bg ="black", fg ="white", font = "none 10 bold") .grid(row = 3, column = 4)

client_text = StringVar()
Label (window, textvariable=client_text, bg ="black", fg ="white", font = "none 10 bold") .grid(row = 4, column = 4)

def run_server():
	server_text.set("Server listening...")
	Server()

def client_callback():
	client_text.set("Client finished.")

def start_client():
	client_text.set("Client working...")
	Client(client_callback)

#### buttons for server, client, exit 
Button (window, text = "Start Client", width = 8, command = start_client) .grid(row = 4, column = 0, padx = 5, pady= 5)
Button (window, text = "Start server", width = 8, command = run_server) .grid(row = 3, column = 0)
Button (window, text = "Exit", width = 8, command = Exit) .grid(row = 5, column = 0)

#### text entry for image path
Label (window, text="Specify Image to send:",bg ="black", fg ="white", font = "none 12 bold") .grid(row = 0, column = 4)

#### create a text entry
textentry = Entry(window, width = 20, bg="white")
textentry.grid(row = 0,column = 5, sticky = W)  


#### run the main loop
window.mainloop()

