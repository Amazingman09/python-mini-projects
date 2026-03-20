import turtle
import csv
import random
import time

class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer.lower()

    def is_correct(self, guess):
        if guess.strip().lower() == self.correct_answer:
            return True 
        return False 

class GraphicsManager:
    def __init__(self, username):
        self.screen = turtle.Screen()
        self.screen.title("One Percent Club")
        self.screen.bgcolor("blue")
        self.screen.setup(width=1500, height=700)

        self.drawer = self.create_turtle("red")
        self.score_writer = self.create_turtle("green")
        self.strike_writer = self.create_turtle("brown")
        self.pen = self.create_turtle("white", (0, 260))
        self.quest_writer = self.create_turtle("white", (0, 0))
        self.wrong_display = self.create_turtle("red")
        self.end_writer = self.create_turtle("black")
        self.username = username

    def create_turtle(self, color, position=(0, 0)):
        self = turtle.Turtle()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.color(color)
        self.goto(position)
        return self
         
    def MainMenu(self):    
        
        self.keypress = False  # Use an instance variable

        def key():
            self.keypress = True

        self.screen.listen()
        self.screen.onkeypress(key, "g")

        while not self.keypress:
            self.pen.write("PRESS G TO PLAY", align="center", font=("Arial", 20, "bold"))
            time.sleep(0.5)
            self.pen.clear()
            time.sleep(0.5)
        
        self.pen.clear()
        self.pen.goto(0,50)
        self.pen.write(f"Hello {self.username}", align="center", font=("Arial", 20, "bold"))
        time.sleep(3)
        self.pen.clear()
        self.pen.write("Welcome to the 1/100 club", align="center", font=("Arial", 20, "bold"))
        time.sleep(3)
        self.pen.clear()

    def draw_grid(self):
        self.screen.bgcolor("gray")
        self.drawer.clear()
        y = -100
        for _ in range(2):
            for x in [-500, 10]:
                self.drawer.goto(x, y)
                self.drawer.pendown()
                self.drawer.fillcolor("black")
                self.drawer.begin_fill()
                for _ in range(2):
                    self.drawer.forward(500)
                    self.drawer.right(90)
                    self.drawer.forward(100)
                    self.drawer.right(90)
                self.drawer.end_fill()
                self.drawer.penup()
            y -= 110
            
        width = 1000
        height = 250 # top left corner co-ordnates 
        
        x = -width // 2
        y = 250
        self.drawer.goto(x, y)
        self.drawer.pendown()
        self.drawer.fillcolor("black")
        self.drawer.begin_fill()
        for _ in range(2):
            self.drawer.forward(width)
            self.drawer.right(90)
            self.drawer.forward(height)
            self.drawer.right(90)
        self.drawer.end_fill()
        self.drawer.penup()
           
    def draw_leaderboard(self):
        
        BOX_WIDTH = 200
        NUM_BOX_WIDTH = 60
        BOX_HEIGHT = 50
        START_X = -438
        START_Y = 200 
        lb_length = 7
        y = START_Y
            
        for counter in range(3):
       
            for _ in range(lb_length):
                
                self.drawer.penup()
                self.drawer.goto(START_X, y) # main answer box
                self.drawer.pendown()
                self.drawer.fillcolor("Black")
                self.drawer.begin_fill()
                for _ in range(2):
                    self.drawer.pencolor("Red")
                    self.drawer.forward(BOX_WIDTH)
                    self.drawer.right(90)
                    self.drawer.forward(BOX_HEIGHT)
                    self.drawer.right(90)
                self.drawer.end_fill()
                self.drawer.penup()
                
                self.drawer.goto(START_X + BOX_WIDTH + 10, y) #number box
                self.drawer.pendown()
                self.drawer.fillcolor("Black")
                self.drawer.begin_fill()
                for _ in range(2):
                    self.drawer.forward(NUM_BOX_WIDTH)
                    self.drawer.right(90)
                    self.drawer.forward(BOX_HEIGHT)
                    self.drawer.right(90)

                self.drawer.end_fill()
                self.drawer.penup()
                
                y = y - 50
                
            START_X = START_X + BOX_WIDTH + NUM_BOX_WIDTH + 30
            y = START_Y
            
        width = 1200
        height = 150 # top left corner co-ordnates 
        
        x = -width // 2
        y = 380
        self.drawer.goto(x, y)
        self.drawer.pendown()
        self.drawer.fillcolor("black")
        self.drawer.begin_fill()
        for _ in range(2):
            self.drawer.forward(width)
            self.drawer.right(90)
            self.drawer.forward(height)
            self.drawer.right(90)
        self.drawer.end_fill()
        self.drawer.penup()
            
    def display_users(self, users_list):
        BOX_WIDTH = 200
        NUM_BOX_WIDTH = 60
        BOX_HEIGHT = 50
        START_X = -438
        START_Y = 200 
        lb_length = 7
        y = START_Y
        width = 1200
        height = 150
        numPerRow = 0
        
        x1 = -width // 2
        y1 = 380
        self.pen.pencolor("White")
        self.pen.penup()
        self.pen.goto(0, y1 - (height//1.25))
        self.pen.write(f"LEADERBOARD",  align="center", font=("Arial", 50, "bold"))
        for i in range(3):
            while finished != True and numPerRow <= 7:
                #write names
                self.pen.penup()
                self.pen.goto(START_X + (BOX_WIDTH//2), y - BOX_HEIGHT)
                self.pen.pendown()
                self.pen.write(f"{users_list[i][1]}",  align="center", font=("Arial", 25, "bold"))
                
                #write scores
                self.pen.penup()
                self.pen.goto(START_X + BOX_WIDTH + 10 + (NUM_BOX_WIDTH//2), y - BOX_HEIGHT)
                self.pen.pendown()
                self.pen.write(f"{users_list[i][3]}",  align="center", font=("Arial", 25, "bold"))
                self.pen.penup()
                if not users_list[i + 1]:
                    finished = False
                    numPerRow += 1
                
                y -= 50
                    
            numPerRow = 0    
            START_X = START_X + BOX_WIDTH + NUM_BOX_WIDTH + 30
            y = START_Y
            
            
    def show_question(self, question):
        self.pen.clear()
        self.pen.goto(0, 125)  # Position above the answer boxes
        self.pen.write(question.text, align="center", font=("Arial", 20, "bold"))

    def display_wrong(self, strikes):
        self.wrong_display.clear()
        self.wrong_display.goto(0, -240)
        self.wrong_display.write("X", align="center", font=("Arial", 50, "bold"))
        self.screen.ontimer(self.wrong_display.clear, 1000)
        self.update_strikes(strikes)

    def update_strikes(self, strikes):
        self.strike_writer.clear()
        self.strike_writer.goto(-700, 250)
        self.strike_writer.write(f"Strikes: {strikes} / 3", font=("Arial", 16, "bold"))

    def update_score(self, score):
        self.score_writer.clear()
        self.score_writer.goto(550, 250)
        self.score_writer.write(f"Score: {score} / 10", font=("Arial", 20, "bold"))
        
    def display_options_in_boxes(self, options):
        positions = [
            (-250, -160),  # Top left box center
            (250, -160),    # Top right box center
            (-250, -270),  # Bottom left box center
            (250, -270)     # Bottom right box center
        ]
        
        choice = ("A","B","C","D")

        for i in range(4):
            self.pen.goto(positions[i])
            self.pen.write(f"{choice[i]}) {options[i]}", align="center", font=("Arial", 16, "bold"))

    def show_end_message(self, message, color="red"):
        self.end_writer.goto(0, 200)
        self.end_writer.color(color)
        self.end_writer.write(message, align="center", font=("Arial", 20, "bold"))
        
class GetInputs:
    def __init__(self, leaderboard):
        self.guess = ""
        self.leaderboard = leaderboard
        self.boxes = {
            "A": (-500, 0, -110, -210),   # x cords, y cords
            "B": (10, 500, -110, -210),
            "C": (-500, 0, -220, -320),
            "D": (10, 500, -220, -320)
            }
        
    
    
class QuizGame:
    def __init__(self, graphics, leaderboard):
        self.graphics = graphics
        self.questions = self.load_questions()
        self.used_indices = []
        self.score = 0
        self.strikes = 0
        self.max_strikes = 3
        self.max_score = 10
        self.guess = ""
        self.boxes = {
            "A": (-500, 0, -110, -210),   # x cords, y cords
            "B": (10, 500, -110, -210),
            "C": (-500, 0, -220, -320),
            "D": (10, 500, -220, -320)
        }
        self.guess = ""
        self.waiting_for_answer = False
        self.users = []*3
        self.username = GraphicsManager.username
      


    def load_questions(self):
        # Load choices from choices.csv
        choices_data = {}
        with open('choices.txt', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cn = row['CN']
                choices_data[cn] = [
                    row['Choice1'].strip(),
                    row['Choice2'].strip(),
                    row['Choice3'].strip(),
                    row['Choice4'].strip()
                ]


    # Load questions from questions.csv
        questions = []
        self.letter_list = []
        letters = ["A", "B", "C", "D"]

        with open('questions.txt', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                q_text = row['QuestionText'].strip()
                correct = row['CorrectAnswer'].strip().lower()
                cn = row['CN']

                options = choices_data.get(cn, [])
                random.shuffle(options)

                correct_option = next((opt for opt in options if opt.lower() == correct), None)
                
                if correct_option is None:
                    print(f"Warning: Correct answer '{correct}' not found in options {options}")
                    continue  # Skip this question to avoid crashing
                
                correct_index = options.index(correct_option)
                letter_answer = letters[correct_index]
                self.letter_list.append(letter_answer)

                questions.append(Question(q_text, options, correct_option))
    
        return questions           
        
    def GetUserScores(self):
        with open("User Details.csv", mode="r") as file:
            file_reader = csv.reader(file)
            self.users = list(file_reader)

    
    def updateDatabase(self):
        # Update the current user data
        for row in self.users:
            if row[1] == self.username:
                row[3] = str(self.score)

        # Rewrite the CSV
        with open("User Details.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            for counter in range(len(self.users)):
                writer.writerows([self.users[counter][0], self.users[counter][1], self.users[counter][2], self.users[counter][3]])
        
                    
    def SortScores(self):
        self.users.sort(key=lambda x: x[2], reverse=True)
    
    def run_leaderboard(self):
        
        
        self.GetUserScores()
        self.updateDatabase()
        self.SortScores()
            
        self.graphics.draw_leaderboard()
        self.graphics.display_users(self.users)
        
    def play(self):
        
        print("Questions:", len(self.questions))
        print("Letters:", len(self.letter_list))
        
        self.graphics.MainMenu()
        self.graphics.draw_grid()
        self.graphics.update_score(self.score)
        self.graphics.update_strikes(self.strikes)

        while len(self.used_indices) < len(self.questions) and self.strikes < self.max_strikes and self.score < self.max_score:
            index = random.randint(0, len(self.questions) - 1)
            if index in self.used_indices:
                continue

            question = self.questions[index]
            self.graphics.show_question(question)
            self.graphics.display_options_in_boxes(question.options)
            self.used_indices.append(index)
            
            guess = self.graphics.screen.textinput("Your Guess", "Enter your answer: ")
            
            if guess and question.is_correct(guess):
                self.score += 1
                self.graphics.update_score(self.score)
            elif guess.lower() == self.letter_list[index].lower():
                self.score += 1
                self.graphics.update_score(self.score)
            else:
                self.strikes += 1
                self.graphics.display_wrong(self.strikes)
            
        if self.strikes >= self.max_strikes:
            self.graphics.show_end_message("Game Over! You've run out of strikes.")
        elif self.score < self.max_score:
            self.graphics.show_end_message(f"Not bad though it's only a mere {self.score} points", color="green")
        else:
            self.graphics.show_end_message("GG. You're in the One Percent Club!", color="green")
            
        time.sleep(2)
        self.graphics.drawer.clear()
        self.graphics.pen.clear()
        self.graphics.strike_writer.clear()
        self.graphics.quest_writer.clear()
        self.graphics.score_writer.clear()
        self.graphics.end_writer.clear()
        
    
        self.run_leaderboard()


        turtle.done()
        
if __name__ == "__main__":
    GraphicsManager.username = "TestUser"
    graphics = GraphicsManager
    game = QuizGame(graphics("TestUser"), leaderboard=False)
    game.play()
    
        

        

 # Run the game
#graphics = GraphicsManager()
#game = QuizGame(graphics)
#game.play()
