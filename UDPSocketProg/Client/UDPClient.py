from socket import *
import os
from time import sleep
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12000
BUFFER_SIZE = 1024
os.system("cls")

# creates the progress bar and prints it to the terminal
def progress_bar(fileSize:int, iteration:int)->None:
    PROGRESS_BAR_LENGTH = 40
    percentageJump = 100.0 / (fileSize / BUFFER_SIZE)
    if percentageJump > 100.0:
        percentageJump = 100.0

    progressBar = "Sending File: [" + \
                  "#" * int(round((PROGRESS_BAR_LENGTH / 100) * (percentageJump * iteration))) + \
                  " " * int(round((PROGRESS_BAR_LENGTH / 100) * (percentageJump * (100 / percentageJump - iteration)))) + \
                  "]"
    os.system("cls")
    print(progressBar)
    return

# getting the file name and directory from the user and checking to see if the file exists 
def get_file_name()->str:
    while True: 
        fileDirectory = input("Input file name and directory (EXAMPLE: C:\\desktop\\file.txt)\n>")
        os.system("cls")
        if os.path.exists(fileDirectory):
            break
        else:
            print("{0} does not exist".format(fileDirectory))
    return fileDirectory        

# waits for a server response; returns a code from the server
def server_response(clientSocket:socket)->str:
    code, address = clientSocket.recvfrom(BUFFER_SIZE)
    while not SERVER_IP == address[0] or not SERVER_PORT == address[1]:
        code, address = clientSocket.recvfrom(BUFFER_SIZE)
    return code.decode()

# sends the server a request for unloading the data
def send_request(clientSocket:socket, request:bytes)->None:
    print("Sending requests to {0} server...".format(SERVER_IP))

    request_counter = 0
    code = ""
    # keep sending request until the server responds with an accept
    while code != "202":
        # have the file sent over to the client socket
        clientSocket.sendto(request, (SERVER_IP, SERVER_PORT))

        # wait for the server to respond
        code = server_response(clientSocket)
        
        # check to see if the server is too busy
        request_counter += 1
        if request_counter >= 10:
            raise Exception

    os.system("cls")
    return

def send_data(clientSocket:socket, fileDirectory:str)->None:
    # opening up the file using the fileDirectory
    file = open(fileDirectory, "rb")
    # getting the size of the file so we can tell how many times the client has to send file data to the server
    # used for the progress bar
    fileSize = os.path.getsize(fileDirectory)

    # reading in a BUFFER_SIZE of data from the file
    data = file.read(BUFFER_SIZE)
    iteration = 0
    # loop until there is no more data to be sent
    while data:
        # prints the progress bar to the terminal
        progress_bar(fileSize, iteration)
        # sending the BUFFER_SIZE of data to the server
        clientSocket.sendto(data, (SERVER_IP, SERVER_PORT))
        # reading in another BUFFER_SIZE of data from the file
        data = file.read(BUFFER_SIZE)
        # sleep for a little to give the server a chance to save the data
        sleep(0.01)
        iteration += 1
    
    progress_bar(fileSize, iteration)

    # close the file
    file.close()

    # send the server a code let it know data is done being transfered
    clientSocket.sendto("200".encode(), (SERVER_IP, SERVER_PORT))

    # wait for the server to respond, letting the client know if the file unloaded successfully or not
    code = server_response(clientSocket)
    if code == "200":
        print("Upload was successful to {} server".format(SERVER_IP))
        return
    else:
        raise Exception

# error handling for different types of errors that can happen when transfering the data
def error_message(errorCode:int, *argv)->None:
    os.system("cls")
    if errorCode == "1":
        # the server never responded back to the client
        print("{0} server did not respond".format(argv[0]))
    elif errorCode == "2":
        # the server is busy with another client
        print("{0} server is too busy, try again later".format(argv[0]))
    elif errorCode == "3":
        # the file failed tranfer properly to the server
        print("Failed to upload to {0} server: {1}".format(argv[0], argv[1]))
    else:
        # common error
        print("Error")
    quit()

def main():
    # create the UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)

    # getting the file name and directory from the user and checking to see if the file exists
    fileDirectory = get_file_name()

    # going to try to send request to the server, if the server does not respond it throws an error
    try:
        send_request(clientSocket, fileDirectory.encode())
    except TimeoutError:
        error_message(1, SERVER_IP)
    except:
        error_message(2, SERVER_IP)

    # going to try to send the file data to the server, it will throw an error if the server timesout
    try:
        send_data(clientSocket, fileDirectory)
    except TimeoutError:
        error_message(1, SERVER_IP)
    except:
        error_message(3, SERVER_IP, fileDirectory)
    
    # close the client socket and leave main
    clientSocket.close()
    return

if __name__ == '__main__':
    main()
    quit()