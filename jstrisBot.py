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

def bestMove(moves, increase):
	best_diff_sum = 200
	best_move = -1
	rot = -1
	
	for i in range(len(moves)):
		for move in moves[i]:
			temp_top = top.copy()
			temp_top[move] += increase[i][0]
			if increase[i][1] > 0:
				temp_top[move+1] += increase[i][1]
				if increase[i][2] > 0:
					temp_top[move+2] += increase[i][2]
					if increase[i][3] > 0:
						temp_top[move+3] += increase[i][3]
			
			diff_sum = 0
			for j in range(9):
				diff_sum += abs(temp_top[j+1] - temp_top[j])
			
			if abs(diff_sum) < best_diff_sum:
				best_diff_sum = abs(diff_sum)
				best_move = move
				rot = i
	
	return best_move, rot

def reduceMoves(moves, width):
	reduced = []
	for i in moves: # Get moves that can reduce >=3 walls
		if i == 0:
			if diff[width - 1] >= 3:
				reduced.append(i)
			break
		if i == 10 - width:
			if diff[10 - width - 1] <= -3:
				reduced.append(i)
			break
		if diff[i + width - 1] >= 3 or diff[i - 1] <= -3:
			reduced.append(i)
	return reduced

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
	moves0 = reduceMoves(moves_no_3[0], 4)
	
	# 1 rotation
	moves1 = reduceMoves(moves_no_3[1], 1)
	
	moves_reducing = [moves0, moves1]
	
	increase = [[1,1,1,1], [4,0,0,0]]
	if len(moves_no_3[0]) == 0 and len(moves_no_3[1]) == 0: # no moves create < 3 walls
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_holes, increase)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_reducing, increase)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_3, increase)
		else: # at least 1 move can reduce walls
			best_move, rot = bestMove(moves_reducing, increase)
	
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

def placeSquare():
	# 0 rotations
	moves0 = {}
	if top[0] == top[1]:
		moves0[0] = (0, diff[1] - 2)
	
	for i in range(1, 8):
		if top[i] == top[i+1]:
			moves0[i] = (diff[i-1] + 2, diff[i+1] - 2)
	
	if top[8] == top[9]:
		moves0[8] = (diff[7] + 2, 0)
	
	# moves with no holes
	moves_no_holes = [moves0]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = reduceMoves(moves_no_3[0], 2)
	
	moves_reducing = [moves0]
	
	increase = [[2,2,0,0]]
	if len(moves_no_3[0]) == 0: # no moves create < 3 walls
		if len(moves0) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move,_ = bestMove(moves_no_holes, increase)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move,_ = bestMove(moves_reducing, increase)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move,_ = bestMove(moves_no_3, increase)
		else: # at least 1 move can reduce walls
			best_move,_ = bestMove(moves_reducing, increase)
	
	top[best_move] += 2
	top[best_move+1] += 2
	
	if best_move < 4:
		pyautogui.press('left', presses=4-best_move)
	elif best_move > 4:
		pyautogui.press('right', presses=best_move-4)
	pyautogui.press('space')

def placeBlueL():
	# 0 rotations
	moves0 = {}
	if top[0] == top[1] == top[2]:
		moves0[0] = (0, diff[2] - 1)
	
	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2]:
			moves0[i] = (diff[i-1] + 2, diff[i+2] - 1)
	
	if top[7] == top[8] == top[9]:
		moves0[7] = (diff[6] + 2, 0)
	
	# 1 rotation
	moves1 = {}
	if top[0] + 2 == top[1]:
		moves1[0] = (0, diff[1] - 1)
	
	for i in range(1, 8):
		if top[i] + 2 == top[i+1]:
			moves1[i] = (diff[i-1] + 3, diff[i+1] - 1)
	
	if top[8] + 2 == top[9]:
		moves1[8] = (diff[7] + 3, 0)
	
	# 2 rotations
	moves2 = {}
	if top[0] == top[1] == top[2] + 1:
		moves2[0] = (0, diff[2] - 2)
	
	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2] + 1:
			moves2[i] = (diff[i-1] + 1, diff[i+2] - 2)
	
	if top[7] == top[8] == top[9] + 1:
		moves2[7] = (diff[6] + 1, 0)
	
	# 3 rotations
	moves3 = {}
	if top[0] == top[1]:
		moves3[0] = (0, diff[1] - 3)
	
	for i in range(1, 8):
		if top[i] == top[i+1]:
			moves3[i] = (diff[i-1] + 1, diff[i+1] - 3)
	
	if top[8] == top[9]:
		moves3[8] = (diff[7] + 1, 0)
	
	# moves with no holes
	moves_no_holes = [moves0, moves1, moves2, moves3]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = reduceMoves(moves_no_3[0], 3)
	
	# 1 rotation
	moves1 = reduceMoves(moves_no_3[1], 2)
	
	# 2 rotations
	moves2 = reduceMoves(moves_no_3[2], 3)
	
	# 3 rotations
	moves3 = reduceMoves(moves_no_3[3], 2)
	
	moves_reducing = [moves0, moves1, moves2, moves3]
	
	increase = [[2,1,1,0], [3,1,0,0], [1,1,2,0], [1,3,0,0]]
	if len(moves_no_3[0]) == 0 and len(moves_no_3[1]) == 0 and len(moves_no_3[2]) == 0 and len(moves_no_3[3]) == 0: # no moves create < 3 walls
		if len(moves0) == 0 and len(moves1) == 0 and len(moves2) == 0 and len(moves3) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_holes, increase)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_reducing, increase)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0 and len(moves1) == 0 and len(moves2) == 0 and len(moves3) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_3, increase)
		else: # at least 1 move can reduce walls
			best_move, rot = bestMove(moves_reducing, increase)
	
	if rot == 0: # 0 rotations
		top[best_move] += 2
		top[best_move+1] += 1
		top[best_move+2] += 1
		
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	elif rot == 1: # 1 rotation
		top[best_move] += 3
		top[best_move+1] += 1
		
		pyautogui.press('up')
		if best_move < 4:
			pyautogui.press('left', presses=4-best_move)
		elif best_move > 4:
			pyautogui.press('right', presses=best_move-4)
		pyautogui.press('space')
	elif rot == 2: # 2 rotations
		top[best_move] += 1
		top[best_move+1] += 1
		top[best_move+2] += 2
		
		pyautogui.press('up', presses=2)
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	else: # 3 rotations
		top[best_move] += 1
		top[best_move+1] += 3
		
		pyautogui.press('up', presses=3)
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')

def placeOrangeL():
	# 0 rotations
	moves0 = {}
	if top[0] == top[1] == top[2]:
		moves0[0] = (0, diff[2] - 2)
	
	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2]:
			moves0[i] = (diff[i-1] + 1, diff[i+2] - 2)
	
	if top[7] == top[8] == top[9]:
		moves0[7] = (diff[6] + 1, 0)
	
	# 1 rotation
	moves1 = {}
	if top[0] == top[1]:
		moves1[0] = (0, diff[1] - 1)
	
	for i in range(1, 8):
		if top[i] == top[i+1]:
			moves1[i] = (diff[i-1] + 3, diff[i+1] - 1)
	
	if top[8] == top[9]:
		moves1[8] = (diff[7] + 3, 0)
	
	# 2 rotations
	moves2 = {}
	if top[0] + 1 == top[1] == top[2]:
		moves2[0] = (0, diff[2] - 1)
	
	for i in range(1, 7):
		if top[i] + 1 == top[i+1] == top[i+2]:
			moves2[i] = (diff[i-1] + 2, diff[i+2] - 1)
	
	if top[7] + 1 == top[8] == top[9]:
		moves2[7] = (diff[6] + 2, 0)
	
	# 3 rotations
	moves3 = {}
	if top[0] == top[1] + 2:
		moves3[0] = (0, diff[1] - 3)
	
	for i in range(1, 8):
		if top[i] == top[i+1] + 2:
			moves3[i] = (diff[i-1] + 1, diff[i+1] - 3)
	
	if top[8] == top[9] + 2:
		moves3[8] = (diff[7] + 1, 0)
	
	# moves with no holes
	moves_no_holes = [moves0, moves1, moves2, moves3]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = reduceMoves(moves_no_3[0], 3)
	
	# 1 rotation
	moves1 = reduceMoves(moves_no_3[1], 2)
	
	# 2 rotations
	moves2 = reduceMoves(moves_no_3[2], 3)
	
	# 3 rotations
	moves3 = reduceMoves(moves_no_3[3], 2)
	
	moves_reducing = [moves0, moves1, moves2, moves3]
	
	increase = [[1,1,2,0], [3,1,0,0], [2,1,1,0], [1,3,0,0]]
	if len(moves_no_3[0]) == 0 and len(moves_no_3[1]) == 0 and len(moves_no_3[2]) == 0 and len(moves_no_3[3]) == 0: # no moves create < 3 walls
		if len(moves0) == 0 and len(moves1) == 0 and len(moves2) == 0 and len(moves3) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_holes, increase)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_reducing, increase)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0 and len(moves1) == 0 and len(moves2) == 0 and len(moves3) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_3, increase)
		else: # at least 1 move can reduce walls
			best_move, rot = bestMove(moves_reducing, increase)
	
	if rot == 0: # 0 rotations
		top[best_move] += 1
		top[best_move+1] += 1
		top[best_move+2] += 2
		
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	elif rot == 1: # 1 rotation
		top[best_move] += 3
		top[best_move+1] += 1
		
		pyautogui.press('up')
		if best_move < 4:
			pyautogui.press('left', presses=4-best_move)
		elif best_move > 4:
			pyautogui.press('right', presses=best_move-4)
		pyautogui.press('space')
	elif rot == 2: # 2 rotations
		top[best_move] += 2
		top[best_move+1] += 1
		top[best_move+2] += 1
		
		pyautogui.press('up', presses=2)
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	else: # 3 rotations
		top[best_move] += 1
		top[best_move+1] += 3
		
		pyautogui.press('up', presses=3)
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')

def placeT():
	# 0 rotations
	moves0 = {}
	if top[0] == top[1] == top[2]:
		moves0[0] = (0, diff[2] - 1)
	
	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2]:
			moves0[i] = (diff[i-1] + 1, diff[i+2] - 1)
	
	if top[7] == top[8] == top[9]:
		moves0[7] = (diff[6] + 1, 0)
	
	# 1 rotation
	moves1 = {}
	if top[0] + 1 == top[1]:
		moves1[0] = (0, diff[1] - 1)
	
	for i in range(1, 8):
		if top[i] + 1 == top[i+1]:
			moves1[i] = (diff[i-1] + 3, diff[i+1] - 1)
	
	if top[8] + 1 == top[9]:
		moves1[8] = (diff[7] + 3, 0)
	
	# 2 rotations
	moves2 = {}
	if top[0] == top[1] + 1 == top[2]:
		moves2[0] = (0, diff[2] - 1)
	
	for i in range(1, 7):
		if top[i] == top[i+1] + 1 == top[i+2]:
			moves2[i] = (diff[i-1] + 1, diff[i+2] - 1)
	
	if top[7] == top[8] + 1 == top[9]:
		moves2[7] = (diff[6] + 1, 0)
	
	# 3 rotations
	moves3 = {}
	if top[0] == top[1] + 1:
		moves3[0] = (0, diff[1] - 3)
	
	for i in range(1, 8):
		if top[i] == top[i+1] + 1:
			moves3[i] = (diff[i-1] + 1, diff[i+1] - 3)
	
	if top[8] == top[9] + 1:
		moves3[8] = (diff[7] + 1, 0)
	
	# moves with no holes
	moves_no_holes = [moves0, moves1, moves2, moves3]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = reduceMoves(moves_no_3[0], 3)
	
	# 1 rotation
	moves1 = reduceMoves(moves_no_3[1], 2)
	
	# 2 rotations
	moves2 = reduceMoves(moves_no_3[2], 3)
	
	# 3 rotations
	moves3 = reduceMoves(moves_no_3[3], 2)
	
	moves_reducing = [moves0, moves1, moves2, moves3]
	
	increase = [[1,2,1,0], [3,1,0,0], [1,2,1,0], [1,3,0,0]]
	if len(moves_no_3[0]) == 0 and len(moves_no_3[1]) == 0 and len(moves_no_3[2]) == 0 and len(moves_no_3[3]) == 0: # no moves create < 3 walls
		if len(moves0) == 0 and len(moves1) == 0 and len(moves2) == 0 and len(moves3) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_holes, increase)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_reducing, increase)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0 and len(moves1) == 0 and len(moves2) == 0 and len(moves3) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_3, increase)
		else: # at least 1 move can reduce walls
			best_move, rot = bestMove(moves_reducing, increase)
	
	if rot == 0: # 0 rotations
		top[best_move] += 1
		top[best_move+1] += 2
		top[best_move+2] += 1
		
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	elif rot == 1: # 1 rotation
		top[best_move] += 3
		top[best_move+1] += 1
		
		pyautogui.press('up')
		if best_move < 4:
			pyautogui.press('left', presses=4-best_move)
		elif best_move > 4:
			pyautogui.press('right', presses=best_move-4)
		pyautogui.press('space')
	elif rot == 2: # 2 rotations
		top[best_move] += 1
		top[best_move+1] += 2
		top[best_move+2] += 1
		
		pyautogui.press('up', presses=2)
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	else: # 3 rotations
		top[best_move] += 1
		top[best_move+1] += 3
		
		pyautogui.press('up', presses=3)
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')

def placeGreenZ():
	# 0 rotations
	moves0 = {}
	if top[0] == top[1] == top[2] - 1:
		moves0[0] = (0, diff[2] - 1)
	
	for i in range(1, 7):
		if top[i] == top[i+1] == top[i+2] - 1:
			moves0[i] = (diff[i-1] + 1, diff[i+2] - 1)
	
	if top[7] == top[8] == top[9] - 1:
		moves0[7] = (diff[6] + 1, 0)
	
	# 1 rotation
	moves1 = {}
	if top[0] - 1 == top[1]:
		moves1[0] = (0, diff[1] - 2)
	
	for i in range(1, 8):
		if top[i] - 1 == top[i+1]:
			moves1[i] = (diff[i-1] + 2, diff[i+1] - 2)
	
	if top[8] - 1 == top[9]:
		moves1[8] = (diff[7] + 2, 0)
	
	# moves with no holes
	moves_no_holes = [moves0, moves1]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = []
	for i in moves_no_3[0]: # get moves that can reduce >=3 walls
		if i == 0:
			if diff[2] >= 3:
				moves0.append(i)
			break
		if i == 7:
			if diff[6] <= -3:
				moves0.append(i)
			break
		if diff[i + 2] >= 3 or diff[i - 1] <= -3:
			moves0.append(i)
	
	# 1 rotation
	moves1 = []
	for i in moves_no_3[1]:
		if i == 0:
			if diff[1] >= 3:
				moves1.append(i)
			break
		if i == 8:
			if diff[7] <= -3:
				moves1.append(i)
			break
		if diff[i + 1] >= 3 or diff[i - 1] <= -3:
			moves1.append(i)
	
	moves_reducing = [moves0, moves1]
	
	increase = [[1,2,1,0], [2,2,0,0]]
	if len(moves_no_3[0]) == 0 and len(moves_no_3[1]) == 0: # no moves create < 3 walls
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_holes, increase)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_reducing, increase)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_3, increase)
		else: # at least 1 move can reduce walls
			best_move, rot = bestMove(moves_reducing, increase)
	
	# 0 rotations
	if rot == 0:
		top[best_move] += 1
		top[best_move+1] += 2
		top[best_move+2] += 1
		
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	
	else: # 1 rotation
		top[best_move] += 2
		top[best_move+1] += 2
		
		pyautogui.press('up')
		if best_move < 4:
			pyautogui.press('left', presses=4-best_move)
		elif best_move > 4:
			pyautogui.press('right', presses=best_move-4)
		pyautogui.press('space')

def placeRedZ():
	# 0 rotations
	moves0 = {}
	if top[0] - 1 == top[1] == top[2]:
		moves0[0] = (0, diff[2] - 1)
	
	for i in range(1, 7):
		if top[i] - 1 == top[i+1] == top[i+2]:
			moves0[i] = (diff[i-1] + 1, diff[i+2] - 1)
	
	if top[7] - 1 == top[8] == top[9]:
		moves0[7] = (diff[6] + 1, 0)
	
	# 1 rotation
	moves1 = {}
	if top[0] == top[1] - 1:
		moves1[0] = (0, diff[1] - 2)
	
	for i in range(1, 8):
		if top[i] == top[i+1] - 1:
			moves1[i] = (diff[i-1] + 2, diff[i+1] - 2)
	
	if top[8] == top[9] - 1:
		moves1[8] = (diff[7] + 2, 0)
	
	# moves with no holes
	moves_no_holes = [moves0, moves1]
	
	moves_no_3 = filterMoves(moves_no_holes)
	
	if moves_no_3 == -1: # c pressed
		return
	
	# 0 rotations
	moves0 = []
	for i in moves_no_3[0]: # get moves that can reduce >=3 walls
		if i == 0:
			if diff[2] >= 3:
				moves0.append(i)
			break
		if i == 7:
			if diff[6] <= -3:
				moves0.append(i)
			break
		if diff[i + 2] >= 3 or diff[i - 1] <= -3:
			moves0.append(i)
	
	# 1 rotation
	moves1 = []
	for i in moves_no_3[1]:
		if i == 0:
			if diff[1] >= 3:
				moves1.append(i)
			break
		if i == 8:
			if diff[7] <= -3:
				moves1.append(i)
			break
		if diff[i + 1] >= 3 or diff[i - 1] <= -3:
			moves1.append(i)
	
	moves_reducing = [moves0, moves1]
	
	increase = [[1,2,1,0], [2,2,0,0]]
	if len(moves_no_3[0]) == 0 and len(moves_no_3[1]) == 0: # no moves create < 3 walls
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_holes, increase)
		else: # choose wall reduction that reults in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_reducing, increase)
	else: # at least 1 move in moves_no_3
		if len(moves0) == 0 and len(moves1) == 0: # no walls can be reduced, choose the move that results in sum of diffs being closest to 0
			best_move, rot = bestMove(moves_no_3, increase)
		else: # at least 1 move can reduce walls
			best_move, rot = bestMove(moves_reducing, increase)
	
	# 0 rotations
	if rot == 0:
		top[best_move] += 1
		top[best_move+1] += 2
		top[best_move+2] += 1
		
		if best_move < 3:
			pyautogui.press('left', presses=3-best_move)
		elif best_move > 3:
			pyautogui.press('right', presses=best_move-3)
		pyautogui.press('space')
	
	else: # 1 rotation
		top[best_move] += 2
		top[best_move+1] += 2
		
		pyautogui.press('up')
		if best_move < 4:
			pyautogui.press('left', presses=4-best_move)
		elif best_move > 4:
			pyautogui.press('right', presses=best_move-4)
		pyautogui.press('space')

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
