import sys

DIRECTION = {
							'U': (-1, 0),
							'D': (1, 0), 
							'R': (0, 1),
							'L': (0, -1)
						 }

def GetBounds(current_location, bounds):
	if current_location[1] > bounds['R']:
		bounds['R'] = current_location[1]
	if current_location[1] < bounds['L']:
		bounds['L'] = current_location[1]
	if current_location[0] > bounds['D']:
		bounds['D'] = current_location[0]
	if current_location[0] < bounds['U']:
		bounds['U'] = current_location[0]


def ConvertToTuple(wire):
	moves = []
	bounds = {'R': 0, 'L':0, 'U':0, 'D':0}
	current_location = [0,0]
	for section in wire:
		# Ignore the direction for this
		steps = int(section[1:])
		moves.extend([DIRECTION[section[0]]] * steps)
		move = tuple([x * steps for x in DIRECTION[section[0]]])
		current_location = [sum(x) for x in zip(move, current_location)]
		GetBounds(current_location, bounds)
	return moves, bounds

def MakeBoard(b1, b2):
	max_bounds = dict([(k,max(abs(b1[k]), abs(b2[k]))) for k in b1.keys()])
	board = [['.'] * (max_bounds['R'] + max_bounds['L'] + 1)]
	for i in xrange(max_bounds['U'] + max_bounds['D'] + 1):
		board.append(['.'] * (max_bounds['R'] + max_bounds['L'] + 1))
	return board, max_bounds

def GetSymbol(move, current, w):
	if current != 'o' and current != w and current != '.':
		return 'X'
	else:
		return w

def DrawWire(wire, board, shift, w, crossings):
	shifted = shift
	for move in wire:
		shifted = [sum(x) for x in zip(move, shifted)] 
		symbol =	GetSymbol(move, board[shifted[0]][shifted[1]], w)
		board[shifted[0]][shifted[1]] = symbol
		if symbol == 'X':
			crossings.append(shifted)

def PrintBoard(board):
	for i in reversed(range(len(board))):
		print ''.join(board[i])

def MinStepsToCrossing(wire, shift, crossing):
	current_location = shift
	length = 0
	for w in wire:
		current_location = tuple([sum(x) for x in zip(current_location, w)])
		length += 1
		if current_location == crossing:
			break
	return length

def FindManhattanCrossing(wire1, wire2, board, shift, crossings):
	min_distance = sys.maxint
	min_cross = shift
	for j, i in crossings:
		distance = abs(i - shift[1]) + abs(j-shift[0])
		if min_distance > distance:
			min_distance = distance
			min_cross = (j,i)
	return min_distance, min_cross

def FindMinStepsCrossing(wire1, wire2, board, shift, crossings):
	min_length = sys.maxint
	min_cross = shift
	for j, i in crossings:
		steps = MinStepsToCrossing(wire1, shift, (j, i)) + MinStepsToCrossing(wire2, shift, (j, i))
		if steps < min_length:
			min_length = steps
			min_cross = (j, i)
	return min_length, min_cross

def DoEverything(line1, line2):
	wire1, bounds1 = ConvertToTuple(line1.split(','))
	print bounds1
	wire2, bounds2 = ConvertToTuple(line2.split(','))
	print bounds2
	board, max_bounds = MakeBoard(bounds1, bounds2)
	shift = (max_bounds['U'], max_bounds['L'])
	board[shift[0]][shift[1]] = 'o'
	crossings = []
	DrawWire(wire1, board, shift, '1', crossings)
	DrawWire(wire2, board, shift, '2', crossings)
	#PrintBoard(board)
	#return FindManhattanCrossing(wire1, wire2, board, shift, crossings)
	return FindMinStepsCrossing(wire1, wire2, board, shift, crossings)

def TestFindCrossing():
	tests = (
			('R75,D30,R83,U83,L12,D49,R71,U7,L72',
			 'U62,R66,U55,R34,D71,R55,D58,R83', 610),
			('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
			 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 410)
			)
	for test in tests:
		print "Testing on input ", test
		d, point = DoEverything(test[0], test[1])
		if not d == test[2]:
			print 'Nope! d: ', d, ' point:', point
		else:
			print 'Pass'


def main():
	print 'Testing: '
	TestFindCrossing()
	if (len(sys.argv) < 2):
		print 'Missing data file!'
		print 'Usage: python [script] [data]'
		sys.exit(1)

	f = open(sys.argv[1])
	content = f.readlines()
	f.close()
	
	d, point = DoEverything(content[0], content[1])
	print 'D: ', d, ' point: ', point
	
if __name__== "__main__":
	main()
