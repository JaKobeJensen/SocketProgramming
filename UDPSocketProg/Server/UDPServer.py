from socket import *
import os
os.system("cls")
SREVER_IP = '127.0.0.1'
SERVER_PORT = 12000
BUFFER_SIZE = 1024

# getting a new data packet from an existing address
# checks to see if the new sender is the same as the initial client
# sends a 400 code to the new sender if their not the initial client to let them knew the server is bust and try again later
def new_packet(serverSocket:socket, initialAddress:tuple)->bytes:
    data, newAddress = serverSocket.recvfrom(BUFFER_SIZE)
    while not initialAddress[0] == newAddress[0] or not initialAddress[1] == newAddress[1]:
        serverSocket.sendto("400".encode(), newAddress)
        data, newAddress = serverSocket.recvfrom(BUFFER_SIZE)
    return data

# making a unique file name using the hash function
def hash_file_name(fileName:str)->str:
    fileNameHash = str(hash(fileName.split(".")[0]))
    fileExtension = fileName.split(".")[1]
    newFileName = "SavedFiles\\{0}.{1}".format(fileNameHash, fileExtension)
    return newFileName

def main()->None:
    # create the UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    # bind the port number to the socket
    serverSocket.bind((SREVER_IP, SERVER_PORT))
    # setting the timeout for the serverSocket
    serverSocket.settimeout(1)

    try:
        print("Waiting for new request...")
        # loop forever because it is a server
        while True:
            try:
                # waiting for a client to send a request
                data, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
            except TimeoutError:
                continue
            
            # letting the client know that its requested was accepted
            serverSocket.sendto("202".encode(), clientAddress)

            # Getting the file name from the data
            fileName = data.decode()
            # hashing the file name for a unique name
            hashedFileName = hash_file_name(fileName)
            # creating and opening the new file with a hashed name
            file = open(hashedFileName, "wb")

            print("Recieving file from {1}: {0}".format(fileName, clientAddress[0]))

            try:
                # gets the next data packet from the client address
                data = new_packet(serverSocket, clientAddress)
                # loop until the file is finished transfering
                while(data.decode() != "200"):
                    # write to the new file
                    file.write(data)
                    # gets the next data packet from the client address 
                    data = new_packet(serverSocket, clientAddress)
                
                # letting the client know the download was successful
                serverSocket.sendto("200".encode(), clientAddress)

                # close the new file
                file.close()

                print("Finished download from {1}: {0}\n".format(fileName, clientAddress[0]))
            except TimeoutError:
                # let the client know the file download was unseccussful and they timedout
                serverSocket.sendto("408".encode(), clientAddress)

                # close the file and remove it from the SavedFiles folder
                file.close()
                os.remove(hashedFileName)

                print("Download failed from {1}: {0}\n".format(fileName, clientAddress[0]))

            print("Waiting for new request...")

    # if the server gets shutdown or interupted close the socket
    except:
        serverSocket.close()
        print("\nServer Shutdown")
        return

if __name__ == '__main__':
    main()
    quit()