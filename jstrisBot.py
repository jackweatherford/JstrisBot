import pyautogui
from pynput.keyboard import Key, Controller, Listener

top = [0 for _ in range(10)]
diff = [0 for _ in range(9)]
wait = False
c_pressed = False

def filterMoves(moves_no_holes):
	press_c = True
	for moves in moves_no_holes:
		if len(moves) > 0:
			press_c = False
			break
	
	if press_c:
		if not c_pressed:
			pyautogui.press('c')
			return -1
		else:
			print('Unlucky, all moves create holes')
			# TODO: Continue, make a hole + keep list of holes?
			exit(1)
	
	moves_no_3 = []
	
	for moves in moves_no_holes:
		temp = []
		for pos, diffs in moves.items():
			if abs(diffs[0]) < 3 and abs(diffs[1]) < 3:
				temp.append(pos)
		moves_no_3.append(temp)
	
	return moves_no_3

def bestLine(moves):
	best_diff_sum = 200
	best_move = -1
	rot = -1
	
	# 0 rotations
	for move in moves[0]:
		temp_top = top.copy()
		temp_top[move] += 1
		temp_top[move+1] += 1
		temp_top[move+2] += 1
		temp_top[move+3] += 1
		
		diff_sum = 0
		for i in range(9):
			diff_sum += abs(temp_top[i+1] - temp_top[i])
		
		if abs(diff_sum) < best_diff_sum:
			best_diff_sum = abs(diff_sum)
			best_move = move
			rot = 0
	
	# 1 rotation
	for move in moves[1]:
		temp_top = top.copy()
		temp_top[move] += 4
		
		diff_sum = 0
		for i in range(9):
			diff_sum += abs(temp_top[i+1] - temp_top[i])
		
		if abs(diff_sum) < best_diff_sum:
			best_diff_sum = abs(diff_sum)
			best_move = move
			rot = 1
	
	return best_move, rot

# Move format => moves<# rotations> = {column index : (left diff, right diff), ... }
def placeLine():
	# 0 rotations
	moves0 = {}
	if top[0] == top[1] == top[2] == top[3]:
		moves0[0] = (0, diff[3] - 1)
	
	for i in range(1, 6):
		if top[i] == top[i+1] == top[i+2] == top[i+3]:
			moves0[i] = (diff[i-1] + 1, diff[i+3] - 1)
	
	if top[6] == top[7] == top[8] == top[9]:
		moves0[6] = (diff[5] + 1, 0)
	
	# 1 rotation
	moves1 = {}
	moves1[0] = (0, diff[0] - 4)
	for i in range(1, 9):
		moves1[i] = (diff[i-1] + 4, diff[i] - 4)
	moves1[9] = (diff[8] +  4, 0)
	
	# moves with no holes
	moves_no_holes = [moves0, moves1]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = []
	for i in moves_no_3[0]: # get moves that can reduce >=3 walls
		if i == 0:
			if diff[3] >= 3:
				moves0.append(i)
			break
		if i == 6:
			if diff[5] <= -3:
				moves0.append(i)
			break
		if diff[i + 3] >= 3 or diff[i - 1] <= -3:
			moves0.append(i)
	
	# 1 rotation
	moves1 = []
	for i in moves_no_3[1]:
		if i == 0:
			if diff[0] >= 3:
				moves1.append(i)
			break
		if i == 9:
			if diff[8] <= -3:
				moves1.append(i)
			break
		if diff[i] >= 3 or diff[i - 1] <= -3:
			moves1.append(i)
	
	moves_reducing = [moves0, moves1]
	
	if len(moves_no_3[0]) == 0 and len(moves_no_3[1]) == 0: # no moves create < 3 walls
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestLine(moves_no_holes)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move, rot = bestLine(moves_reducing)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestLine(moves_no_3)
		else: # at least 1 move can reduce walls
			best_move, rot = bestLine(moves_reducing)
	
	# 0 rotations
	if rot == 0:
		top[best_move] += 1
		top[best_move+1] += 1
		top[best_move+2] += 1
		top[best_move+3] += 1
		
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	
	else: # 1 rotation
		top[best_move] += 4
		
		pyautogui.press('up')
		if best_move < 5:
			pyautogui.press('left', presses=5-best_move)
		elif best_move > 5:
			pyautogui.press('right', presses=best_move-5)
		pyautogui.press('space')

def bestSquare(moves):
	best_diff_sum = 200
	best_move = -1
	
	# 0 rotations
	for move in moves[0]:
		temp_top = top.copy()
		temp_top[move] += 2
		temp_top[move+1] += 2
		
		diff_sum = 0
		for i in range(9):
			diff_sum += abs(temp_top[i+1] - temp_top[i])
		
		if abs(diff_sum) < best_diff_sum:
			best_diff_sum = abs(diff_sum)
			best_move = move
	
	return best_move

def placeSquare():
	# 0 rotations
	moves0 = {}
	if top[0] == top[1]:
		moves0[0] = (0, diff[1] - 2)
	
	for i in range(1, 8):
		if top[i] == top[i+1]:
			moves0[i] = (diff[i-1] + 2, diff[i+1] - 2)
	
	if top[8] == top[9]:
		moves0[6] = (diff[7] + 2, 0)
	
	# moves with no holes
	moves_no_holes = [moves0]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = []
	for i in moves_no_3[0]: # get moves that can reduce >=3 walls
		if i == 0:
			if diff[1] >= 3:
				moves0.append(i)
			break
		if i == 8:
			if diff[7] <= -3:
				moves0.append(i)
			break
		if diff[i + 1] >= 3 or diff[i - 1] <= -3:
			moves0.append(i)
	
	moves_reducing = [moves0]
	
	if len(moves_no_3[0]) == 0: # no moves create < 3 walls
		if len(moves0) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move = bestSquare(moves_no_holes)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move = bestSquare(moves_reducing)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move = bestSquare(moves_no_3)
		else: # at least 1 move can reduce walls
			best_move = bestSquare(moves_reducing)
	
	top[best_move] += 2
	top[best_move+1] += 2
	
	if best_move < 4:
		pyautogui.press('left', presses=4-best_move)
	elif best_move > 4:
		pyautogui.press('right', presses=best_move-4)
	pyautogui.press('space')

def placeBlueL():

	# 0 rotations
	if top[0] == top[1] == top[2] and abs(top[2] + 1 - top[3]) < 3:
		top[0] += 2
		top[1] += 1
		top[2] += 1
		
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return

	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2] and abs(top[i] + 2 - top[i-1]) < 3 and abs(top[i+2] + 1 - top[i+3]) < 3:
			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)

			top[i] += 2
			top[i+1] += 1
			top[i+2] += 1

			pyautogui.press('space')
			return

	if top[7] == top[8] == top[9] and abs(top[7] + 2 - top[6]) < 3:
		top[7] += 2
		top[8] += 1
		top[9] += 1
		
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 1 rotation
	if top[0] + 2 == top[1] and abs(top[1] + 1 - top[2]) < 3:
		top[0] += 3
		top[1] += 1
		
		pyautogui.press('up')
		pyautogui.press('left', presses=4)
		pyautogui.press('space')
		return

	for i in range(1, 7):
		if top[i] + 2 == top[i+1] and abs(top[i] + 3 - top[i-1]) < 3 and abs(top[i+1] + 1 - top[i+2]) < 3:

			top[i] += 3
			top[i+1] += 1

			pyautogui.press('up')

			if i < 4:
				pyautogui.press('left', presses=4-i)
			elif i > 4:
				pyautogui.press('right', presses=i-4)
			
			pyautogui.press('space')
			return

	if top[8] + 2 == top[9] and abs(top[8] + 3 - top[7]) < 3:
		top[8] += 3
		top[9] += 1
		
		pyautogui.press('up')
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 2 rotations
	if top[0] == top[1] == top[2] + 1 and abs(top[2] + 2 - top[3]) < 3:
		top[0] += 1
		top[1] += 1
		top[2] += 2
		
		pyautogui.press('up', presses=2)
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return

	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2] + 1 and abs(top[i+2] + 2 - top[i+3]) < 3 and abs(top[i] + 1 - top[i-1]) < 3:
			
			top[i] += 1
			top[i+1] += 1
			top[i+2] += 2
			
			pyautogui.press('up', presses=2)
			
			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)

			pyautogui.press('space')
			return

	if top[7] == top[8] == top[9] + 1 and abs(top[7] + 1 - top[6]) < 3:
		top[7] += 1
		top[8] += 1
		top[9] += 2
		
		pyautogui.press('up', presses=2)
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 3 rotations
	if top[0] == top[1] and abs(top[1] + 3 - top[2]) < 3:
		top[0] += 1
		top[1] += 3
		
		pyautogui.press('up', presses=3)
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return

	for i in range(1, 8):
		if top[i] == top[i+1] and abs(top[i+1] + 3 - top[i+2]) < 3 and abs(top[i] + 1 - top[i-1]) < 3:

			top[i] += 1
			top[i+1] += 3

			pyautogui.press('up', presses=3)

			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)
			
			pyautogui.press('space')
			return

	if top[8] == top[9] and abs(top[8] + 1 - top[7]) < 3:
		top[8] += 1
		top[9] += 3
		
		pyautogui.press('up', presses=3)
		pyautogui.press('right', presses=5)
		pyautogui.press('space')
		return

	pyautogui.press('c')

def placeOrangeL():

	# 0 rotations
	if top[0] == top[1] == top[2] and abs(top[2] + 2 - top[3]) < 3:
		top[0] += 1
		top[1] += 1
		top[2] += 2
		
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return

	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2] and abs(top[i+2] + 2 - top[i+3]) < 3 and abs(top[i] + 1 - top[i-1]) < 3:
			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)

			top[i] += 1
			top[i+1] += 1
			top[i+2] += 2

			pyautogui.press('space')
			return

	if top[7] == top[8] == top[9] and abs(top[7] + 1 - top[6]) < 3:
		top[7] += 1
		top[8] += 1
		top[9] += 2
		
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 1 rotation
	if top[0] == top[1] and abs(top[1] + 1 - top[2]) < 3:
		top[0] += 3
		top[1] += 1
		
		pyautogui.press('up')
		pyautogui.press('left', presses=4)
		pyautogui.press('space')
		return

	for i in range(1, 8):
		if top[i] == top[i+1] and abs(top[i] + 3 - top[i-1]) < 3 and abs(top[i+1] + 1 - top[i+2]) < 3:

			top[i] += 3
			top[i+1] += 1

			pyautogui.press('up')

			if i < 4:
				pyautogui.press('left', presses=4-i)
			elif i > 4:
				pyautogui.press('right', presses=i-4)
			
			pyautogui.press('space')
			return

	if top[8] == top[9] and abs(top[8] + 3 - top[7]) < 3:
		top[8] += 3
		top[9] += 1
		
		pyautogui.press('up')
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 2 rotations
	if top[0] + 1 == top[1] == top[2] and abs(top[2] + 1 - top[3]) < 3:
		top[0] += 2
		top[1] += 1
		top[2] += 1
		
		pyautogui.press('up', presses=2)
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return

	for i in range(1, 7):
		if top[i] + 1 == top[i+1] == top[i+2] and abs(top[i] + 2 - top[i-1]) < 3 and abs(top[i+2] + 1 - top[i+3]) < 3:
			
			top[i] += 2
			top[i+1] += 1
			top[i+2] += 1
			
			pyautogui.press('up', presses=2)
			
			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)

			pyautogui.press('space')
			return

	if top[7] + 1 == top[8] == top[9] and abs(top[7] + 2 - top[6]) < 3:
		top[7] += 2
		top[8] += 1
		top[9] += 1
		
		pyautogui.press('up', presses=2)
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 3 rotations
	if top[0] == top[1] + 2 and abs(top[1] + 3 - top[2]) < 3:
		top[0] += 1
		top[1] += 3
		
		pyautogui.press('up', presses=3)
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return

	for i in range(1, 7):
		if top[i] == top[i+1] + 2 and abs(top[i+1] + 3 - top[i+2]) < 3 and abs(top[i] + 1 - top[i-1]) < 3:

			top[i] += 1
			top[i+1] += 3

			pyautogui.press('up', presses=3)

			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)
			
			pyautogui.press('space')
			return

	if top[8] == top[9] + 2 and abs(top[8] + 1 - top[7]) < 3:
		top[8] += 1
		top[9] += 3
		
		pyautogui.press('up', presses=3)
		pyautogui.press('right', presses=5)
		pyautogui.press('space')
		return

	pyautogui.press('c')

def placeT():

	# 0 rotations
	if top[0] == top[1] == top[2] and abs(top[2] + 1 - top[3]) < 3:
		pass
	
	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2]:
			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)

			top[i] += 1
			top[i+1] += 2
			top[i+2] += 1

			pyautogui.press('space')
			return

	pyautogui.press('c')

def placeGreenZ():

	# 0 rotations
	if top[0] == top[1] == top[2] - 1 and abs(top[2] + 1 - top[3]) < 3:
		top[0] += 1
		top[1] += 2
		top[2] += 1
		
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return
	
	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2] - 1 and abs(top[i] + 1 - top[i-1]) < 3 and abs(top[i+2] + 1 - top[i+3]) < 3:
			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)

			top[i] += 1
			top[i+1] += 2
			top[i+2] += 1

			pyautogui.press('space')
			return
	
	if top[7] == top[8] == top[9] - 1 and abs(top[7] + 1 - top[6]) < 3:
		top[7] += 1
		top[8] += 2
		top[9] += 1
		
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 1 rotation
	if top[0] - 1 == top[1] and abs(top[1] + 2 - top[2]) < 3:
		top[0] += 2
		top[1] += 2
		
		pyautogui.press('up')
		pyautogui.press('left', presses=4)
		pyautogui.press('space')
		return
	
	for i in range(1, 8):
		if top[i] - 1 == top[i+1] and abs(top[i] + 2 - top[i-1]) < 3 and abs(top[i+1] + 2 - top[i+2]) < 3:
			
			top[i] += 2
			top[i+1] += 2
			
			pyautogui.press('up')
			
			if i < 4:
				pyautogui.press('left', presses=4-i)
			elif i > 4:
				pyautogui.press('right', presses=i-4)

			pyautogui.press('space')
			return
	
	if top[8] - 1 == top[9] and abs(top[8] + 2 - top[7]) < 3:
		top[8] += 2
		top[9] += 2
		
		pyautogui.press('up')
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	pyautogui.press('c')

def placeRedZ():

	# 0 rotations
	if top[0] - 1 == top[1] == top[2] and abs(top[2] + 1 - top[3]) < 3:
		top[0] += 1
		top[1] += 2
		top[2] += 1
		
		pyautogui.press('left', presses=3)
		pyautogui.press('space')
		return
	
	for i in range(1, 7):
		if top[i] - 1 == top[i+1] == top[i+2] and abs(top[i] + 1 - top[i-1]) < 3 and abs(top[i+2] + 1 - top[i+3]) < 3:
			if i < 3:
				pyautogui.press('left', presses=3-i)
			elif i > 3:
				pyautogui.press('right', presses=i-3)

			top[i] += 1
			top[i+1] += 2
			top[i+2] += 1

			pyautogui.press('space')
			return
	
	if top[7] - 1 == top[8] == top[9] and abs(top[7] + 1 - top[6]) < 3:
		top[7] += 1
		top[8] += 2
		top[9] += 1
		
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	# 1 rotation
	if top[0] == top[1] - 1 and abs(top[1] + 2 - top[2]) < 3:
		top[0] += 2
		top[1] += 2
		
		pyautogui.press('up')
		pyautogui.press('left', presses=4)
		pyautogui.press('space')
		return
	
	for i in range(1, 8):
		if top[i] == top[i+1] - 1 and abs(top[i] + 2 - top[i-1]) < 3 and abs(top[i+1] + 2 - top[i+2]) < 3:
			
			top[i] += 2
			top[i+1] += 2
			
			pyautogui.press('up')
			
			if i < 4:
				pyautogui.press('left', presses=4-i)
			elif i > 4:
				pyautogui.press('right', presses=i-4)

			pyautogui.press('space')
			return
	
	if top[8] == top[9] - 1 and abs(top[8] + 2 - top[7]) < 3:
		top[8] += 2
		top[9] += 2
		
		pyautogui.press('up')
		pyautogui.press('right', presses=4)
		pyautogui.press('space')
		return

	pyautogui.press('c')

def update(piece_color):
	global top, diff, wait, c_pressed
	
	# Wait for other threads to join
	while wait:
		pass
	wait = True
	
	if piece_color == 155:
		print('Placing Line')
		placeLine()
	elif piece_color == 159:
		print('Placing Square')
		placeSquare()
	elif piece_color == 65:
		print('Placing Blue L')
		placeBlueL()
	elif piece_color == 91:
		print('Placing Orange L')
		placeOrangeL()
	elif piece_color == 41:
		print('Placing T')
		placeT()
	elif piece_color == 177:
		print('Placing Green Z')
		placeGreenZ()
	elif piece_color == 15:
		print('Placing Red Z')
		placeRedZ()
	
	print(top)
	# Update bottom
	bottom = [y > 0 for y in top]
	
	# Clear lines
	if bottom == [1 for _ in range(10)]:
		while 0 not in top:
			top = [y - 1 for y in top]
		bottom = [y > 0 for y in top]
	
	# Update diff
	for i in range(9):
		diff[i] = top[i+1] - top[i]
	
	wait = False

def on_press(key):
	if key == Key.space or key == Key.down or repr(key) == "'c'":
		if repr(key) == "'c'":
			print('Pressed C')
			c_pressed = True
		else:
			c_pressed = False
		
		piece_color = pyautogui.pixel(624, 232)[1]
		while piece_color == 0 and wait:
			piece_color = pyautogui.pixel(624, 232)[1]
		
		update(piece_color)

if __name__ == '__main__':
	# Disable failsafe (move mouse to bottom right corner to terminate script)
	pyautogui.FAILSAFE = False
	
	# Listen for key presses
	listener = Listener(on_press=on_press)
	listener.start()
	
	try:
		# Wait for GO! message to appear
		go_color = 0
		while not go_color == 203:
			go_color = pyautogui.pixel(638, 600)[0]
		
		# Wait for first piece to appear
		first_piece_color = 0
		while first_piece_color == 0:
			first_piece_color = pyautogui.pixel(624, 232)[1]
		update(first_piece_color)
		
		# Keep the code alive and listening for space presses.
		while True:
			pass
	
	except KeyboardInterrupt: # If Ctrl-C input
		exit('Terminating')
