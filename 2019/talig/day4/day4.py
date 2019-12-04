import sys

def NonDecreasing(password):
	for i in range(len(password)-1):
		if password[i] > password[i+1]:
			return False
	return True

def HasDouble(password):
	has_double = False
	i = 0
	while i < len(password):
		count = 1
		j = i + 1
		while j<len(password) and password[j] == password[i]:
			count += 1
			j += 1
		has_double = has_double or count == 2
		i = j
	return has_double

def LegalPassword(password):
	return len(password) == 6 and NonDecreasing(password) and HasDouble(password)
		

def Test():
	tests = ((111122, True), (112222, True), (223450, False), (123789, False), (123444, False), (112233, True)
			)
	for test in tests:
		print "Testing on input ", test
		res = LegalPassword(str(test[0]))
		if res != test[1]:
			print 'Nope! res: ', res, ' password:', test[0]
		else:
			print 'Pass'


def main():
	print 'Testing: '
	Test()
	if (len(sys.argv) < 2):
		print 'Missing data file!'
		print 'Usage: python [script] [data]'
		sys.exit(1)

	input_range = sys.argv[1].split('-')
	start = int(input_range[0])
	end = int(input_range[1])

	current = start
	legal_passwords = 0
	while current < end:
		if LegalPassword(str(current)):
			legal_passwords += 1
		current += 1
	
	print 'Legal passwords: ', legal_passwords
	
	
if __name__== "__main__":
	main()
