from collections import defaultdict
import copy
import itertools
import intcode
import sys
import threading

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  content = content_file.read()
  orig_tape = [int(x) for x in content.split(',') if x]


in_q = intcode.SimpleQueue()
in_q.put(2)
out_q = intcode.SimpleQueue()
print('in=%s, out=%s' % (in_q, out_q))

comp = intcode.Computer(orig_tape, in_q, out_q)
comp.run()
while not out_q.empty():
  print('out=%d' % out_q.get())
