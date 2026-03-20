import turtle
import csv
import random
import time

# Constants
BOX_WIDTH = 200
BOX_HEIGHT = 50
USERNAME_X = -100
USERNAME_Y = 125
PASSWORD_X = -100
PASSWORD_Y = 25
NC_X = 60  # new account x
NC_Y = -40  # new account y
EXIT_Y = 300
EXIT_X = 600
BACK_Y = 300
BACK_X = 550

# Setup pens

class GraphicsBox:
    def __init__(self):
        self.pen = self.create_turtle("Black")
        self.pen.hideturtle()
        self.pen.penup()
        
        self.pen_NC = self.create_turtle("Black")
        self.pen_NC.hideturtle()
        self.pen_NC.penup()
        
        self.screen = turtle.Screen()
        self.screen.setup(width=800, height=600)
        self.screen.bgcolor("AntiqueWhite1")
        self.screen.title("Password Manager")
    
    def create_turtle(self, color, position=(0, 0)):
        self = turtle.Turtle()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.color(color)
        self.goto(position)
        return self
        
    

    def draw_login(self):
        # Clear previous drawings/messages
        self.pen.clear()
        self.pen_NC.clear()

        # Draw Username box
        self.pen.goto(USERNAME_X, USERNAME_Y)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.fillcolor("white")
        for _ in range(2):
            self.pen.forward(BOX_WIDTH)
            self.pen.right(90)
            self.pen.forward(BOX_HEIGHT)
            self.pen.right(90)
        self.pen.end_fill()
        self.pen.penup()
        self.pen.goto(0, 125)
        self.pen.write("Enter Username", align="center", font=("Arial", 14, "bold"))

        # Draw Password box
        self.pen.goto(PASSWORD_X, PASSWORD_Y)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.fillcolor("white")
        for _ in range(2):
            self.pen.forward(BOX_WIDTH)
            self.pen.right(90)
            self.pen.forward(BOX_HEIGHT)
            self.pen.right(90)
        self.pen.end_fill()
        self.pen.penup()
        self.pen.goto(0, 25)
        self.pen.write("Enter Password", align="center", font=("Arial", 14, "bold"))
        
        # Write create account link
        self.pen_NC.goto(NC_X, NC_Y)
        self.pen_NC.pencolor("Blue")
        self.pen_NC.write("Create new account", align="center", font=("Arial", 7, "underline"))
        self.pen_NC.pencolor("Black")
        
        #Draw Exit Button
        self.pen.goto(EXIT_X, EXIT_Y)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.pencolor("Red")
        self.pen.fillcolor("Red")
        for _ in range(2):
            self.pen.forward(BOX_WIDTH/4)
            self.pen.right(90)
            self.pen.forward(BOX_HEIGHT)
            self.pen.right(90)
        self.pen.end_fill()
        self.pen.penup()
        self.pen.goto(625, 255)
        self.pen.pencolor("White")
        self.pen.write("X", align="center", font=("Arial", 25, "bold"))
        self.pen.pencolor("Black")
        
        
    def draw_NC(self):
        # New account screen header
        self.screen.bgcolor("green")
        self.pen_NC.clear()
        self.pen.goto(0, 200)
        self.pen.write("Create new account", align="center", font=("Arial", 20, "underline"))


class GetInputs:
    def __init__(self, graphics: GraphicsBox):
        self.screen = graphics.screen
        self.pen = graphics.pen

        self.P_response = ""
        self.U_response = ""
        self.password_entered = False
        self.username_entered = False
        self.NC = False # True if user clicked "Create new account"
        self.processing = False
        self.Exit = False
        

    def handle_click(self, x, y):
        astrick = ""

        # Password box click
        if -100 <= x <= 100 and -25 <= y <= 25 and not self.password_entered:
            self.P_response = self.screen.textinput("Enter Password", "Enter your password:")
            if self.P_response:
                astrick = "*" * len(self.P_response)
                self.pen.goto(0, -15)
                self.pen.write(astrick, align="center", font=("Arial", 16, "normal"))
                self.password_entered = True

        # Username box click
        elif -100 <= x <= 100 and 75 <= y <= 125 and not self.username_entered:
            self.U_response = self.screen.textinput("Enter Username", "Enter your username:")
            if self.U_response:
                self.pen.goto(0, 85)
                self.pen.write(self.U_response, align="center", font=("Arial", 16, "normal"))
                self.username_entered = True
                
        # Exit box click
        #elif 600 <= x <= 650 and 250 <= y <= 300 and self.processing != True:
        #    self.Exit = True            
            

        # "Create new account" link click
        elif 20 <= x <= 100 and -50 <= y <= -30 and not self.NC:
            Acc_graphics.draw_NC()
            self.NC = True
        if self.password_entered and self.username_entered and self.processing == False:
            self.processing = True
            enc.run()

class Encryption:
    def __init__(self, inputs: GetInputs, graphics: GraphicsBox):
        self.U_response = inputs.U_response
        self.P_response = inputs.P_response 

        self.password_entered = inputs.password_entered
        self.username_entered = inputs.username_entered
        self.NC = inputs.NC  # True if user clicked "Create new account"
        self.processing = inputs.processing

        self.CR_Password = ""
        self.__key = None
        self.pen = graphics.pen
        self.user_check = False
        self.login = False
        self.NewPK = ""
        self.users = []

    def getEncryptionKey(self):
        # Read user details and store them
        self.processing = True
        with open("User Details.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            self.users = list(reader)
            
            LastPK = str(self.users[len(self.users) - 1][0])
            number = int(LastPK[1:])
            self.NewPK = "P" + str(number + 1)
            
        # Generate and store key once per account
        self.__key = random.randint(1, 1000)
        with open("QKeysQ.csv", mode="a", newline="") as file:
            writer = csv.writer(file)            
            writer.writerow([self.NewPK, self.__key])

    def getEncryptedDetails(self):
        # Encrypt current password with current key
        ascii_List = [ord(i) for i in self.P_response]
        CR_List = [i - self.__key for i in ascii_List]
        self.CR_Password = ",".join(map(str, CR_List))
        
        # Save username and encrypted password 
        return self.CR_Password
    
    def check_Username(self):
        with open("User Details.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            usernames = [row[1] for row in reader if row]
        if self.U_response in usernames:
            self.pen.goto(0, -100)
            self.pen.write("Username already in use.", align="center", font=("Arial", 16, "bold"))
            self.user_check = True

            return False
        

    def uploadDetails(self):
        self.CR_Password = self.getEncryptedDetails() 
        # Save username and encrypted password                     
        with open("User Details.csv", mode="a", newline="") as file:                       
            writer = csv.writer(file)
            writer.writerow([self.NewPK, self.U_response, self.CR_Password, 0])
            
        with open("User Details.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            self.users = list(reader)
        print("All users")
        print("")
        for counter in range (len(self.users)):
            print(f"{self.users[counter][0]}|{self.users[counter][1]}|{self.users[counter][3]}|") # list of usernames

    def check_login(self):
        try:
            # Read stored users
            with open("User Details.csv", mode="r") as file:
                reader = csv.reader(file)
                self.users = list(reader)

            if not self.users:
                self.pen.goto(0, -100)
                self.pen.write("No users stored.", align="center", font=("Arial", 16, "bold"))
                self.processing = False
                return False
            else:
                self.pen.goto(-300, -75)
                self.pen.write("Accessing database ✅", align="center", font=("Arial", 10, "bold"))
                

            usernames = [row[1] for row in self.users if row]
            if self.U_response not in usernames:
                self.pen.goto(0, -100)
                self.pen.write("Username not found.", align="center", font=("Arial", 16, "bold"))
                self.processing = False
                return False
            else:
                self.pen.goto(-150, -75)
                self.pen.write("Found Username ✅", align="center", font=("Arial", 10, "bold"))
            

            # Read matching key by index
            with open("QKeysQ.csv", mode="r") as key_file:
                key_reader = csv.reader(key_file)          
                keys_data = list(key_reader)                
#                 self.pen.goto(0, -75)
#                 self.pen.write("Decrypting...", align="center", font=("Arial", 10, "bold"))
                print("All users")
                print("")
                for counter in range (len(self.users)):
                    print(f"{self.users[counter][0]}|{self.users[counter][1]}|{self.users[counter][3]}|") # list of usernames    
                print("")
                print(len(self.users))

               # use equi-join to find decryption key, by using the primary key
                counter = 0
                for counter in range(len(self.users)):
                    if keys_data[counter][0] == self.users[counter][0] and self.U_response == self.users[counter][1]:
                        key = int(keys_data[counter][1])
                        stored_password = self.users[counter][2]
                        
                self.pen.goto(0, -75)
                self.pen.write("Decrypting...", align="center", font=("Arial", 10, "bold"))

            # Decrypt and compare
            encrypted_values = stored_password.split(",")
            decrypted_chars = [chr(int(value) + key) for value in encrypted_values]
            decrypted_password = "".join(decrypted_chars)
            
            self.pen.goto(150, -75)
            self.pen.write("Dectypting sucessfull ✅", align="center", font=("Arial", 10, "bold"))
            
            self.pen.goto(300, -75)
            self.pen.write("Checking password ...", align="center", font=("Arial", 10, "bold"))

            if decrypted_password == self.P_response:
                self.pen.goto(0, -150)
                self.pen.write("Login successful!", align="center", font=("Arial", 16, "bold"))
                self.login = True
                self.processing = False
                return True
            else:
                self.pen.goto(0, -150)
                self.pen.write("Incorrect password.", align="center", font=("Arial", 16, "bold"))
                self.processing = False
                return False

        except Exception as e:
            self.pen.goto(0, -100)
            self.pen.write(f"Error: {e}", align="center", font=("Arial", 16, "bold"))
            self.processing = False
            return False


    def run(self):
        
        enc.username_entered = Acc_inputs.username_entered
        enc.password_entered = Acc_inputs.password_entered
        enc.NC = Acc_inputs.NC
        enc.U_response = Acc_inputs.U_response
        enc.P_response = Acc_inputs.P_response

        print(f"Username: {self.username_entered}")
        print(f"Password: {self.password_entered}")
        
        if self.username_entered and self.password_entered and self.NC == True and self.check_Username() != False:
            # Create new account
            self.getEncryptionKey()
            self.uploadDetails()
            self.pen.goto(0, -130)
            self.pen.write("Account created!", align="center", font=("Arial", 16, "bold"))
        if self.username_entered and self.password_entered and self.NC == False:
            # Login
            self.check_login()
            self.processing = False
            self.login = True

if __name__ == "__main__":
    
    Acc_graphics = GraphicsBox()
    Acc_inputs = GetInputs(Acc_graphics)
    enc = Encryption(Acc_inputs, Acc_graphics)

    enc.NC = Acc_inputs.NC
    program_running = True
    
    Acc_graphics.draw_login()
    Acc_graphics.screen.onscreenclick(Acc_inputs.handle_click)
    turtle.done()
    
        
        
