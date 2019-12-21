import intcode
import StringIO
from collections import deque
import sys
import Queue
import copy


class EchoQueue():
  def __init__(self, last_cmd, istream, stream, outputs):
    self.last_cmd = last_cmd
    self.stream = stream
    self.istream = istream
    self.outputs = outputs
    self.q = Queue.Queue()

    self.buffer = deque()
    for i in xrange(2):
      self.buffer.append(None)
    self.robot_x = None
    self.current_x = 0

  def get(self):
    while self.q.empty():
      line = self.istream.readline()
      if line == '\n':
        line = self.last_cmd + '\n'
      for c in line:
        self.q.put(ord(c))
    c = self.q.get()
    return c

  def put(self, c):
    self.write(c)

    if c == ord('@'):
      self.robot_x = self.current_x
    if c == 10:
      self.current_x = 0
    else:
      self.current_x += 1

    self.buffer.popleft()
    self.buffer.append(c)
    if self.buffer[0] == ord('#') and self.buffer[1] == ord('\n'):
      self.stream.write(' ' * self.robot_x)
      self.stream.write(' ABCDEFGHI\n')
        

  def write(self, c):
    if c < 256:
      c = chr(c)
    else:
      self.outputs.append(c)
      c = '\nOutput: %d\n' % c
    self.stream.write(c)
    self.stream.flush()




class Droid():
  def __init__(self, last_cmd, inp=None):
    self.num_outputs = []
    istream = sys.stdin
    if inp is not None:
      istream = StringIO.StringIO(inp)
    self.q = EchoQueue(last_cmd, istream, sys.stdout, self.num_outputs)
    self.computer = intcode.Computer("day21.data", self.q, self.q)

  def add_input(self, inp):
    for c in inp:
      self.q.put(ord(c))

  def run(self):
    self.computer.run()
    return self.num_outputs

  def result(self):
    if not self.num_outputs:
      return None
    assert len(self.num_outputs) == 1
    return self.num_outputs[0]

  
  """
  def refresh_screen(self):
    out = []
    while True:
      try:
        c = self.out_q.get_nowait()
        if c < 256:
          c = chr(c)
        else:
          c = '\nOutput: %d\n' % c
        out.append(c)
      except Queue.Empty:
        break
    sys.stdout.write(''.join(out))
  """


def playground(last_cmd='WALK'):
  while True:
    droid = Droid(last_cmd=last_cmd)
    if droid.run():
      break


def try_solution(soln, expected):
  commands = soln.split('\n')
  commands = [c.partition('#') for c in commands]
  commands = [c for c, _, _ in commands]
  commands = [c.strip() for c in commands if c.strip()]

  droid = Droid(last_cmd='WALK', inp=('\n'.join(commands) + '\n'))
  success = droid.run()
  if not success:
    print('crashed :(')
  else:
    assert droid.result() == expected, 'expected %s, saw: %s' % (
        expected, repr(droid.result()))

def solve_part_a():
  program = """
NOT T T
AND A T
AND B T
AND C T
NOT T T
AND D T
OR T J
WALK
  """
  try_solution(program, 19361332)

def solve_part_b():
  program = """
NOT T T
NOT T T
AND A T
AND B T
AND C T
NOT T T  #

AND D T

OR T J
WALK
AND E T
AND F T
AND G T
NOT T T
AND H T

RUN
  """
  try_solution(program, None)


arg = 'WALK'
if len(sys.argv) >= 2:
  arg = sys.argv[1]

if arg == 'a':
  solve_part_a()
elif arg == 'b':
  solve_part_b()
else:
  print('using last command: %s' % arg)
  playground(arg.upper())

  


  
  
