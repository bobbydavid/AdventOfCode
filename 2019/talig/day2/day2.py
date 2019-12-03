import math
import sys
import operator
import copy

OPS = {1: operator.add, 2: operator.mul}

def ExecuteInstructions(input_array):
  i = 0
  while (input_array[i] != 99 and i < len(input_array) - 4): 
    x = input_array[input_array[i+1]]
    y = input_array[input_array[i+2]]
    result = OPS[input_array[i]](x,y) 
    input_array[input_array[i+3]] = result
    i += 4
  return input_array

# Once you have a working computer, the first step is to restore the
# gravity assist program (your puzzle input) to the "1202 program alarm"
# state it had just before the last computer caught fire. To do this,
# before running the program, replace position 1 with the value 12 and
# replace position 2 with the value 2.
def RestoreAlarmState(input_array, noun, verb):
  a = copy.deepcopy(input_array)
  a[1] = noun
  a[2] = verb
  return a

def TestComputer():
  tests = (
      ([1,0,0,0,99], [2,0,0,0,99]),
      ([2,3,0,3,99], [2,3,0,6,99]),
      ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
      ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
      )
  for test in tests:
    print "Testing on input ", test
    result = ExecuteInstructions(test[0])
    if not result == test[1]:
      print result
    else:
      print 'Pass'

def TestReset():
  b = [1,2,3,4]
  c = RestoreAlarmState(b, 12, 2)
  print c[1] == 12
  print c[2] == 2

def FindNounAndVerb(input_array, target):
  for noun in xrange(100):
    for verb in xrange(100):
      a = RestoreAlarmState(input_array, noun, verb)
      a = ExecuteInstructions(a)
      if a[0] == target:
        return noun, verb
  return None, None

def main():
  #print 'Testing: '
  #TestComputer()
  #print 'Testing reset state: '
  #TestReset()
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  content = [int(x) for x in f.read().split(',')]
  f.close()
  
  if (len(sys.argv) == 3):
    # (b)
    print 'Looking for noun and verb to get target: ', sys.argv[2]
    noun, verb = FindNounAndVerb(content, int(sys.argv[2]))
    print 'Noun: ', noun, 'Verb: ', verb
    print 'Result: ', 100 * noun + verb
  else: 
    # (a)
    RestoreAlarmState(content, 12, 2)
    new_content = ExecuteInstructions(content)
    print 'Value in position 0: ', new_content[0]
  
if __name__== "__main__":
  main()
