import intcode
import math
import string
import sys
import Queue



def load_tape(filename):
  with open(filename, 'r') as contents:
    return [int(x) for x in contents.read().split(',') if x]

_cached_tape = load_tape('day19.data')
def check_coords(x, y):
  QueueFactory = intcode.SimpleQueue
  in_q = QueueFactory()
  in_q.put(x)
  in_q.put(y)
  out_q = QueueFactory()
  drone = intcode.Computer(_cached_tape, in_q, out_q)
  drone.run()
  out = out_q.get()
  if out == 1:
    return '#'
  elif out == 0:
    return '.'
  else:
    raise Exception('bad output: %s' % out)

  


def print_part_a():
  count = 0
  x_to_skip = 0
  for y in xrange(50):
    l = None
    r = None
    for x in xrange(50):
      if x < x_to_skip:
        c = '.'
      else:
        c = check_coords(x, y)
      if c == '#':
        count += 1
        if l is None:
          l = x
          s_to_skip = x - 2 
      if c == '.' and r is None and l is not None:
        r = x - 1
    if r is None:
      return
    dodraw(y, l, r)

def solve_part_a():
  count = 0
  for y in xrange(50):
    l = None
    r = None
    for x in xrange(50):
      c = check_coords(x, y)
      if c == '#':
        count += 1
  print('count: %d' % count)


def dodraw(y, l, r):
  w = r + 1 - l
  print('%3d:'%y + '.' * (l - 1) + '#' * w + ' %s'%((l,r),))
      

def solve_part_b(sq, draw = False):
  last_sq = []
  for y in xrange(10000):
    #if y % 100 == 0:
    #  print 'y=%d' % y
    if y < 10:
      l = 2 * y - max(0, int(math.floor(float(y - 1) / 3)))
      r = 2 * y + int(math.floor(float(y) / 5))
    else:
      while check_coords(l, y) == '.':
        l += 1
      while check_coords(r + 1, y) == '#':
        r += 1
    last_sq.append( (l,r) )



    py = y - sq + 1
    if py < 0:
      continue

    prev_l, prev_r = last_sq[py]   # potentially 1st row of ship

    overlap = prev_r + 1 - l
    if overlap >= sq:
      sleigh_x = l
      sleigh_y = py
      print('py=%d, y=%d, l=%d, r=%d, prev_l=%d, prev_r=%d, sleigh_x=%d, sleigh_y=%d, overlap=%d' % (
          py, y, l, r, prev_l, prev_r, sleigh_x, sleigh_y, overlap))
      if draw:
        i = 0
        for i in xrange(sq):
          xl, xr = last_sq[py + i]
          idx = py + i
          indent = sleigh_x - xl
          post = xr - (sleigh_x + sq - 1)
          assert (xr - xl + 1) == (indent + sq + post)
          print('%3d:'%idx+'.'*(xl-1)+'#'*indent+'O'*sq+'#'*post+' %s'%((xl,xr),))
          #dodraw(idx, xl,xr)

      print('py=%d, y=%d, l=%d, r=%d, prev_l=%d, prev_r=%d, sleigh_x=%d, sleigh_y=%d' % (
          py, y, l, r, prev_l, prev_r, sleigh_x, sleigh_y))
      sleigh_r = sleigh_x + sq - 1
      assert sleigh_r <= prev_r
      assert sleigh_r <= r
          
      print(sleigh_x * 10000 + sleigh_y)
      return sleigh_x * 10000 + sleigh_y

    if draw:  # draw on screen
      dodraw(py, prev_l, prev_r)


#solve_part_a()
#print_part_a()
sq = 100
answer = solve_part_b(sq, draw=False)

assert answer < 9880491  # My first guess was bad.
