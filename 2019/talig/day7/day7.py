import math
import sys
import operator
import copy
from functools import partial
import collections
import itertools
import threading
from Queue import Queue

TestAmp = collections.namedtuple('TestAmp', ['program', 'input', 'expected_output'])
Amp = collections.namedtuple('Amp', ['program' , 'input_queue', 'output_queue'])

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

def GetOp(op_num, inputs):
  # Inputs is a Queue.
  if op_num == 3:
    op = partial(OPS[op_num], inputs.get())
  else:
    op = OPS[op_num]
  return op

def ExecuteInstructions(input_array, inputs, outputs):
  # Inputs is a Queue.
  i = 0
  op_num = input_array[i] % 100
  output = None
  op = GetOp(op_num, inputs)
  while op and i < len(input_array):
    new_i, output = op(input_array, i, input_array[i]/100)
    if output != None:
      outputs.put(output)
    i = new_i
    op_num = input_array[i] % 100
    op = GetOp(op_num, inputs)
  return True

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

def FindNounAndVerb(input_array, target):
  for noun in xrange(100):
    for verb in xrange(100):
      a = RestoreAlarmState(input_array, noun, verb)
      a = ExecuteInstructions(a)
      if a[0] == target:
        return noun, verb
  return None, None

def ChainQueues():
  amp_queues = [0] * 5 # Note the size here...
  amp_queues[4] = [Queue(), Queue()]
  for i in range(3, -1, -1):
    # Set queues for Amp #i to be a new input queue, and the next amp's input as output.
    amp_queues[i] = [Queue(), amp_queues[i+1][0]]
  # Set the input to A to be the output of E.
  amp_queues[0] = [amp_queues[4][1], amp_queues[0][1]]
  return amp_queues

def RunAmplifiers(program, inputs):
  amp_queues = ChainQueues()
  amps = dict((k, Amp(copy.deepcopy(program), amp_queues[k][0], amp_queues[k][1])) for k in range(5))
  for i in range(5): # Set the phase
    amps[i].input_queue.put(inputs[i])
  amps[0].input_queue.put(0) # For the first AMP, second input is 0.
  for i in range(5): # This is easier that A-E.
    ExecuteInstructions(amps[i].program, amps[i].input_queue, amps[i%5].output_queue)
  return amps[4].output_queue.get()

def RunAmplifiersFeedback(program, inputs):
  amp_queues = ChainQueues()
  amps = dict((k, Amp(copy.deepcopy(program), amp_queues[k][0], amp_queues[k][1])) for k in range(5))
  for i in range(5): # Set the phase
    amps[i].input_queue.put(inputs[i])
  amps[0].input_queue.put(0) # For the first AMP, second input is 0.
  threads = []
  for i in range(5): # This is easier that A-E.
    x = threading.Thread(target=ExecuteInstructions, 
                         args=(amps[i].program, 
                               amps[i].input_queue, 
                               amps[i%5].output_queue))
    threads.append(x)
    x.start()
    
  for i, thread in enumerate(threads):
    #print 'Looking at AMP ', chr(ord('A')+i)
    thread.join()
    #print 'Done'

  return amps[4].output_queue.get()

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

def TestAmplifiers():
  tests = [
          TestAmp([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0], 43210),
          TestAmp([3,23,3,24,1002,24,10,24,1002,23,-1,23,
                   101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4], 54321),
          TestAmp([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                   1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1, 0, 4, 3, 2], 65210),
          ]
  for test in tests:
    output = RunAmplifiers(test.program, test.input)
    if output == test.expected_output:
      print 'Pass'
    else:
      print 'Nope. Expected: ', test.expected_output, ' Received: ', output

def TestAmplifiersFeedback():
  tests = [
          TestAmp([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                   27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5], 139629729), 
          TestAmp([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                   -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                   53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6], 18216)
          ]
          
  for test in tests:
    output = RunAmplifiersFeedback(test.program, test.input)
    if output == test.expected_output:
      print 'Pass'
    else:
      print 'Nope. Expected: ', test.expected_output, ' Received: ', output


def Test():
  print 'Testing: '
  TestAmplifiers()
  print 'Testing with feedback: '
  TestAmplifiersFeedback()
  print '\n\n\n\n', '*'*30, '\n'

def Run(permute, func, content):
  max_output = 0
  max_setting = []
  for inp in itertools.permutations(permute):
    output = func(content, inp)
    if output > max_output:
      max_output = output
      max_setting = inp
  
  print func.func_name, ' ==> Max Output: ', max_output, ' with Setting: ', max_setting

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
  Run(range(5), RunAmplifiers, content)
  # (b)
  Run(range(5,10), RunAmplifiersFeedback, content)
  
if __name__== "__main__":
  main()
