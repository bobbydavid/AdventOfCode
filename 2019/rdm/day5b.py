import copy
import sys

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print 'Data file: ' + filename
with open(filename, 'r') as content_file:
  content = content_file.read()
  orig_tape = [int(x) for x in content.split(',') if x]

print(orig_tape)


def calc(tape, input_data, output_data):
  i = 0
  while True:
    if output_data and output_data[-1] != 0:
      print 'Output was non-zero and failed.'
      return

    instruction = tape[i]

    def get_mode(i, n):
      mode = instruction / 100
      # Find the Nth digit, counting right to left.
      for x in range(n):
        mode /= 10
      print 'arg#=%d, mode=%d' % (n, mode)
      return mode % 10

    def read_arg(i, n):
      mode = get_mode(i, n)
      index = i + 1 + n
      if mode == 0:
        result = tape[tape[index]]  # The number it points to.
      elif mode == 1:
        result = tape[index]  # The number itself.
      else:
        raise Exception('bad read mode %d' % mode)
      print 'read arg#%d = %d' % (n, result)
      return result

    def write_arg(i, n, data):
      mode = get_mode(i, n)
      index = i + 1 + n
      if mode == 0:
        print 'write %d at %d' % (data, tape[index])
        tape[tape[index]] = data
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
      write_arg(i, 0, input_data.pop())
    elif op == 4:  # OUTPUT
      arg_count = 1
      output_data.append(read_arg(i, 0))
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
    elif op == 99:
      return
    else:
      raise Exception('unknown op %s' % op)
    ints_to_skip = 1 + arg_count
    assert i + ints_to_skip < len(tape), 'i=%d, skip=%d, len=%d' % (i, ints_to_skip, len(tape))
    print([x for x in tape[i:i+ints_to_skip]])

    if jmp == -1:
      i += ints_to_skip
    else:
      print 'jumping %d -> %d' % (i, jmp)
      i = jmp

output_data = []
calc(orig_tape, [5], output_data)

print 'output data:'
print output_data
