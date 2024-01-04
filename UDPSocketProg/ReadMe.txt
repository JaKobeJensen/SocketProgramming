************************************Server*****************************************
In the Server folder, run the UDPServer.py script first before transfering data from
the client.
When the server starts up it will wait until it recieved a request from the client.
After a client sends a request to the server, the server will send back a request 
accept code back to the client, letting them know the server is not busy and it is
ready for the data to be transfered to it.
The server will wait for the client wait to send data and write that data to a file.
After the data was successfully transfered the server will let the client know the
transfer was successful.
Files transfered from the client will be saved in the SavedFiles.

***********************************Client*******************************************
In the Client folder, run the UDPClient.py script to start transfering files to the
server. 
The server must be running before files can be transfered, or an error will be thrown
saying the server did not respond.
When prompt with "Input file name and directory (EXAMPLE: C:\desktop\file.txt)", 
enter the name of the file. If the file is not in the same directory as the 
UDPClient.py script, make sure to add the path of file also like in ht example.
After entering the file name, the client will start sending the data in blocks of
whatever the BUFFER_SIZE constent is set to.
After all the blocks of data are sent, the client will let the server know that was 
all of the data and then the client will wait for a response from ther server to see 
if the data tranfered successfully.