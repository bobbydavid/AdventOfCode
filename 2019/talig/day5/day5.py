import math
import sys
import operator
import copy
from functools import partial

def GetParam(input_array, i, mode):
  if mode == 0:
    return input_array[input_array[i]]
  if mode == 1:
    return input_array[i]

def SetParam(input_array, i, value):
  input_array[input_array[i]] = value

def MathOps(operator, input_array, i, mode):
  x = GetParam(input_array, i+1, mode % 10)
  mode = mode / 10 
  y = GetParam(input_array, i+2, mode % 10)
  mode = mode / 10 
  result = operator(x,y) 
  SetParam(input_array, i+3, result)
  return i + 4, None

def StoreInput(var, input_array, i, _):
  SetParam(input_array, i+1, var)
  return i + 2, None

def Output(input_array, i, mode):
  return i + 2, GetParam(input_array, i+1, mode % 10)

def JumpIfTrue(input_array, i, mode):
  if not GetParam(input_array, i+1, mode % 10) == 0:
    mode = mode / 10
    return GetParam(input_array, i+2, mode % 10), None
  else:
    return i+3, None

def JumpIfFalse(input_array, i, mode):
  if GetParam(input_array, i+1, mode % 10) == 0:
    mode = mode / 10
    return GetParam(input_array, i+2, mode % 10), None
  else:
    return i+3, None

OPS = {1: partial(MathOps, operator.add),
       2: partial(MathOps, operator.mul),
       3: StoreInput,
       4: Output,
       5: JumpIfTrue,
       6: JumpIfFalse, 
       7: partial(MathOps, operator.lt),
       8: partial(MathOps, operator.eq),
       99: None}

def ExecuteInstructions(input_array, val):
  i = 0
  op_num = input_array[i] % 100
  if op_num == 3:
    op = partial(OPS[op_num], val)
  else:
    op = OPS[op_num]
  while op and i < len(input_array):
    new_i, output = op(input_array, i, input_array[i]/100)
    if output != None:
      print 'Output for instruction ', i, ' :', output
    i = new_i
    op_num = input_array[i] % 100
    op = OPS[op_num]
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
      ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
      ([1002,4,3,4,33], [1002,4,3,4,99]),
      )
  for test in tests:
    print 'Testing on input ', test
    result = ExecuteInstructions(test[0], 0)
    if not result == test[1]:
      print result
    else:
      print 'Pass'

def TestReset():
  b = [1,2,3,4]
  c = RestoreAlarmState(b, 12, 2)
  print c[1] == 12
  print c[2] == 2

def TestWithInput(var):
  tests = (
        ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], var),
        ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], var))
  for test in tests:
    print 'Testing on input ', test
    print 'Expect ', 1 if var > 0 else 0
    result = ExecuteInstructions(test[0], var)
     
def TestLarge():
  program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
  print 'Expect 999:'
  ExecuteInstructions(program, 7)
  print 'Expect 1000:'
  ExecuteInstructions(program, 8)
  print 'Expect 1001:'
  ExecuteInstructions(program, 9)

def FindNounAndVerb(input_array, target):
  for noun in xrange(100):
    for verb in xrange(100):
      a = RestoreAlarmState(input_array, noun, verb)
      a = ExecuteInstructions(a)
      if a[0] == target:
        return noun, verb
  return None, None

def Test():
  #TestComputer()
  #print 'Testing reset state: '
  #TestReset()
  print 'Testing: '
  TestWithInput(0)
  TestWithInput(7)
  TestLarge()
  print '\n\n\n\n', '*'*30, '\n'

def main():
  Test()
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  content = [int(x) for x in f.read().split(',')]
  f.close()
  
  # (a)
  new_content = ExecuteInstructions(copy.deepcopy(content), 1)
  # WAS: 3122865

  # (b)
  new_content = ExecuteInstructions(copy.deepcopy(content), 5)
  # Was: 773660
  
if __name__== "__main__":
  main()
