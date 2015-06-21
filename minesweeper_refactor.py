import random 
import sys
import os

def play_game():
    # determine size of board and number of mines
    board_size = get_board_size()
    num_mine = [1, 15, 40][(board_size / 5) - 1]

    # generate board and place mines
    board = generate_board(board_size)
    mine_list = place_mines(board, num_mine)

    # loop until user wins or loses
    spaces_revealed = 0
    flags_placed = 0
    while True:
        direction_msg = "Flags Placed: " + str(flags_placed) + "/" + str(num_mine) + "\n\nTo check location, input coordinate (ex: B5)\nTo place a flag on a mine, input '*' and the coordinate (ex: *A3)\n"
        print_board_with_msg(board, direction_msg)

        move = get_next_move(board)
        revealed_space = place_move(board, mine_list, move)

        if revealed_space == 'bomb':
            print_board_with_msg(board, "And BOOM goes the dynamite! Sorry about that... Better luck next time!\n")
            sys.exit()
        elif revealed_space == 'flag':
            flags_placed += 1
        elif revealed_space == 'open':
            spaces_revealed += 1

            # check if the user uncovered all spaces (and won)
            if spaces_revealed + num_mine == board_size ** 2:
                print_board_with_msg(board, "Congratulations!! You won!\n")
                sys.exit()

def get_board_size():
    print 'Board Size:\nA - 5x5\nB - 10x10\nC - 15x15'
    query_string = 'What size board would you like? '
    while True:
        size = raw_input(query_string).lower()

        if size == 'a' or size == '5' or size == '5x5':
            return 5
        elif size == 'b' or size == '10' or size == '10x10':
            return 10
        elif size == 'c' or size == '15' or size == '15x15':
            return 15
        else:
            query_string = 'Invalid size... What size board would you like? '

def generate_board(board_size):
    board = [ ]

    for x in range(0,board_size):
        board.append(["~"] * board_size)

    return board

def place_mines(board, num_mine):
    mine_list = [ ]
    while (len(mine_list) < num_mine):
        col = random_col(board)
        row = random_row(board)
        if ([col, row] not in mine_list):
            mine_list.append([col, row])

    return mine_list

def random_col(list):
    return random.randint(0,len(list) - 1)

def random_row(list):
    return random.randint(0,len(list) - 1)

# print the board
def print_board(board):
    print

    # generate / print top line
    top = '  '
    for y in range(0,len(board)):
        top += unichr(65 + y) + '  '
    print top

    # print contents of board
    for x in range(0,len(board)):
        print "| " + "  ".join(board[x]) + " | " + str(x+1)

    print

# print the board with a message following
def print_board_with_msg(board, msg):
    os.system('clear')
    print_board(board)
    print msg

def get_next_move(board):
    while True:
        move = raw_input("-> ").upper()

        # if move is of valid format, return guess
        if move[0] == '*' and is_valid_move(board, move):
            return [int(move[2:]) - 1, ord(move[1]) - 65, True]
        elif move[0] != '*' and is_valid_move(board, move):
            return [int(move[1:]) - 1, ord(move[0]) - 65, False]

        # if user wants to quit game
        elif move == "QUIT" or move == "Q":
            sys.exit('System Quit')

# determines if move is of the correct format
def is_valid_move(board, move):
    # check if guess is correct length
    if len(move) < 2:
        print 'Error: move input too short'
        return False

    # set move to be array of form: [col, row, is_flag]
    if (move[0] == '*'):
        move = [move[2:], ord(move[1]) - 65, True]
    else:
        move = [move[1:], ord(move[0]) - 65, False]

    # check if 'number' of guess is valid number
    try: 
        move[0] = int(move[0]) - 1
    except ValueError:
        print 'Error: invalid move row number'
        return False

    # check if letter is in valid range
    if move[1] < 0 or move[1] > len(board):
        print 'Error: move letter out of range'
        return False

    # check if guess number is in valid range
    if move[0] > len(board) or move[0] < 0:
        print 'Error: move number out of range'
        return False

    # check if space has already been guessed
    if board[move[0]][move[1]] != '~':
        print 'Error: space already revealed'
        return False

    if move[2] and board[move[0]][move[1]] == '*':
        print 'Error: space already flagged'
        return False

    return True

def place_move(board, mine_list, move):
    if move[2]:
        board[move[0]][move[1]] = '*'
        return 'flag'
    elif [move[0], move[1]] in mine_list:
        for mine in mine_list:
            board[mine[0]][mine[1]] = 'X'
        return 'bomb'
    else:
        board[move[0]][move[1]] = str(get_surrounding_bomb_count(mine_list, move))

        # if 0 bombs, 'recurse' to uncover all 0s
        if board[move[0]][move[1]] == '0':
            to_do_spaces = get_unchecked_surrounding_spaces(board, move)
            
            while len(to_do_spaces) != 0:
                active = to_do_spaces.pop(0)
                if board[active[0]][active[1]] == '~':
                    board[active[0]][active[1]] = str(get_surrounding_bomb_count(mine_list, active))
                    if get_surrounding_bomb_count(mine_list, active) == 0:
                        to_do_spaces += get_unchecked_surrounding_spaces(board, active)

        return 'open'

def get_surrounding_bomb_count(mine_list, move):
    surrounding_bombs = 0

    for inc_col in range(-1,2):
        for inc_row in range(-1,2):
            if not (inc_col == 0 and inc_row == 0):
                    surrounding_bombs += [move[0] + inc_row, move[1] + inc_col] in mine_list

    return surrounding_bombs

def get_unchecked_surrounding_spaces(board, move):
    spaces = [ ]
    for inc_col in range(-1,2):
        for inc_row in range(-1,2):
            if inc_col == 0 and inc_row == 0:
                continue
            elif move[0] + inc_row < 0 or move[1] + inc_col < 0 or move[0] + inc_row >= len(board) or move[1] + inc_col >= len(board):
                continue
            elif board[move[0] + inc_row][move[1] + inc_col] == '~':
                spaces.append([move[0] + inc_row, move[1] + inc_col])

    return spaces

play_game()




