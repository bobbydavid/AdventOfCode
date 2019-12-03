import copy
import sys

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print 'Data file: ' + filename
with open(filename, 'r') as content_file:
  content = content_file.read()
  print content
  orig_tape = [int(x) for x in content.split(',') if x]

def calc(tape):
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
      i += 4
    elif op == 2:
      assert i + 4 < len(tape)
      arg1_index = tape[i + 1]
      arg2_index = tape[i + 2]
      dest_index = tape[i + 3]
      arg1 = tape[arg1_index]
      arg2 = tape[arg2_index]
      tape[dest_index] = arg1 * arg2
      i += 4
    elif op == 99:
      return tape[0]
      break
    else:
      assert False, 'unknown op ' + str(op)

for n in range(100):
  for v in range(100):
    tape= copy.copy(orig_tape)
    tape[1] = n
    tape[2] = v
    result = calc(tape)
    if result == 19690720:
      print 'noun = %d, verb = %d' % (n, v)
      sys.exit(0)

print 'not found'
sys.exit(1)

