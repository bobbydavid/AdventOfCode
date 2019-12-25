import sys
from collections import deque
from computer import Computer
from os import system
from itertools import chain, combinations

class IOQueue:
  def __init__(self):
    self.buffer = deque()

  def get(self):
    while not self.buffer:
      command = raw_input('')
      self.add_command(command)
    return self.buffer.popleft()

  def put(self, c):
    sys.stdout.write(chr(c))

  def add_command(self, command):
    command += '\n'
    self.buffer.extend([ord(c) for c in command])
  
# (a) ==> 10504192
def pick_up_all_things_and_go_to_security():
  return ['east','take weather machine', 'west', 'west', 'west', 'take bowl of rice',
          'east', 'north', 'take polygon', 'east', 'take hypercube', 'south', 'take dark matter',
          'north', 'west', 'north', 'take candy cane', 'west', 'north', 'take manifold',
          'south', 'west', 'north', 'take dehydrated water', 'west']

def drop_all(items):
  commands = []
  for i in items:
    commands.append('drop ' + i)
  return commands

def take_all(items):
  commands = []
  for i in items:
    commands.append('take ' + i)
  return commands

def powerset(iterable):
  s = iterable
  return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def run_commands(commands, queue):
  for command in commands:
    queue.add_command(command)

def find_combo(queue):
  inventory = ['weather machine',
               'bowl of rice',
               'candy cane',
               'manifold',
               'dehydrated water',
               'hypercube', 
               'polygon',
               'dark matter']
  # We start with everything.
  # Answer was: bowl of rice, candy cane, dehydrated water, dark matter.
  run_commands(drop_all(inventory), queue)
  options = powerset(inventory)
  for o in options:
    commands = take_all(o)
    commands.append('south')
    run_commands(commands, queue)
    run_commands(drop_all(o), queue)

def main():
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  intcode = [int(x) for x in f.read().split(',')]
  f.close()
  
  computer = Computer(intcode, IOQueue(), IOQueue())
  _ = system('clear')
  computer.start()
  run_commands(pick_up_all_things_and_go_to_security(), computer.InputQueue())
  find_combo(computer.InputQueue())
 
if __name__== "__main__":
  main()
