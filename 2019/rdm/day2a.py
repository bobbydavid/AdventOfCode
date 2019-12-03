import sys

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print 'Data file: ' + filename
with open(filename, 'r') as content_file:
  content = content_file.read()
  print content
  tape = [int(x) for x in content.split(',') if x]

print 'Found ' + str(len(tape)) + ' opcodes:'


tape[1] = 12
tape[2] = 2

i = 0
while True:
  op = tape[i]
  if op == 1:
    assert i + 4 < len(tape)
    arg1_index = tape[i + 1]
    arg2_index = tape[i + 2]
    dest_index = tape[i + 3]
    arg1 = tape[arg1_index]
    arg2 = tape[arg2_index]
    tape[dest_index] = arg1 + arg2
    print '@%d: ADD %d (@ %d) + %d (@ %d) = %d, stored @ %d' % (i, arg1, arg1_index, arg2, arg2_index, (arg1 + arg2), dest_index)
    i += 4
  elif op == 2:
    assert i + 4 < len(tape)
    arg1_index = tape[i + 1]
    arg2_index = tape[i + 2]
    dest_index = tape[i + 3]
    arg1 = tape[arg1_index]
    arg2 = tape[arg2_index]
    tape[dest_index] = arg1 * arg2
    print '@%d: MUL %d (@ %d) * %d (@ %d) = %d, stored @ %d' % (i, arg1, arg1_index, arg2, arg2_index, (arg1 * arg2), dest_index)
    i += 4
  elif op == 99:
    print '99 -> program exit'
    break
  else:
    assert False, 'unknown op ' + str(op)

print 'Final tape:'
print tape

