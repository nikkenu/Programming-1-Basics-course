#Programming 1, round 13: task 13.10
#Niklas Nurminen, niklas.nurminen@student.tut.fi
#Game called paisti.
#The idea is to throw dices and wish that u hit number that is equal to CUP position.
#Player who gets cups to red, gets question to CONSOLE, if answer is right = wins the game
#Player 1 at the top, Player 2 at the bottom.


from tkinter import *
from tkinter import messagebox
import random
import time

CUPS_IN_A_ROW = 6 #Skaalautuva!
TURNS = 1 #Skaalautuva!
DICES = 2 #Skaalautuva!

DICEPICS = ["1.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif", "1S.gif"]

class Paisti():

    def __init__(self,player_one,player_two):
        self.__window = Tk()
        self.__window.title("Paistipeli by Niklas Nurminen")
        self.__player_one_name = str(player_one)
        self.__player_two_name = str(player_two)
        self.__turn = 0 #Tells which player turn it is
        self.__turns = 0 #Gives information how many throw player has done in one turn ( MAX 1 )

        #Pictures to list
        self.__dicepics = []
        for picture in DICEPICS:
            picture = PhotoImage(file=picture)
            self.__dicepics.append(picture)

        #Player 1 cups
        self.__player_one_cups = []
        for i in range(CUPS_IN_A_ROW):
            new_label = Label(self.__window,bg="green",fg="white",text=i+1,highlightcolor="red",width=5,height=3,relief="solid")
            new_label.grid(row=1,column=i)
            self.__player_one_cups.append(new_label)

        #Player 2 cups
        self.__player_two_cups = []
        for i in range(CUPS_IN_A_ROW):
            new_label = Label(self.__window, bg="green",fg="white",text=i+1, highlightcolor="red", width=5, height=3, relief="solid")
            new_label.grid(row=3, column=i)
            self.__player_two_cups.append(new_label)

        #Throw button
        self.__throwButton = Button(self.__window, text="Throw",command=self.throw)
        self.__throwButton.grid(row=2,column=2,columnspan=2,sticky=E+W)

        #Quit button
        self.__quitButton = Button(self.__window,text="Quit",bg="red",fg="white",command=self.__window.destroy)
        self.__quitButton.grid(row=2,column=4,columnspan=2,sticky=E+W)

        #Turn change button
        self.__turnChange = Button(self.__window,text="End Turn",bg="yellow",command=self.end_turn)
        self.__turnChange.grid(row=2,column=0,columnspan=2,sticky=E+W)

        #New game button
        self.__new_game = Button(self.__window,text="New Game",relief="raised",command=self.initialize_game)
        self.__new_game.grid(row=5,columnspan=6,sticky=E+W)

        #Info
        self.__infoLabel = Label(self.__window)
        self.__infoLabel.grid(row=4,columnspan=6,sticky=E+W)

        #Instructions
        self.__instructions = Button(self.__window,text="Instructions",command=self.instructions)
        self.__instructions.grid(row=6,columnspan=6,sticky=W+E)

        #Dices
        self.__dices_in_field = []
        for i in range(DICES):
            new_label = Label(self.__window)
            new_label.grid(row=2,column=CUPS_IN_A_ROW+i,sticky=NW)
            self.__dices_in_field.append(new_label)

        self.initialize_game()

    def instructions(self):
        """
        Pop-up window, where are the instructions
        """
        guide = Toplevel()
        guide.title("Instructions")
        Message(guide,text="Each player has one throw on each turn. To win the game, you have to get cups 2-6(red)"
                           "then activate bonus game, where you need to do some calculations. If you are right you win").pack()

    def initialize_game(self):
        """
        Restores game to default settings.
        Example dice numbers to = 1
        Sets every cup to available
        And changes cup labels to green
        """
        self.__turn = 0
        self.__gameinfo = "{} starts".format(self.__player_one_name)

        #Restores dice values to "1"
        for label in self.__dices_in_field:
            label.configure(image=self.__dicepics[0])

        #Sets every's cup value to "TRUE" in list. (If "false" cup is not available in game)
        self.__cups_available_P_one = [True] * CUPS_IN_A_ROW
        self.__cups_available_P_two = [True] * CUPS_IN_A_ROW

        #Sets default green background for cups
        for label in self.__player_one_cups:
            label.configure(bg="green")
            label.configure(state=NORMAL)

        for label in self.__player_two_cups:
            label.configure(bg="green")
            label.configure(state=NORMAL)

        self.update_text()

    def update_text(self):
        """Updates text when called"""
        self.__infoLabel.configure(text=self.__gameinfo)

    def end_turn(self):
        """
        This restores self.__turns and tells which player turn it is 
        """
        if self.__turn == 0:
            self.__turn += 1
            self.__gameinfo = "{} turn".format(self.__player_two_name)
        else:
            self.__turn -= 1
            self.__gameinfo = "{} turn".format(self.__player_one_name)
        self.__turns = 0
        self.update_text()

    def throw(self):
        """
        If we hit throw button, this function gets activated. This generates value(DICES) numbers from 1-6 and adds to them list.
        Then it changed dices pictures to match values we generated.
        Also calls functions like bad_dice_value, or throw_player
        """
        if self.__turns < TURNS:
            dices = []
            i = 0
            while i < DICES:
                dices.append(random.randint(1,6))
                i+=1
            for i in range(DICES):
                self.__dices_in_field[i].configure(image=self.__dicepics[dices[i]-1])
            dices_value = sum(dices)
            if dices_value > CUPS_IN_A_ROW: # if "useless" pops up text and ends turn automatically
                self.bad_dice_value()
            else:
                if self.__turn == 0:
                    self.throw_player_one(dices_value)
                else:
                    self.throw_player_two(dices_value)
            self.__turns += 1

    def bad_dice_value(self):
        """
        Pop-up window if dices total values is over CUPS_IN_A_ROW, because there value cant be used
        """
        top = Toplevel()
        top.title('Bad Luck!')
        Message(top, text="Unfortunately dices value was over {}".format(CUPS_IN_A_ROW), padx=20, pady=20).pack()
        top.after(2000, top.destroy)

    def throw_player_one(self,dices_value):
        """
        If cups is available turns it to red and changes value to False
        :param dices_value: Dices total value
        """
        if self.__cups_available_P_two[dices_value-1] == True:
            self.__player_two_cups[dices_value-1].configure(bg="red")
            self.__cups_available_P_two[dices_value-1] = False
            self.check_bonus(self.__cups_available_P_two)

    def throw_player_two(self,dices_value):
        """
        Exactly the same but to player one
        """
        if self.__cups_available_P_one[dices_value-1] == True:
            self.__player_one_cups[dices_value-1].configure(bg="red")
            self.__cups_available_P_one[dices_value-1] = False
            self.check_bonus(self.__cups_available_P_one)

    def check_bonus(self,list):
        """
        Checks if list values are "False" from 1->. We skip [0], because its the bonus question, and also value cant be under amount of dices
        So we use this list[1:]
        :param list: Gets cups_available list 
        """
        min_value = DICES-1
        check_values = True
        for i in list[min_value:]:
            if i != False:
                check_values = False
        if check_values == True:
            self.question()

    def question(self):
        """
        This could be pop-up window aswell, but to save some time it prints to console, and you answer there.
        Basically we generate 3 random numbers between 1-10. If user answer right, we call function self.winner()
        """
        numbers = random.sample(range(1,10),3)
        correct = sum(numbers)
        print("How much is {} + {} + {}".format(numbers[0],numbers[1],numbers[2]))
        print(correct) #TODO: ASSARIN AIVOJEN HELPOTTAMISEKSI
        answer = int(input(" = "))
        if answer == correct:
            self.winner()
        else:
            self.__gameinfo = "Wrong answer"
            self.update_text()

    def winner(self):
        """
        If player hits the correct answer this function is called. 
        Cups label turn to yellow etc. Visual effects mostly. 
        """
        name = self.__player_one_name
        if self.__turn == 1:
            name = self.__player_two_name
        for label in self.__player_one_cups:
            label.configure(bg="yellow",fg="black")
        for label in self.__player_two_cups:
            label.configure(bg="yellow",fg="black")
        for i in range(DICES):
            self.__dices_in_field[i].configure(image=self.__dicepics[6])
        self.__gameinfo = "{} IS THE WINNER!!!".format(name)
        self.update_text()

    def start(self):
        self.__window.mainloop()


class Names: #This program only asks player names
    def __init__(self):
        self.__name_window = Tk()
        self.__name_window.title("Tell ur names")
        self.__player_one = Label(self.__name_window,text="First player name: ")
        self.__player_one.grid(row=0,column=0)
        self.__one_name = Entry(self.__name_window)
        self.__one_name.grid(row=0,column=1)

        self.__player_two = Label(self.__name_window,text="Second player name: ")
        self.__player_two.grid(row=1,column=0)
        self.__two_name = Entry(self.__name_window)
        self.__two_name.grid(row=1, column=1)

        self.__readyButton = Button(self.__name_window,text="RDY?",bg="green",command=self.save)
        self.__readyButton.grid(column=2,row=0,rowspan=2,sticky=N+S)


    def save(self): #Saves Entrys to "self", and then destroys windows that the game can start
        self.__first_name = self.__one_name.get()
        self.__second_name = self.__two_name.get()
        self.__name_window.destroy()

    def get_one(self): #Returns Player 1 name
        return self.__first_name

    def get_two(self): #Returns Player 2 name
        return self.__second_name

    def start(self):
        self.__name_window.mainloop()

def main():

    names = Names()
    names.start()

    ui = Paisti(names.get_one(),names.get_two())
    ui.start()
main()