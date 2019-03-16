Blaine McMahon, Jacob Sword, Nicholas Yameen

1) The files submitted are the following:
		GUI.py		- The GUI for client and server
		UDPclient.py	- Script to run a client (triggered from GUI)
		UDPserver.py	- Script tp run a server (triggered from GUI)
		rdt_receiver.py	- Holds all the RDT 2.2 Receiver functions used by client and server
		rdt_sender.py	- Holds all the RDT 2.2 Sender functions used by client and server
		NEED DEFAULT	- default image being sent
		sever.png	- used by the GUI

For Phase 3, we used Python as our programming language. The code was ran on Python version 3.6 on Mac and Windows.
The GUI require pillow, if not installed preform a "pip install pillow".  It also uses tkinter,
but this should be included in all recent installations of python.

2) To run the the program, first make sure any picture you'd like to use (should be JPEG format) is in the directory with the above files. 
Then run the python script called GUI.py by issuing the command "python GUI.py" (or python3 GUI.py depending on installation)
When the GUI opens, enter the name of the image you would like to use, or leave blank to use the default NEED NEW DEFAULT, noted above. 
Once you have typed in the file name, click "server" button, this will start the server.  The server will use the above typed filename (or default)
for its "response" file: the file it will send back to the client.

Next, you can change the file for the client or leave blank for the default (DEFAULT again). 
Click the "client" button and the client will start. 
In the terminal, messages will appear with the name of the thread Server or Client, followed by status updates.
When the script is finished, the client will end and the server will continue to listen, click client to run again
or exit the GUI to finish.

You should be able to see new files in the current directory denoted the successful transmission of files.
Files received by the client will be entitled "client_recv_{{whatever filename was received}}".
Files received by the server will be entitled "server_recv_{{whatever filename was received}}"

3) The different scenarios in this project can be seen by doing the following:
	A. No loss/err: put a 0 in the if statment on line 132 in rdt_sender.py and put a 0 in the if statment on line 118 in rdt_receiver.py
	B. ACK Bit err: in rdt_sender.py put 5, 10, ..., 60 on line 132 in the rdt_rcv() function keep 0 on 118 in rdt_receiver.py
	C. Data Loss err: in rdt_receiver.py put 5, 10, ..., 60 on line 118 in the rdt_rcv() function keep 0 on 132 in rdt_sender.py