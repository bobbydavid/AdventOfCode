from collections import defaultdict
from collections import deque
import curses
import copy
import itertools
import sys
import threading

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  content = content_file.read()
  orig_tape = [int(x) for x in content.split(',') if x]


# IntOp computer.
#
# Read from input_queue using get()
# Write to output_queue using put(x)
def compute(tape, input_queue, output_queue):
  tape = defaultdict(int, enumerate(tape))
  i = 0
  relative_base = 0
  while True:
    instruction = tape[i]
    # print('# instruction=%d' % instruction)

    def get_mode(i, n):
      mode = instruction // 100
      # Find the Nth digit, counting right to left.
      for x in range(n):
        mode //= 10
      mode %= 10
      return mode

    def read_arg(i, n):
      mode = get_mode(i, n)
      index = i + 1 + n
      # print('# read_arg(%d, %d): mode=%d' % (i, n, mode))
      if mode == 0:
        result = tape[tape[index]]  # The number it points to.
      elif mode == 1:
        result = tape[index]  # The number itself.
      elif mode == 2:
        result = tape[relative_base + tape[index]]  # Points to + offset
      else:
        raise Exception('bad read mode %d' % mode)
      # print('# read_arg(%d, %d): result=%d' % (i, n, result))
      return result

    def write_arg(i, n, data):
      mode = get_mode(i, n)
      index = i + 1 + n
      if mode == 0:
        tape[tape[index]] = data
      elif mode == 2:
        tape[relative_base + tape[index]] = data
      else:
        raise Exception('bad write mode %d' % mode)

    op = instruction % 100
    jmp = -1  # -1 means "do not jump"

    if op == 1:  # ADD
      arg_count = 3
      arg1 = read_arg(i, 0)
      arg2 = read_arg(i, 1)
      write_arg(i, 2, arg1 + arg2)
    elif op == 2:  # MUL
      arg_count = 3
      arg1 = read_arg(i, 0)
      arg2 = read_arg(i, 1)
      write_arg(i, 2, arg1 * arg2)
    elif op == 3:  # WRITE FROM INPUT
      arg_count = 1
      write_arg(i, 0, input_queue.get())
    elif op == 4:  # OUTPUT
      arg_count = 1
      output_queue.put(read_arg(i, 0))
    elif op == 5:  # JUMP IF TRUE
      arg_count = 2
      if read_arg(i, 0) != 0:
        jmp = read_arg(i, 1)
    elif op == 6:  # JUMP IF FALSE
      arg_count = 2
      if read_arg(i, 0) == 0:
        jmp = read_arg(i, 1)
    elif op == 7:  # LESS THAN
      arg_count = 3
      result = 0
      if read_arg(i, 0) < read_arg(i, 1):
        result = 1
      write_arg(i, 2, result)
    elif op == 8:  # EQUALS
      arg_count = 3
      result = 0
      if read_arg(i, 0) == read_arg(i, 1):
        result = 1
      write_arg(i, 2, result)
    elif op == 9:
      arg_count = 1
      relative_base += read_arg(i, 0)
    elif op == 99:
      return
    else:
      raise Exception('unknown op %s' % op)
    ints_to_skip = 1 + arg_count
    assert i + ints_to_skip < len(tape), 'i=%d, skip=%d, len=%d' % (i, ints_to_skip, len(tape))

    #dbg_string = 'DBG: %d' % (instruction,)
    #dbg_string += ''.join([' ' + str(tape[i + 1 + x]) for x in range(arg_count)])
    # print(dbg_string)

    if jmp == -1:
      i += ints_to_skip
    else:
      i = jmp


# Queue that allows for simple read/writes.
class SimpleQueue:
  def __init__(self, values = []):
    self.q = deque(values)

  def get(self):
    self.q.popleft()

  def put(self, x):
    self.q.append(x)





class Player():
  def __init__(self):
    self.ball_x = None
    self.paddle_x = None
    self.score = None
    self.buffer = []
    # A set of (x,y) of known blocks.
    self.blocks = set()

  def put(self, v):
    self.buffer.append(v)
    if len(self.buffer) == 3:
      self.view(self.buffer[0], self.buffer[1], self.buffer[2])
      self.buffer = []

  def view(self, x, y, tile):
    if x == -1 and y == 0:  # SCORE
      self.score = tile
      return
    # Track the blocks we know about.
    if tile == 2:
      self.blocks.add((x,y))
    else:
      self.blocks.discard((x,y))
    # Track coords.
    if tile == 3:  # PADDLE
      self.paddle_x = x
    if tile == 4:  # BALL
      self.ball_x = x

  def get(self):
    if self.score is not None and len(self.blocks) == 0:
      print('no blocks, score=%d' % self.score)
    if self.ball_x is None or self.paddle_x is None:
      print('not sure where ball/paddle')
      return 0
    delta = self.ball_x - self.paddle_x
    if delta > 0:
      return 1
    elif delta < 0:
      return  -1
    else:
      return 0
"""
try:
  scr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  scr.clear()

finally:
  curses.nocbreak()
  scr.keypad(False)
  curses.echo()
  curses.endwin()
"""


orig_tape[0] = 2
player = Player()
compute(orig_tape, player, player)
print('final score: %d' % player.score)

