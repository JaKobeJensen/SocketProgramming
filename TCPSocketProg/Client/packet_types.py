class LeaderboardPacket:
    def __init__(self):
        self.players:list[tuple[str, int]] = []

class QuestionPacket:
    def __init__(self):
        self.question:str = None
        self.answer:str = None
        self.hint:str = None
        self.options:list[str] = []
        self.time:int = 0
        self.numberOfQuestions:int = 0
        self.questionNumber:int = 0
        
class DisconnectPacket:
    def __init__(self):
        self.disconnect:bool = True
        
class ConnectPacket:
    def __init__(self):
        self.connect:bool = True
        
class ScorePacket:
    def __init__(self):
        self.score:int = 0
        
class NumOfPlayerPacket:
    def __init__(self):
        self.NumOfPlayer:int = 0 
        
class TimeoutPacket:
    def __init__(self):
        self.timeout:bool = True 

class AnswerPacket:
    def __init__(self):
        self.answer:str = ""

class NamePacket:
    def __init__(self):
        self.name:str = ""