import os
from packet_types import *
import pickle
os.system("cls")

"""
This python script is used to convert question .txt files to .bin files.

QUESTION FORMAT:
    Questions should be formatted like so:
        Question
        Option 1
        Option 2
        Option 3
        Option 4
        Answer (Should be either A, B, C, D; upper case matters)
    There should be a empty line between questions.
    At the end of the last question there should be a "*" character indicating the end of the file. 
    Look at the Quizzes folder and look at the ExampleQuestionFormat.txt file for an example how the .txt file should be formatted.
"""

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

class Question:
    def __init__(self):
        self.question:str = None
        self.answer:str = None
        self.hint:str = None
        self.options:list[str] = []

def get_path(fileExtention:str)->str:
    while True:
        print("Enter Question .{0} File Path (EXAMPLE: Quizzes\\quiz.{0})".format(fileExtention))
        path = input(">")
        os.system("cls")
        if os.path.exists(path):
            return path
        print("Question .{0} File Does Not Exists: {1}\n".format(fileExtention, path))
        
def convert_txt_to_bin()->None:
    path = get_path("txt")
    file = open(path, "r")
    questions:list[Question] = []
    while True:
        question = Question()
        question.question = file.readline()[:-1]
        for _ in range(4):
            question.options.append(file.readline()[:-1])
        question.answer = file.readline()[:-1]
        #question.hint(file.readline())
        questions.append(question)        
        if file.readline() == "*":
            break
    file.close()
    
    savePath = path.split(".")[0] + ".bin"
    file = open(savePath, "wb")
    for question in questions:
        pickle.dump(question, file, pickle.HIGHEST_PROTOCOL)
    file.close()
    
    return

def load_question_bin()->list[Question]:
    questions:list[Question] = []
    #path = get_path("bin")
    path = "Quizzes\\GeneralKnowledge.bin"
    file = open(path, "rb")
    
    try:
        while True:
            questions.append(pickle.load(file))
    except EOFError:
        file.close()
        return questions

def main()->None:
    #convert_txt_to_bin()
    
    questions = load_question_bin()
    for question in questions:
        print_question(question)
    '''
    for question in questions:
        print(question.question, "\n",
              question.answer, "\n",
              question.options[0], "\n",
              question.options[1], "\n",
              question.options[2], "\n",
              question.options[3], "\n",)
    '''
    return

if __name__ == "__main__":    
    main()
    quit()
    
    