from socket import *
import os
import pickle
from packet_types import *
from time import sleep, time
os.system("cls")

SERVER_IP = '127.0.0.1'
SERVER_PORT = 11000
BUFFER_SIZE = 1024
MAX_PLAYER_NAME_LENGTH = 10
MAX_PLAYERS_DISPLAYED = 10

class GameInfo:
    def __init__(self):
        self.score:int = 0
        self.playerName:str = ""
        self.time = 0
        self.serverAddress:tuple[str,int] = ("0.0.0.0", 0)
        self.numPlayers:int = 0    
        self.start:bool = False
        self.numberOfQuestions:int = 0
        self.currentQuestion:int = 0

def send_packet(clientSocket:socket, packet:object)->None:
    clientSocket.send(pickle.dumps(packet))

def get_packet(clientSocket:socket)->object:
    try:
        return pickle.loads(clientSocket.recv(BUFFER_SIZE))
    except ConnectionResetError:
        return None

def print_header(gameInfo:GameInfo)->None:
    MAX_PLAYER_NAME_LENGTH = 10
    
    os.system("cls")
    scoreTxt = "Score: {0}".format(gameInfo.score)
    connectTxt = "Connected: {0}:{1}".format(gameInfo.serverAddress[0], gameInfo.serverAddress[1])
    titleTxt = "Super Quiz Game".center(os.get_terminal_size()[0] - len(scoreTxt) - len(connectTxt))

    timeTxt = "Time Left: {0} seconds".format(gameInfo.time)
    numPlayersTxt = "Players Connected: {0}".format(gameInfo.numPlayers).rjust(os.get_terminal_size()[0] - len(timeTxt))

    if len(gameInfo.playerName) > MAX_PLAYER_NAME_LENGTH:
        nameTxt = "Name: {0}".format(gameInfo.playerName[:10])
    else:
        nameTxt = "Name: {0}".format(gameInfo.playerName)
    questionNumTxt = "Question {0}/{1}".format(gameInfo.currentQuestion, gameInfo.numberOfQuestions).rjust(os.get_terminal_size()[0] - len(nameTxt))

    print(scoreTxt + titleTxt + connectTxt)
    print(timeTxt + numPlayersTxt)
    print(nameTxt + questionNumTxt)
    print("\n")
    
    return

def print_question(question:QuestionPacket)->None:
    SCREEN_PERCENTAGE = 0.75
    MAX_QUESTION_LENGTH = int(os.get_terminal_size()[0] * SCREEN_PERCENTAGE)
    MAX_ANSWER_LENGTH = int((MAX_QUESTION_LENGTH / 2) * SCREEN_PERCENTAGE)
    MAX_ANSWER_AREA_HEIGHT = 5
    PADDING = " " * int((os.get_terminal_size()[0] - MAX_QUESTION_LENGTH) / 2)
    PADDING_ANSWER = " " * int((MAX_QUESTION_LENGTH/2 - MAX_ANSWER_LENGTH) / 2)

    questionTxt = [question.question]
    while len(questionTxt[-1]) > MAX_QUESTION_LENGTH:
        firstPart = questionTxt[-1][:MAX_QUESTION_LENGTH]
        lastPart = questionTxt[-1][MAX_QUESTION_LENGTH:]
        questionTxt.remove(-1)
        questionTxt.append(firstPart)
        questionTxt.append(lastPart)
    for partOfQuestionTxt in questionTxt:
        print(partOfQuestionTxt.center(os.get_terminal_size()[0]))
    print("\n")

    verticalBorderTxt = "|".center(MAX_QUESTION_LENGTH)
    horizontalBorderTxt = "|".center(MAX_QUESTION_LENGTH,"-")
    topAnswerTxt = "A.)" + "|".rjust(round(MAX_QUESTION_LENGTH/2)-3) + "B.)"
    bottomAnswerTxt = "C.)" + "|".rjust(round(MAX_QUESTION_LENGTH/2)-3) + "D.)"

    print(PADDING + topAnswerTxt)
    for i in range(1, MAX_ANSWER_AREA_HEIGHT):
        if i == round(MAX_ANSWER_AREA_HEIGHT/2):
            print(PADDING + PADDING_ANSWER + question.options[0].center(MAX_ANSWER_LENGTH) + PADDING_ANSWER + "|" + PADDING_ANSWER + question.options[1].center(MAX_ANSWER_LENGTH))
        else:
            print(PADDING + verticalBorderTxt)
    print(PADDING + horizontalBorderTxt)
    print(PADDING + bottomAnswerTxt)
    for i in range(1, MAX_ANSWER_AREA_HEIGHT):
        if i == round(MAX_ANSWER_AREA_HEIGHT/2):
            print(PADDING + PADDING_ANSWER + question.options[2].center(MAX_ANSWER_LENGTH) + PADDING_ANSWER + "|" + PADDING_ANSWER + question.options[3].center(MAX_ANSWER_LENGTH))
        else:
            print(PADDING + verticalBorderTxt)
    return

def print_leaderboard(leaderboard:LeaderboardPacket)->None:
    PADDING = 25
    PADDING_TEXT = " " * PADDING

    leaderboardTitleTxt = "Leaderboard".center(os.get_terminal_size()[0])
    print(leaderboardTitleTxt)

    topBorder = " " + ("_" * (os.get_terminal_size()[0] - PADDING*2 - 2)) + " "
    print(PADDING_TEXT + topBorder + PADDING_TEXT)

    emptyLineTxt = "|" + "|".rjust(os.get_terminal_size()[0] - PADDING*2 - 1)
    for idx, player in enumerate(leaderboard.players):
        if idx + 1 == MAX_PLAYERS_DISPLAYED:
            break

        print(PADDING_TEXT + emptyLineTxt + PADDING_TEXT)

        if len(player[0]) > MAX_PLAYER_NAME_LENGTH:
            playerName = player[0][:10]
        else:
            playerName = player[0]
        playerScore = str(player[1])

        playerScoreTxtRight = "|    {0}.)".format(idx+1)
        playerScoreTxtCenter = playerName.center(int((os.get_terminal_size()[0] - PADDING*2 - len(playerScoreTxtRight) - 1) / 2)) + \
                               playerScore.center(int((os.get_terminal_size()[0] - PADDING*2 - len(playerScoreTxtRight)) / 2))
        playerScoreTxtLeft = "|"

        print(PADDING_TEXT + playerScoreTxtRight + playerScoreTxtCenter + playerScoreTxtLeft + PADDING_TEXT)

    print(PADDING_TEXT + emptyLineTxt + PADDING_TEXT)

    bottomBorder = "|" + ("_" * (os.get_terminal_size()[0] - PADDING*2 - 2)) + "|"
    print(PADDING_TEXT + bottomBorder + PADDING_TEXT)

    return

def connect_to_server_screen()->tuple[str, int]:
    print("Server To Connect To (EXAMPLE: IPAdress:PortNumber -> 127.0.0.1:12000)")
    serverAddress = input(">")
    serverAddress = serverAddress.split(":")
    
    serverIPCheck = serverAddress[0].split(".")
    if len(serverIPCheck) != 4:
        return("0.0.0.0", 0)
    elif len(serverAddress) < 2:
        return (serverAddress[0], 0)
    else:
        return (serverAddress[0], int(serverAddress[1]))

def connect_to_server(clientSocket:socket, gameInfo:GameInfo)->tuple[str,int]:
    print_header(gameInfo)
    while True:
        try:
            serverAddress = connect_to_server_screen()
            gameInfo.serverAddress = serverAddress
            print("\nConnecting To {0}:{1} Server...".format(serverAddress[0], serverAddress[1]))
            clientSocket.connect(serverAddress)
            print_header(gameInfo)
            print("Waiting For Game To Start...\n")
            break
        except ConnectionRefusedError:
            print_header(gameInfo)
            print("Couldn't Connect To {0}:{1} Server\n".format(serverAddress[0], serverAddress[1]))
        except OSError:
            print_header(gameInfo)
            print("Invalid IP Address Format\n")
    return serverAddress

def get_player_name(gameInfo:GameInfo)->str:
    print_header(gameInfo)
    print("Enter Name")
    playerName = input(">")
    gameInfo.playerName = playerName
    return playerName

def get_score(leaderboard:LeaderboardPacket, gameInfo:GameInfo)->None:
    for player in leaderboard.players:
        if player[0] == gameInfo.playerName:
            gameInfo.score = player[1]
            return
    return

def start_question(question:QuestionPacket, clientSocket:socket, gameInfo:GameInfo)->int:
    VALID_ANSWERS = ["A", "B", "C", "D"]
    
    gameInfo.time = question.time
    gameInfo.numberOfQuestions = question.numberOfQuestions
    gameInfo.currentQuestion = question.questionNumber

    startTime = time()
    
    answer = ""
    print_header(gameInfo)
    print_question(question)
    while True:
        answer = input(">").upper()
        if time() - startTime >= gameInfo.time:
            break
        elif answer in VALID_ANSWERS:
            packet = AnswerPacket()
            packet.answer = answer
            send_packet(clientSocket, packet)
            break
        else:
            print_header(gameInfo)
            print("Invalid Answer\n")
            print_question(question)

    print_header(gameInfo)
    print("Waiting For Players To Answer...")
    return 0

def quiz_game(clientSocket:socket, gameInfo:GameInfo)->int:
    packet = ConnectPacket()
    while type(packet) != DisconnectPacket:
        packet = get_packet(clientSocket)   
        if type(packet) == LeaderboardPacket:
            get_score(packet, gameInfo)
            gameInfo.numPlayers = len(packet.players)
            print_header(gameInfo)
            if gameInfo.start != True:
                print("Waiting For Game To Start...\n")
            print_leaderboard(packet)
        elif type(packet) == QuestionPacket:
            gameInfo.start = True
            if start_question(packet, clientSocket, gameInfo) == 1:
                return 1
        elif type(packet) == DisconnectPacket:
            continue
        else:
            return 1
    return 0 

def main()->int:
    # gameInfo will keep track of game variables
    gameInfo = GameInfo()
    # create the TCP socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    # get player name
    get_player_name(gameInfo)
    # connect to the server
    connect_to_server(clientSocket, gameInfo)
    # send name to server
    packet = NamePacket()
    packet.name = gameInfo.playerName
    send_packet(clientSocket, packet)

    # start to quiz game
    if quiz_game(clientSocket, gameInfo) == 1:
        print_header(gameInfo)
        print("Disconnected From {0}.{1}".format(gameInfo.serverAddress[0], gameInfo.serverAddress[1]))
        clientSocket.close()
        sleep(2)
        return 1
    
    print_header(gameInfo)
    print("Disconnected From {0}.{1}".format(gameInfo.serverAddress[0], gameInfo.serverAddress[1]))
    clientSocket.close()
    sleep(2)
    return 0

if __name__ == '__main__':
    try:
        while True:
            code = main()
    except KeyboardInterrupt:    
        os.system("cls")
        quit()
