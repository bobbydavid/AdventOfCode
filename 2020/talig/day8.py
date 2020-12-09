# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re
import collections
import copy

DAY = 8
Instruction = collections.namedtuple('Instruction', ['instruction', 'value'])

class Computer():
  def __init__(self, instructions):
    self.accumulator = 0
    self.instruction_counter = 0
    self.instructions = []
    for i in instructions:
      instruction, value = i.split()
      self.instructions.append(Instruction(instruction, int(value)))

  def jmp(self, delta):
    self.instruction_counter += delta
  
  def acc(self, delta):
    self.accumulator += delta
    self.instruction_counter += 1

  def reset(self):
    self.accumulator = 0
    self.instruction_counter = 0

  def getLength(self):
    return len(self.instructions)

  def updateInstruction(self, index, instruction):
    self.instructions[index] = instruction
  
  def getAcc(self):
    return self.accumulator

  def getInstructionCounter(self):
    return self.instruction_counter

  def getInstruction(self, index=None):
    if index is None:
      index = self.instruction_counter
    return self.instructions[index]
  
  def execute(self):
    current = self.instructions[self.instruction_counter]
    if current.instruction == 'jmp':
      self.jmp(current.value)
    elif current.instruction == 'acc':
      self.acc(current.value)
    else: # nop
      self.instruction_counter += 1
    return

  def run(self):
    while self.instruction_counter < self.getLength():
      self.execute()

def FindLoop(computer):
  visited = {}
  instruction_counter = computer.getInstructionCounter() 
  while instruction_counter not in visited and instruction_counter < computer.getLength():
    visited[instruction_counter] = True
    computer.execute()
    instruction_counter = computer.getInstructionCounter()
  # We are now in the state "right before executing the same instruction the second time". 
  return visited
  
def SwitchInstruction(computer, index):
  inst = computer.getInstruction(index)
  if inst.instruction == 'acc':
    return False
  if inst.instruction == 'jmp':
    computer.updateInstruction(index, Instruction('nop', inst.value))
  elif inst.instruction == 'nop':
    computer.updateInstruction(index, Instruction('jmp', inst.value))
  return True
  

def BreakLoop(computer):
  last_updated = 0
  last_inst = computer.getLength()
  for i in range(last_inst):
    if (SwitchInstruction(computer, i)):
      visited = FindLoop(computer)
      if last_inst - 1 in visited:
        print('Switched instruction', i, computer.getInstruction(i))
        return computer.getAcc()
      else:
        # Undo the change
        SwitchInstruction(computer, i)
        computer.reset()


def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]
  computer = Computer(lines)
  
  print('Day', DAY, ' part 1')
  _ = FindLoop(computer)
  print('The accumulator value right before the loop restarts is', computer.getAcc())

  computer.reset() 
  # Brute force way of doing this is chaning a nop to a jmp and a jmp to a nop, one at a time. 

  print('Day', DAY, ' part 2')
  print('Accumulator value:', BreakLoop(computer))
  # Verifying :)
  computer.reset()
  computer.run()
  print('It works!')
  

if __name__== '__main__':
  main()
