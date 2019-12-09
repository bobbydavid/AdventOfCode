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

# Modes
POSITION = 0
DIRECT = 1
RELATIVE = 2

class Computer(threading.Thread):
  def __init__(self, program, input_queue, output_queue,group=None, target=None, name=None,
               args=(), kwargs=None, verbose=None):
    super(Computer,self).__init__(group=group, target=target, 
                    name=name, verbose=verbose)
    self.program = copy.deepcopy(program)
    self.program.extend([0]*1000)
    # Queueus
    self.input_queue = input_queue
    self.output_queue = output_queue
    # Base
    self.relative_base = 0
    # Operations Map
    self.OPS = {1: partial(self.MathOps, operator.add),
                2: partial(self.MathOps, operator.mul),
                3: self.StoreInput,
                4: self.Output,
                5: self.JumpIfTrue,
                6: self.JumpIfFalse, 
                7: partial(self.MathOps, operator.lt),
                8: partial(self.MathOps, operator.eq),
                9: self.AdjustRelativeBase,
                99: None}

  def SetOuputQueue(self, queue):
    self.output_queue = output_queue

  def InputQueue(self):
    return self.input_queue
  
  def OutputQueue(self):
    return self.output_queue

  def GetParamIndex(self, i, mode):
    index = 0
    if mode == POSITION:
      index = self.program[i]
    if mode == DIRECT:
      index = i
    if mode == RELATIVE:
      index = self.relative_base + self.program[i]
    return index

  def SetParam(self, i, value, mode):
    self.program[self.GetParamIndex(i, mode)] = value

  def GetParam(self, i, mode):
    return self.program[self.GetParamIndex(i, mode)]

  def MathOps(self, operator, i, mode):
    x = self.GetParam(i+1, mode % 10)
    mode = mode / 10 
    y = self.GetParam(i+2, mode % 10)
    mode = mode / 10 
    result = operator(x,y) 
    self.SetParam(i+3, result, mode % 10)
    return i + 4, None

  def StoreInput(self, var, i, mode):
    self.SetParam(i+1, var, mode)
    return i + 2, None

  def Output(self, i, mode):
    return i + 2, self.GetParam(i + 1, mode % 10)

  def JumpIfTrue(self, i, mode):
    if not self.GetParam(i+1, mode % 10) == 0:
      mode = mode / 10
      return self.GetParam(i+2, mode % 10), None
    else:
      return i+3, None

  def JumpIfFalse(self, i, mode):
    if self.GetParam(i+1, mode % 10) == 0:
      mode = mode / 10
      return self.GetParam(i+2, mode % 10), None
    else:
      return i+3, None
  
  def AdjustRelativeBase(self, i, mode):
    self.relative_base += self.GetParam(i + 1, mode % 10)
    return i + 2, None

  def GetOp(self, op_num):
    # Inputs is a Queue.
    if op_num == 3:
      op = partial(self.OPS[op_num], self.input_queue.get())
    else:
      op = self.OPS[op_num]
    return op

  # Was ExecuteInstruction
  def run(self):
    i = 0
    op_num = self.program[i] % 100
    output = None
    op = self.GetOp(op_num)
    while op and i < len(self.program):
      new_i, output = op(i, self.program[i]/100)
      if output != None:
        self.output_queue.put(output)
      i = new_i
      op_num = self.program[i] % 100
      op = self.GetOp(op_num)
    return True

  # Once you have a working computer, the first step is to restore the
  # gravity assist program (your puzzle input) to the "1202 program alarm"
  # state it had just before the last computer caught fire. To do this,
  # before running the program, replace position 1 with the value 12 and
  # replace position 2 with the value 2.
  def RestoreAlarmState(self, noun, verb):
    a = copy.deepcopy(self.program)
    a[1] = noun
    a[2] = verb
    return a

  def FindNounAndVerb(self, target):
    for noun in xrange(100):
      for verb in xrange(100):
        a = self.RestoreAlarmState(self, noun, verb)
        self.ExecuteInstructions()
        if self.program[0] == target:
          return noun, verb
    return None, None

# END OF COMPUTER CLASS.

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
  amps = dict((k, Computer(program, amp_queues[k][0], amp_queues[k][1])) for k in range(5))
  for i in range(5): # Set the phase
    amps[i].input_queue.put(inputs[i])
  amps[0].input_queue.put(0) # For the first AMP, second input is 0.
  for i in range(5): # This is easier that A-E.
    amps[i].run()
  return amps[4].OutputQueue().get()

def RunAmplifiersFeedback(program, inputs):
  amp_queues = ChainQueues()
  # Computer extends Thread.
  amps = dict((k, Computer(program, amp_queues[k][0], amp_queues[k][1])) for k in range(5))
  for i in range(5): # Set the phase
    amps[i].input_queue.put(inputs[i])
  amps[0].input_queue.put(0) # For the first AMP, second input is 0.
  threads = []
  for i in range(5): # This is easier that A-E.
    x = amps[i]
    threads.append(x)
    x.start()
    
  for i, thread in enumerate(threads):
    #print 'Looking at AMP ', chr(ord('A')+i)
    thread.join()
    #print 'Done'

  return amps[4].output_queue.get()

def TestReset():
  b = [1,2,3,4]
  c = RestoreAlarmState(b, 12, 2)
  print c[1] == 12
  print c[2] == 2
     
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

def TestBoostCopy():
  c = Computer([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], Queue(), Queue())
  c.start()
  c.join()
  queue = c.OutputQueue()
  res = []
  while queue.qsize() > 0:
    res.append(queue.get())

  print res
  #print c.program
  print [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

def TestOutputLargeNumber():
  c = Computer([104,1125899906842624,99], Queue(), Queue())
  c.start()
  c.join()
  queue = c.OutputQueue()
  assert queue.get() == 1125899906842624


def Test16Digit():
  c = Computer([1102,34915192,34915192,7,4,7,99,0], Queue(), Queue())
  c.start()
  c.join()
  res = c.OutputQueue().get()
  assert len(str(res)) == 16
  print 'Result: ', res

def Test():
  print 'Testing: '
  TestBoostCopy()
  Test16Digit()
  TestOutputLargeNumber()
  print '\n\n\n\n', '*'*30, '\n'

def RunPermutations(permute, func, content):
  max_output = 0
  max_setting = []
  for inp in itertools.permutations(permute):
    output = func(content, inp)
    if output > max_output:
      max_output = output
      max_setting = inp
  
  print func.func_name, ' ==> Max Output: ', max_output, ' with Setting: ', max_setting

def RunComputer(content, initial_value):
  c = Computer(content, Queue(), Queue())
  c.InputQueue().put(initial_value)
  c.start()
  c.join()
  return c.OutputQueue().get()
  

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
  # Run in test mode: 1, output: 3507134798
  print 'BOOST CODE: ', RunComputer(content, 1)
  # (b)
  # Run in boost mode: 2, output: 84513
  print 'Distress signal: ', RunComputer(content, 2)

  
if __name__== "__main__":
  main()
