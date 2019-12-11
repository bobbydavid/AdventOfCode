from collections import defaultdict
from collections import deque
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
  def __init__(values = []):
    self.q = deque(values)

  def get(self):
    self.q.popleft()

  def put(self, x):
    self.q.append(x)


class Spaceship:
  # Direction in clockwise order.
  DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

  # Colors
  BLACK = 0
  WHITE = 1

  # Modes
  PAINT = 0
  TURN = 1
  MODE_COUNT = 2
  
  def __init__(self):
    # Location is (x, y) == (across, up)
    self.robot_location = (0, 0)
    # Index into the DIRECTIONS array.
    self.robot_direction_index = 0
    # Map from (x,y) to color.
    self.hull_color = {}
    self.mode = self.PAINT


  # Allows the IntOps computer to read the current color.
  def get(self):
    if self.robot_location not in self.hull_color:
      color = self.BLACK
    else:
      color = self.hull_color[self.robot_location]
    #print('# read color=%d at %s' % (color, self.robot_location))
    return color


  # Receives the next instruction.
  def put(self, x):
    if (self.mode == self.PAINT):
      assert x == self.WHITE or x == self.BLACK, ('unexpected color %d' % x)
      self.hull_color[self.robot_location] = x
    elif (self.mode == self.TURN):
      if x == 0:
        self.robot_direction_index -= 1
      elif x == 1:
        self.robot_direction_index += 1
      else:
        raise Exception('unexpected turn direction %d' % x)
      self.robot_direction_index %= len(self.DIRECTIONS)
      delta = self.DIRECTIONS[self.robot_direction_index]
      self.robot_location = (self.robot_location[0] + delta[0], self.robot_location[1] + delta[1])
    else:
      raise Exception('unexpected mode %d' % self.mode)
    self.mode += 1
    self.mode %= self.MODE_COUNT


# Part A
ship = Spaceship()
_ = compute(orig_tape, ship, ship)
print('%d painted hull tiles' % len(ship.hull_color))

