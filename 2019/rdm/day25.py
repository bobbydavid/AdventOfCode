from collections import deque
import sys
import copy
import intcode
import aoc

class CommandQueue:
  def __init__(self):
    self.commands = deque()
    self.buffer = deque()
    self.ran = deque()
    self.mute = False

  def get(self):
    while not self.buffer:
      self._buffer_next_command()
    return self.buffer.popleft()

  def _buffer_next_command(self):
    if self.commands:
      c = self.commands.popleft()
    else:
      c = raw_input()
    self.ran.append(c)
    if c == 'MUTE':
      self.mute = True
      print('<muted>')
    elif c == 'UNMUTE':
      self.mute = False
      print('<unmuted>')
    else:
      for x in c:
        self.buffer.append(ord(x))
      self.buffer.append(ord('\n'))

  def put(self, c):
    if not self.mute:
      sys.stdout.write(chr(c))


  def __repr__(self):
    s = 'CommandQueue'
    if self.ran:
      s += '\nExecuted: %s' % list(self.ran)
    if self.commands:
      s += '\nPending: %s' % list(self.ran)
    return s


 
BAD_THINGS = [
  'giant electromagnet', 'infinite loop', 'escape pod',
  'photons', 'molten lava']

def playground():
  q = CommandQueue()
  initial = []
  #initial = ['west', 'west', 'west']

  # Take all things and go to checkpoint.
  initial = ['MUTE', 'west', 'take cake', 'east', 'south', 'take coin', 'south', 'west', 'north', 'north', 'north', 'inv', 'drop cake', 'north', 'drop coin', 'north', 'take cake', 'take coin', 'north', 's', 'south', 'south', 'east', 'inv', 'north', 'east', 'take mouse', 'south', 'south', 'take hypercube', 'north', 'south', 'inv', 'north', 'north', 'west', 'north', 'north', 'south', 'west', 'west', 'take pointer', 'west', 'south', 'north', 'east', 'south', 'take monolith', 'north', 'south', 'north', 'west', 'south', 'inv', 'take tambourine', 'east', 'south', 'north', 'south', 'north', 'east', 'east', 'take mug', 'west', 'west', 'west', 'north', 'east', 'east', 'east', 'south', 'south', 'west', 'north', 'north', 'UNMUTE', 'north', 'inv']
  


  ITEMS = ['pointer', 'hypercube', 'cake', 'tambourine', 'monolith', 'mouse', 'coin', 'mug']

  def _append_recursive_tries(items, initial):
    if not items:
      initial.append('inv')
      initial.append('north')
      return
    this_item = items.pop()
    initial.append('take %s' % this_item)
    _append_recursive_tries(items, initial)
    initial.append('drop %s' % this_item)
    _append_recursive_tries(items, initial)
    items.append(this_item)
  _append_recursive_tries(list(ITEMS), initial)
      
      




  for c in initial:
    q.commands.append(c)

  try:
    computer = intcode.Computer('day25.data', q, q)
    computer.run()
  except KeyboardInterrupt, EOFError:
    pass

  print(q)


playground()

