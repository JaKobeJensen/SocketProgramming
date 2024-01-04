**************************************Server*****************************************
In the Server folder you can run the TCPServer.py script. This will start the server 
and ait for clients to join the server.
The server ip address and port number can be changed at the top of the python script 
by changing the constants SERVER_IP and SERVER_PORT.
After the first client joins the server, the server will start a 30 second countdown 
until the quiz game starts. During this time other clients can join the server and
wait for the quiz game to start.
After the quiz starts, the server will send a question packet to all clients 
connected.
Then the server will wait until the clients send their answers. If a client does not
send an answer, they get zero points for the question. If they answer it right the 
server will give that client points.
After the question is finished, the server will send the clients a leaderboard packet
to show who is in the top 10.
Then the server will repeat this until all questions are sent, after the server will
disconnect the clients and close their sockets and then will wait for new clients to
join and repeat the quiz game.

**************************************Client*****************************************
In the Client folder you can run the TCPClient.py. This will prompt you to enter your
name and then enter the address to the server.
If you entered a address that has a server waiting for clients, the client will 
connect to the server and wait until the quiz game starts.
After it recieves a question packet from the server, it will print the question to 
the terminal and ask the user for an answer.
After the user inputs an answer the client will send the answer to the server.
Then the client waits until the time limit is done and prints out the leader the
server sent to it.
This will continue until the quiz game is over. Then the client will be disconnected
from the server.

*************************************TxtToBin****************************************
I made a python script that take in a txt file full of questions, formatted in a certain way, and converts it to a bin file. This is how the server reads in the 
questions.

