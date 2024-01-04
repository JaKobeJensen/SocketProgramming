from socket import *
import os
import pickle
from packet_types import *
from time import sleep, time
import random
os.system("cls")
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000
SERVER_TIMEOUT = 0.1
BUFFER_SIZE = 1024
QUIZ_GAME_PATH = "Quizzes\\GeneralKnowledge.bin"
CLIENT_CONNECTION_TIMER = 30
QUESTION_TIME_LIMIT = 15
ANSWER_MULTIPLER = 2
CORRECT_ANSWER_SCORE = 100
BETWEEN_QUESTION_TIME = 5

class Client:
    def __init__(self):
        self.clientSocket:socket = None
        self.clientIP:str = None
        self.clientPort:int = None
        self.score:int = 0
        self.correctlyAnswered:int = 0
        self.name:str = None

class Leaderboard:
    def __init__(self):
        self.players:list[Client] = []
    def sort(self, ascending=False)->None:
        if len(self.players) <= 1:
            return
        for i in range(len(self.players)-1):
            for j in range(i, len(self.players)-1):
                if self.players[j].score < self.players[j+1].score and not ascending:
                    temp = self.players[j]
                    self.players[j] = self.players[j+1]
                    self.players[j+1] = temp
                elif self.players[j].score > self.players[j+1].score and ascending:
                    temp = self.players[j]
                    self.players[j] = self.players[j+1]
                    self.players[j+1] = temp 
        return             

class Question:
    def __init__(self):
        self.question:str = None
        self.answer:str = None
        self.hint:str = None
        self.options:list[str] = []

# waits for a packet and returns it
def get_packet(clients:list[Client])->tuple[object,tuple[str,int]]:
    for client in clients:
        try:
            return get_packet_from(client.clientSocket)
        except TimeoutError:
            continue
        except EOFError:
            continue
    return (None, (None, None))

def get_packet_from(clientSocket:socket)->tuple[object,tuple[str,int]]:
    data = clientSocket.recv(BUFFER_SIZE)
    packet = pickle.loads(data)
    return packet, clientSocket.getpeername()

# send a packet to all clients
def send_packet(clients:list[Client], packet:object)->None:
    for client in clients:
        client.clientSocket.send(pickle.dumps(packet))
    return

# makes a LeaderboardPacket and fills in the packet with the leaderboard and sends it to all clients
def send_leaderboard(clients:list[Client], leaderboard:Leaderboard)->None:
    leaderboardPacket = LeaderboardPacket()
    leaderboard.sort()
    for player in leaderboard.players:
        leaderboardPacket.players.append((player.name, player.score))
    send_packet(clients, leaderboardPacket)
    return

# makes a QuestionPacket and fills in the packet the question, time, numQuestion and questionNumber
def send_question(client:list[Client], question:Question, time:int, numQuestions:int, questionNumber:int)->None:
    questionPacket = QuestionPacket()
    questionPacket.question = question.question
    questionPacket.options = question.options.copy()
    questionPacket.answer = question.answer
    questionPacket.time = time
    questionPacket.numberOfQuestions = numQuestions
    questionPacket.questionNumber = questionNumber
    send_packet(client, questionPacket)
    return

# randomizes the questions
def randomize_questions(questions:list[Question])->list[Question]:
    randomList = random.sample(range(0, len(questions)), len(questions))
    randomizedQuestions:list[Question] = []
    for idx in randomList:
        randomizedQuestions.append(questions[idx])
    return randomizedQuestions

# loads in the question from a given file path
# questions are .bin files; look at the TxtToBin.py to see how to make questions .bin files
def load_questions(filePath:str=QUIZ_GAME_PATH)->list[QuestionPacket]:
    questions:list[QuestionPacket] = []   
    file = open(filePath, "rb")
    try:
        while True:
            questions.append(pickle.load(file))
    except EOFError:
        file.close()
        return randomize_questions(questions)

# makes a new Client() class and fills in networking information
def make_new_client(clientSocket:socket, clientAddress:tuple[str, int])->Client:
    newClient = Client()
    newClient.clientIP = clientAddress[0]
    newClient.clientPort = clientAddress[1]
    newClient.clientSocket = clientSocket
    newClient.clientSocket.settimeout(SERVER_TIMEOUT)
    return newClient

# listens for a new connection and adds them to the clients list and the leaderboard
# waits to see if a NamePacket gets sent fromm the client to change the clients name, if timesout gives random name to client
def new_connection(serverSocket:socket, clients:list[Client], leaderboard:Leaderboard)->None:
    clientSocket, clientAddress = serverSocket.accept()
    newClient = make_new_client(clientSocket, clientAddress)
    try:
        packet, _ = get_packet_from(newClient.clientSocket)
    except TimeoutError:
        packet = None
    if type(packet) == NamePacket:
        newClient.name = packet.name
    else:
        num = random.randint(0, 1000)
        newClient.name = "User{:04d}".format(num)
    clients.append(newClient)
    leaderboard.players.append(newClient)
    send_leaderboard(clients, leaderboard)
    return
    
# connects clients to the server until a time limit then stops accepting connections from clients
# populates the clients list and leaderboard
def connect_clients(serverSocket:socket)->tuple[list[Client],Leaderboard]:
    clients:list[Client] = []
    leaderboard = Leaderboard()
    
    # make the server listen on the port
    serverSocket.listen()
    # changing the timeout
    serverSocket.settimeout(SERVER_TIMEOUT)
    
    startTime = time()
    firstConnection = True
    # let clients connect until the timer expires
    while time() - startTime < CLIENT_CONNECTION_TIMER:
        os.system("cls")
        print("Waiting For Clients...\n{0} Clients Connected".format(len(clients)))
        try:
            new_connection(serverSocket, clients, leaderboard)
            if firstConnection:
                firstConnection = False
                startTime = time()
        except TimeoutError:
            if firstConnection:
                startTime = time()
    # stop the server from accepting anymore connection
    serverSocket.listen(0)
    
    os.system("cls")
    print("Waiting For Clients...\n{0} Clients Connected\n".format(len(clients)))
    
    return clients, leaderboard

def disconnect_clients(clients:list[Client])->None:
    send_packet(clients, DisconnectPacket())
    for client in clients:
        client.clientSocket.close()

def check_answer(answer:str, clientAnswer:str, clientAddress:tuple[str,int], clients:list[Client], remainingTime:float)->None:
    if remainingTime < 0:
        remainingTime = 0
    for client in clients:
        if client.clientIP == clientAddress[0] and client.clientPort == clientAddress[1] and clientAnswer == answer:
            multipler = (remainingTime / QUESTION_TIME_LIMIT) * ANSWER_MULTIPLER
            client.score += round(CORRECT_ANSWER_SCORE * multipler)
            return
    return

def start_quiz(clients:list[Client], leaderboard:Leaderboard, questions:list[Question])->None:
    print("Starting Quiz Game")
    for idx, question in enumerate(questions):
        send_question(clients, question, QUESTION_TIME_LIMIT, len(questions), idx+1)
        print("Question {0} Sent".format(idx+1))
        startTime = time()
        while time() - startTime < QUESTION_TIME_LIMIT + 1:
            packet, clientAddress = get_packet(clients)
            if type(packet) != AnswerPacket:
                continue
            check_answer(question.answer, packet.answer, clientAddress, clients, QUESTION_TIME_LIMIT - (time() - startTime))
        print("Question {0} Done".format(idx+1))
        send_leaderboard(clients, leaderboard)
        sleep(BETWEEN_QUESTION_TIME)
    return

def main()->None:
    # create the TCP socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # bind the port number to the socket
    serverSocket.bind((SERVER_IP, SERVER_PORT))
    
    try:
        while True:
            # load in the questions
            questions:list[Question] = load_questions()  
            
            # let the clients connect to the server
            clients, leaderboard = connect_clients(serverSocket)

            # start the quiz game
            start_quiz(clients, leaderboard, questions)

            # disconnect all the clients from the server and close their sockets
            disconnect_clients(clients)
    except KeyboardInterrupt:
        # close server socket
        serverSocket.close()
        return

if __name__ == '__main__':
    main()
    quit()

