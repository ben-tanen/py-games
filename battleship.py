import random 
import sys
import os

board = [ ]
test = ''
top = '  '
tally = 0

#Ask for Board Size (must be between 2 and 10, or system will return an error and quit)
while test == '':
    board_size = int(raw_input("Board Size (2-10): "))
    print
    if board_size < 11 and board_size > 2:
        test = ' '
        break
    else:
        print "Invalid Board Size. Try Again."

#Create Board List
for x in range(0,board_size):
    board.append(["~"] * board_size)
    
#Create Top Row (if/else statements make top letters)
for y in range(1,board_size+1):
    if y == 1:
        y = "A"
    elif y == 2:
        y = "B"
    elif y == 3:
        y = "C"
    elif y == 4:
        y = "D"
    elif y == 5:
        y = "E"
    elif y == 6:
        y = "F"
    elif y == 7:
        y = "G"
    elif y == 8:
        y = "H"
    elif y == 9:
        y = "I"
    elif y == 10:
        y = "J"
    top = top + str(y) + '  '

#Define print_board Function
def print_board(list):
    print top
    for x in range(0,board_size):
        print "| " + "  ".join(list[x]) + " | " + str(x+1)
          
#Define Function to place ship in random row
def random_row(list):
    return random.randint(0,len(list)-1)

#Define Function to place ship in random column 
def random_col(list):
    return random.randint(0,len(list)-1)

print_board(board)
ship_row = random_row(board) + 1
ship_col = random_col(board) + 1

for x in range(0,board_size**2 - board_size):
    test = ' '
    print
    print "- - - Guess " + str(x+1) + "/" + str(board_size**2 - board_size) + " - - -"
    while test == ' ':
        guess = raw_input("Where do you think the ship is? Ex: B3 ==> ")
        skip = False
        if len(guess) == 0:
            skip = True
            guess = 'A1'
        guess_letter = guess[0]
        if len(guess) == 2:
            guess_number = guess[1]
        elif len(guess) == 3:
            guess_number = guess[1:3]
        elif guess == 'quit' or guess == 'QUIT':
            sys.exit('System Quit')
        
        if guess == 'tell me':
            print "System Override: Ship Pos - " + str(ship_col) + str(ship_row)
            skip = True

        if guess_letter == "A":
            guess_letter_value = 1
        elif guess_letter == "B":
            guess_letter_value = 2
        elif guess_letter == "C":
            guess_letter_value = 3
        elif guess_letter == "D":
            guess_letter_value = 4
        elif guess_letter == "E":
            guess_letter_value = 5
        elif guess_letter == "F":
            guess_letter_value = 6
        elif guess_letter == "G":
            guess_letter_value = 7
        elif guess_letter == "H":
            guess_letter_value = 8
        elif guess_letter == "I":
            guess_letter_value = 9
        elif guess_letter == "J":
            guess_letter_value = 10
        
        if int(guess_number) > int(board_size) or int(guess_letter_value) > int(board_size) or int(guess_letter_value) < 1 or int(guess_number) < 1:
            print "Invalid Guess (Out of Range). Try Again"
        elif skip == True:
            print 'Invalid Guess'
        elif board[int(guess_number) - 1][int(guess_letter_value) - 1] == "~":
            test = '     '
        elif board[int(guess_number) - 1][int(guess_letter_value) - 1] == "X":
            print "Invalid Guess (You've guess that already)"
        else:
            print "Invalid Guess"
    
    print
    print "You guessed " + str(guess_letter) + str(guess_number)
    if str(guess_letter_value) == str(ship_col) and str(guess_number) == str(ship_row):
        board[int(guess_number) - 1][int(guess_letter_value) - 1] = "!"
        print 
        print "Congratulations!! You sank my battleship!"
        print
        print_board(board)
        print
        
        os.abort
        sys.exit()
    else:
        print "You missed my battleship!"
        print 
        board[int(guess_number) - 1][int(guess_letter_value) - 1] = "X"

    print_board(board)

print "I'm sorry, you lost..."
print "Try again another time"