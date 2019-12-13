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
  def __init__(self, values = []):
    self.q = deque(values)

  def get(self):
    self.q.popleft()

  def put(self, x):
    self.q.append(x)

in_q = SimpleQueue()
out_q = SimpleQueue()
compute(orig_tape, in_q, out_q)

max_x = 0
max_y = 0
out_data = list(out_q.q)
tiles = {}
for i in range(0, len(out_data), 3):
  max_x = max(max_x, out_data[i])
  max_y = max(max_y, out_data[i + 1])
  tiles[(out_data[i], out_data[i + 1])] = out_data[i + 2]


bcount = 0
for y in range(max_y + 1):
  for x in range(max_x + 1):
    c = ' ' 
    if (x, y) in tiles:
      i = tiles[(x, y)]
      if i == 0:
        c = '.'
      elif i == 1:
        c = 'X'
      elif i == 2:
        bcount += 1
        c = '+'
      elif i == 3:
        c = '-'
      elif i == 4:
        c = '*'
      else:
        raise Exception(' unknown tile %d' % i)
    sys.stdout.write(c)
  sys.stdout.write('\n')
    


print(bcount)
