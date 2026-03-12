# ----- Family fortunes -----


#by Stephen Alao
# Date: 2025-05-26

#Remeber to add sounds effects 

# Family Fortunes Game
import turtle

from playsound import playsound

import threading

import time




# Load background image

screen = turtle.Screen()

screen.title("Family Fortunes Game")

screen.bgpic("sunset_background.gif")

screen.setup(width=1500, height=700)

# initaisle variables

strikes = 0

    #Correct answers(eneter answer and number of people who said it) NOT DICTIONARYYYY!!!!!

correct_answers = [

    ("A", 42),

    ("B", 37),

    ("C", 29),

    ("D", 19),

    ("E", 11)

]

found_answers = []

    # constant variables

BOX_WIDTH = 200

NUM_BOX_WIDTH = 60

BOX_HEIGHT = 50

START_X = -BOX_WIDTH // 2

START_Y = 150

MAX_STRIKES = 3

# Turtles

drawer = turtle.Turtle()

drawer.hideturtle()

drawer.penup()

drawer.speed(0)



writer = turtle.Turtle()

writer.hideturtle()

writer.penup()

writer.color("black")

writer.speed(0)



wrong_display = turtle.Turtle()

wrong_display.hideturtle()

wrong_display.penup()

wrong_display.color("red")

wrong_display.speed(0)



strike_writer = turtle.Turtle()

strike_writer.hideturtle()

strike_writer.penup()

strike_writer.color("darkred")

strike_writer.speed(0)


pen = turtle.Turtle()

pen.hideturtle()

pen.speed(0)

pen.color("black")

pen.penup()

pen.goto(0,260)

pen.write("Place Holder Question",align="center", font=("Courier",16, "normal")) # enter your question here

#Functions

    #music

def play_intro_music():
    playsound("family-fortunes-final-compressed.mp3")

def play_wrong():
    playsound("family-fortunes-wrong-buzzer.mp3")

def play_right():
    playsound("family-fortunes-ding.mp3")

    # anamation

def draw_grid():

    drawer.clear()

    y = START_Y

    for _ in correct_answers:

        # main answer box

        drawer.goto(START_X, y)

        drawer.pendown()

        drawer.fillcolor("white")

        drawer.begin_fill()

        for _ in range(2):

            drawer.pencolor("black")

            drawer.forward(BOX_WIDTH)

            drawer.right(90)

            drawer.forward(BOX_HEIGHT)

            drawer.right(90)

        drawer.end_fill()

        drawer.penup()

        #number box

        drawer.goto(START_X + BOX_WIDTH + 10, y)

        drawer.pendown()

        drawer.begin_fill()

        for _ in range(2):

            drawer.forward(NUM_BOX_WIDTH)

            drawer.right(90)

            drawer.forward(BOX_HEIGHT)

            drawer.right(90)

        drawer.end_fill()

        drawer.penup()



        y -= (BOX_HEIGHT + 10)

     #check if answer is right and display it

def reveal_answers():

    writer.clear()

    y = START_Y - BOX_HEIGHT // 2

    # repeats for each relation in dictionary
    for ans, num in correct_answers:

        if ans in found_answers:

        #display answer

            writer.goto(START_X + BOX_WIDTH // 2, y - 10)

            writer.write(ans, align="center", font=("Arial", 18, "bold"))

        #display number

            writer.goto(START_X + BOX_WIDTH + 10 + NUM_BOX_WIDTH // 2, y- 10)

            writer.write(str(num), align="center", font=("Arial", 16, "bold"))

        y -= (BOX_HEIGHT + 10)

   # show strikes

def display_wrong(strikes):

    wrong_display.clear()

    wrong_display.goto(0, -240)

    wrong_display.write("X", align="center", font=("Arial", 50, "bold"))
        # show x for a second
    screen.ontimer(wrong_display.clear, 1000)

    playsound("family-fortunes-wrong-buzzer.mp3")  # sound effect for wrong answer


    update_strikes_display(strikes)

        # display strikes at top

def update_strikes_display(strikes):

    strike_writer.clear()

    strike_writer.goto(-180, 180)

    strike_writer.write(f"Strikes: {strikes} / {MAX_STRIKES}", font=("Arial", 16, "bold"))


       # GaMe OvEr :(
def game_over():

    writer.goto(0, -220)

    writer.color("red")

    writer.write("Game Over! You've run out of strikes.", align="center", font=("Arial", 20, "bold"))

#main program
#Start game




draw_grid()

reveal_answers()

update_strikes_display(strikes)

while len(found_answers) < len(correct_answers) and strikes < MAX_STRIKES:

    # adds mini input box

    guess = screen.textinput("Your Guess", "Enter a word: ")
    
    # checks if user has guessed
    if guess:

        # removes whitespace and makes input lowercase
        guess = guess.strip().lower()

        # think it creates all answer words idk copied from internet when code didnt work
        answer_words = [ans for ans, _ in correct_answers]
        
        #displays answer and adds it to the list
        if guess in answer_words and guess not in found_answers:

            found_answers.append(guess)

            reveal_answers()

            playsound("family-fortunes-ding.mp3")  # sound effect for correct answer

        else:

            strikes += 1

            display_wrong(strikes)

#End Game

if strikes >= MAX_STRIKES:

    game_over()
    playsound("Comedy failure.mp3")  # sound effect for game over

else:

    writer.goto(0, -220)

    writer.color("green")

    writer.write("Well done! You found all the answers!", align="center", font=("Arial", 20, "bold"))

    playsound("level-win-6416.mp3")  # sound effect for winning


turtle.done()

