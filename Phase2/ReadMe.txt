Blaine McMahon, Jacob Sword, Nicholas Yameen

1) The files submitted are the following:
		GUI.py		- The GUI for client and server
		UDPclient.py	- Script to run a client
		UDPserver.py	- Script tp run a server
		rdt.py		- Holds all the RDT 1.0 functions
		spongebob.bmp	- default image being sent
		sever.png	- used by the GUI

For Phase 2, we used Python as our programming language. The code was ran on Python version 3.6 on Mac and Windows.
The GUI require pillow, if not installed preform a "pip install pillow".

2) To run the the program, first run the python script called GUI.py by issuing the command "python GUI.py". 
Make sure different picture(s) not specified in the ReadMe that is being sent are in the same directory. 
When the GUI opens, enter the name of the image, or leave blank to use the default spongebob.bmp. 
Once you have typed in the file name, click "server" button, this will start the server.

Next, you can change the file for the client or leave blank for the default. Click the "client" button and the 
client will start. In the terminal, messages will appear with the name of the thread Server or Client.
When the script is finished, the client will end and the server will continue to listen, click client to run again
or exit the GUI to finish.