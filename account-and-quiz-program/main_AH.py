import turtle
import csv
import random
import time

import Quiz_AH
import account_manager_AH

#initalse progresstion variables 
login = False
quiz = False
leaderboard = False

#Setting up Password UI
account_manager_AH.screen = turtle.Screen()
account_manager_AH.screen.setup(width=800, height=600)
account_manager_AH.screen.bgcolor("AntiqueWhite1")
account_manager_AH.screen.title("Password Manager")

#initlsie drawing UI variables
account_manager_AH.pen = account_manager_AH.turtle.Turtle()
account_manager_AH.pen.hideturtle()
account_manager_AH.pen.penup()

account_manager_AH.pen_NC = account_manager_AH.turtle.Turtle()
account_manager_AH.pen_NC.hideturtle()
account_manager_AH.pen_NC.penup()

input_manager = account_manager_AH.GetInputs()


# Draw UI and create input and encryption objects
account_manager_AH.Graphics = account_manager_AH.GraphicsBox(account_manager_AH.pen, account_manager_AH.pen_NC)
Acc_Graphics = account_manager_AH.GraphicsBox(account_manager_AH.pen, account_manager_AH.pen_NC)
Acc_inputs = account_manager_AH.GetInputs()
enc = account_manager_AH.Encryption()

account_manager_AH.Graphics.draw_login()

# handles all outputs 
def handle_click(x, y):
    global login, quiz, leaderboard
    
    if login == False:
        
        Acc_inputs.handle_click(x, y)
        
        # link inputs to encryption
        enc.U_response = Acc_inputs.U_response
        enc.P_response = Acc_inputs.P_response
        enc.username_entered = Acc_inputs.username_entered
        enc.password_entered = Acc_inputs.password_entered
        enc.NC = Acc_inputs.NC
        
        # link inputs to Quiz        
        Quiz_AH.GraphicsManager.username = Acc_inputs.U_response
        
        
        if Acc_inputs.Exit == True:
            account_manager_AH.screen.bye()

        # Run only when both inputs entered        
        if enc.username_entered and enc.password_entered:
            enc.run()
            
            
        if enc.login == True:
            login = True
            time.sleep(1)
        
    #Run Quiz File 
    if login == True: 
        account_manager_AH.screen.clear()
        Quiz_AH.QuizGame.leaderboard = leaderboard
        Quiz_Graphics = Quiz_AH.GraphicsManager(Acc_inputs.U_response, Quiz_AH.QuizGame)
        Quiz_Game = Quiz_AH.QuizGame(Quiz_Graphics, leaderboard)
        Quiz_AH.GraphicsManager.game = Quiz_Game
        quiz = True
        Quiz_Game.play()


#click handler

account_manager_AH.screen.onscreenclick(handle_click)


#-------------------------------------------------------------------------------


turtle.done()