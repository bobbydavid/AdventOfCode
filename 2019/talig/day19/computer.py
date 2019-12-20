import math
import sys
import operator
import copy
from functools import partial
import collections
import itertools
import threading
from Queue import Queue

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
    self.program.extend([0]*2000)
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
