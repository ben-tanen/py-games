import random 
import sys
import os

board = [ ]
test = ''
top = '      '
tally = 0
num_flag = 0
guess_num = 0

#Ask for Board Size (must be between 2 and 10, or system will return an error and quit)
print 'Board Size:'
print 'A - 5x5'
print 'B - 10x10'
print 'C - 15x15'
while test == '':
	board_size  = raw_input('What size would you like? ')
	if board_size == 'A' or board_size == 'a' or board_size == '5' or board_size == '5x5':
		board_size = 5
		num_mine = 5
		print
		break
	elif board_size == 'B' or board_size == 'b' or board_size == '10' or board_size == '10x10':
		board_size = 10
		num_mine = 15
		print
		break
	elif board_size == 'C' or board_size == 'c' or board_size == '15' or board_size == '15x15':
		board_size = 15
		num_mine = 40
		print
		break
	else:
		print "Invalid Board Size. Try Again."
		print

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
	elif y == 11:
		y = "K"
	elif y == 12:
		y = "L"
	elif y == 13:
		y = "M"
	elif y == 14:
		y = "N"
	elif y == 15:
		y = "O"
	top = top + str(y) + '  '

#Define print_board Function
def print_board(list):
	print top
	for x in range(0,board_size):
		if x < 9:
			print '  ' + str(x+1) + " | " + "  ".join(list[x]) + " | " + str(x+1)
		if x > 8:
			print ' ' + str(x+1) + " | " + "  ".join(list[x]) + " | " + str(x+1)
	print top
	print
		  
#Define Function to place mine in random row
def random_row(list):
	return random.randint(1,len(list))

#Define Function to place mine in random column	
def random_col(list):
	return random.randint(1,len(list))

mine_col = [ ]
mine_row = [ ]

for x in range(0,num_mine):
	while x != 'blah':
		rand_row = random_row(board)
		rand_col = random_col(board)
		if board[rand_row - 1][rand_col - 1] == '~':
			board[rand_row - 1][rand_col - 1] = 'x'
			mine_row.append(rand_row)
			mine_col.append(rand_col)
			break


for x in range(0,len(mine_row)):
	board[mine_row[x] - 1][mine_col[x] - 1] = '~'

while test == '':
	os.system('clear')
	tally = 0
	flag = False
	print_board(board)
	print 'Mines: ' + str(num_flag) + '/' + str(num_mine)
	print
	print 'To check location, input coordinate (ex: B5)'
	print 'To place a flag on a mine, input f and the coordinate (ex: *A3)'
	print
	if guess_num == (board_size**2) - num_mine:
		sys.exit('You win!!')
	guess = raw_input('-> ')
	guess_num += 1
	guess_letter = guess[0]
	if guess[0] == '*':
		guess_num -= 1
		flag = True
		guess_letter = guess[1]
		if len(guess) == 3:
			guess_number = int(guess[2])
		elif len(guess) == 4:
			guess_number = int(guess[2:4])
		num_flag += 1
	elif len(guess) == 2 and flag == False:
		guess_number = int(guess[1])
	elif len(guess) == 3 and flag == False:
		guess_number = int(guess[1:3])
	elif guess == 'quit' or guess == 'QUIT':
		sys.exit('System Quit')

	guess_letter_value = ord(guess_letter) - 96
	if guess_letter_value < 1:
		guess_letter_value += 32

	for x in range(0,len(mine_row)):
		if guess_number == mine_row[x] and guess_letter_value == mine_col[x] and flag == False:
			for x in range(0,len(mine_row)):
				board[mine_row[x] - 1][mine_col[x] - 1] = 'X'
			os.system('clear')
			print_board(board)
			print 'And BOOM goes the dynamite'
			print 'Sorry, you lost...'
			sys.exit(' ')

	if guess_number != 1 and guess_letter_value != 1:	
		# Top Left Corner
		for x in range(0,len(mine_row)):
			if guess_number - 1 == mine_row[x] and guess_letter_value - 1 == mine_col[x]:
				tally += 1

	if guess_number != 0 and guess_letter_value != board_size:
		# Top Right Corner
		for x in range(0,len(mine_row)):
			if guess_number - 1 == mine_row[x] and guess_letter_value + 1 == mine_col[x]:
				tally += 1

	if guess_number != board_size and guess_letter_value != board_size:
		# Bottom Right Corner
		for x in range(0,len(mine_row)):
			if guess_number + 1 == mine_row[x] and guess_letter_value + 1 == mine_col[x]:
				tally += 1

	if guess_number != board_size and guess_letter_value != 0:
		# Bottom Left Corner
		for x in range(0,len(mine_row)):
			if guess_number + 1 == mine_row[x] and guess_letter_value - 1 == mine_col[x]:
				tally += 1

	if guess_number != 0:
		# Top
		for x in range(0,len(mine_row)):
			if guess_number - 1 == mine_row[x] and guess_letter_value == mine_col[x]:
				tally += 1

	if guess_number != board_size:
		# Bottom
		for x in range(0,len(mine_row)):
			if guess_number + 1 == mine_row[x] and guess_letter_value == mine_col[x]:
				tally += 1

	if guess_letter_value != 0:
		# Left
		for x in range(0,len(mine_row)):
			if guess_number == mine_row[x] and guess_letter_value - 1 == mine_col[x]:
				tally += 1

	if guess_letter_value != board_size:
		# Right
		for x in range(0,len(mine_row)):
			if guess_number == mine_row[x] and guess_letter_value + 1 == mine_col[x]:
				tally += 1
	if board[guess_number - 1][guess_letter_value - 1] != '~':
		guess_num -= 1
	board[guess_number - 1][guess_letter_value - 1] = str(tally)
	if flag == True:
		board[guess_number - 1][guess_letter_value - 1] = '*'





