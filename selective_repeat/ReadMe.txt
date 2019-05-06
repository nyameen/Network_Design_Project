Blaine McMahon, Jacob Sword, Nicholas Yameen

1) The files submitted are the following:
		GUI.py		- The GUI for client and server
		UDPclient.py	- Script to run a client (triggered from GUI)
		UDPserver.py	- Script tp run a server (triggered from GUI)
		rdt_receiver.py	- Holds all the RDT 2.2 Receiver functions used by client and server
		rdt_sender.py	- Holds all the RDT 2.2 Sender functions used by client and server
		config.py	- Holds GUI configuration
		rdt_utils.py - General functions used by both rdt_receiver.py and rdt_sender.py
		spongebob.jpg	- default image being sent
		sever.png	- used by the GUI for display

This code implements the SELECTIVE REPEAT addition of Phase 6.

For Phase 6, we used Python as our programming language. The code was run on Python version 3.6 on Mac and Windows.
The GUI requires pillow, if not installed preform a "pip install pillow".  It also uses tkinter,
but this should be included in all recent installations of python.

2) To run the the program, first make sure any picture you'd like to use (should be JPEG format) is in the directory with the above files. A default jpg "spongebob.jpg" is included.
Then run the python script called GUI.py by issuing the command "python GUI.py" (or python3 GUI.py depending on installation)
When the GUI opens, enter the name of the image you would like to use, or leave blank to use the default noted above. 
Once you have typed in the file name, click "server" button, this will start the server.  The server will use the above typed filename (or default)
for its "response" file: the file it will send back to the client.

Next, you can change the file for the client or leave blank for the default noted above. 
Also, you can specify the corruption option to use (1-5, corresponding to the descriptions shown in part 3 below) or leave as default which is 1
The box below this allows for entry the error rate, but will only be applied if the corruption option allows for it (i.e. is not 1).
(Note: if this box is left empty, error rate is defaulted to 0%)
Below this window is the Window Size box which allows users to select the window size that will be used by both sender and receiver in the selective repeat protocol.

Additionally, the Status Msgs checkbox can be checked to allow for server and client to print status messages during transfer,
and UDT Err Msgs checkbox can be checked to allow for rdt functions to output bit err/data loss and timeout error messages.

Then click the "client" button and the client will start. 
(Each time the client button is clicked, newly input corruption option and error rate settings will be applied)
(Note these settings apply for both client and server as they both send and receive an image)
In the terminal, messages will appear with the name of the thread Server or Client, followed by status updates.
When the script is finished, the client will end and the server will continue to listen, click client to run again
or exit the GUI to finish. After clicking close on the GUI, you may need to hit control^c in the terminal that the process was launched from as well.

You should be able to see new files in the current directory denoted the successful transmission of files.
File received by the client will be entitled "client_recv.jgp".
File received by the server will be entitled "server_recv.jpg"

3) The different scenarios in this project can be seen by doing the following:
	A. No loss/err: use 1 for the input Corruption Option or leave it empty
	B. ACK Bit err: use 2 for the input Corruption Option - input percent error in the field below
	C. Data Bit err: use 3 for the input Corruption Option - input percent error in the field below
	D. ACK Packet Loss err: use 4 for the input Corruption Option - input percent error in the field below
	D. ACK Data Loss err: use 5 for the input Corruption Option - input percent error in the field below

4) This version utilizes Selective Repeat to send and receive messages between host and client. This protocol allows for greater efficieny by allowing for mutiple frames being set at a time, and a timer is created for each sent packet.  

Default values for this process are:
	- The window size is set to 10 
	- Timeout is 50ms 
	- Max buffer size is 65,435 packets

These, and other defaults can be seen in config.py

