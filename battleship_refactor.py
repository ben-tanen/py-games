import random 
import sys

# initate and play the game
def play_game():
    # get board size, generate, and print it
    board_size = get_board_size()
    board = generate_board(board_size)
    print_board(board)

    # determine the ship's location
    ship_col = random_col(board)
    ship_row = random_row(board)

    # can guess up to 75% of the board
    for attempt in range(1, int(board_size**2 * .75)):
        guess = get_guess(board, attempt, ship_col, ship_row)

        # if user guessed correctly
        if is_guess_correct(guess, ship_col, ship_row):
            board[ship_col][ship_row] = "!"
            print_board_with_msg(board, ">> Congratulations!! You sank my battleship!")

        # if user ran out of guesses
        elif attempt == int(board_size**2 * .75) - 1:
            board[ship_col][ship_row] = "!"
            print_board_with_msg(board, ">> Sorry, you lost!")
        
        # if the user guessed wrong but has more guesses  
        else:
            board[int(guess[1:]) - 1][ord(guess[0]) - 65] = "x"
            print_board_with_msg(board, ">> You missed my battleship!")

# get the game board size from the user
def get_board_size():
    low_bound = 2
    high_bound = 26

    # keep asking for board size until user gives valid one
    while True:
        board_size = input(">> Board Size (" + str(low_bound) + " - " + str(high_bound) + ") ==> ")

        # check if board size is valid (within range & of int type)
        try: 
            if int(board_size) >= low_bound and int(board_size) <= high_bound:
                return int(board_size)
        except ValueError:
            continue

# generate the board originally
def generate_board(board_size):
    board = [ ]
    for x in range(0,board_size):
        board.append(["~"] * board_size)

    return board

# print the board
def print_board(board):
    print

    # generate / print top line
    top = '  '
    for y in range(0,len(board)):
        top += chr(65 + y) + '  '
    print(top)

    # print contents of board
    for x in range(0,len(board)):
        print("| " + "  ".join(board[x]) + " | " + str(x+1))

    print

# print the board with a message following
def print_board_with_msg(board, msg):
    print_board(board)
    print(msg)
          
# get random row for ship to exist in
def random_row(list):
    return random.randint(1,len(list))

# get random col for ship to exist in
def random_col(list):
    return random.randint(1,len(list))

# get the guess from the user
# also validates that it is of the correct format
def get_guess(board, guess_num, ship_col, ship_row):
    while True:
        guess = input(">> Guess " + str(guess_num) + "/" + str(int(len(board)**2 * .75) - 1) + ": Where do you think the ship is? Ex: B3 ==> ").upper()

        # if guess is of valid format, return guess
        if is_valid_guess(board, guess):
            return guess

        # additional cases: QUIT quits the game and TELL ME gives the user the location of the ship
        elif guess == "QUIT" or guess == "Q":
            sys.exit('System Quit')
        elif guess == "TELL ME":
            print('>> cheater... ' + str(ship_col) + ', ' + str(ship_row))

# determines if guess is of the correct format
def is_valid_guess(board, guess):
    # check if guess is correct length
    if len(guess) < 2 or len(guess) > 3:
        return False

    # check if 'number' of guess is valid number
    try: 
        int(guess[1:])
    except ValueError:
        return False

    # check if letter is in valid range
    if ord(guess[0]) - 64 <= 0 or ord(guess[0]) - 64 > len(board):
        return False

    # check if guess number is in valid range
    if int(guess[1:]) > len(board) or int(guess[1:]) <= 0:
        return False

    # check if space has already been guessed
    if board[int(guess[1:]) - 1][ord(guess[0]) - 65] == "x":
        return False

    return True

# determines if the guess is correct
def is_guess_correct(guess, ship_col, ship_row):
    if ord(guess[0]) - 64 == ship_col and int(guess[1:]) == ship_row:
        return True
    else:
        return False

# start the game
play_game()