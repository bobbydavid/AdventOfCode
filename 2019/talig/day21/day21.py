import sys
from Queue import Queue
from computer import Computer
from os import system
import itertools

def display_prompt(out_q):
  c = None
  prompt = []
  while c != ':':
    c = chr(out_q.get())
    prompt.append(c)
  print ''.join(prompt)
  
def display_hull(out_q):
  c = out_q.get()
  buff = []
  while c < 256:
    if c != 10:
      buff.append(chr(c))
    else:
      print ''.join(buff)
      buff = []
    c = out_q.get()
  print 'Damage to hull: ', c

def manual_control(computer):
  command = ''
  in_q = computer.InputQueue()
  while command != 'q':
    command = raw_input('')
    command.strip()
    for x in command:
      in_q.put(ord(x))
    in_q.put(ord('\n'))
  display_hull(computer.OutputQueue())
  
def feed_code(springcode, in_q):
  print 'Feeding code!'
  for line in springcode:
    for x in line:
      in_q.put(ord(x))
    in_q.put(ord('\n'))

# (a) ==> 19355364
def walk_hull(computer):
  springcode = [
          'NOT A J',
          'NOT B T',
          'OR T J',
          'NOT C T',
          'OR T J',
          'AND D J',
          'WALK'
         ]
  feed_code(springcode, computer.InputQueue())
  display_hull(computer.OutputQueue())

# (b) => 1142530574
def run_hull(computer):
  # (!A || !B || !C ) && (D && (E || H) && (H || F || I))
  springcode = [
                'NOT A J',
                'NOT B T',
                'OR T J',
                'NOT C T',
                'OR T J',  # J = !A || !B || !C
                'NOT H T',
                'NOT T T',
                'OR F T',
                'OR I T',  # T = H || F || I
                'AND T J', # J =  (!A || !B || !C) && (H || F || I)
                'NOT E T',
                'NOT T T',
                'OR H T',  # T = E || H
                'AND T J',
                'AND D J',
                'RUN',
         ]
  feed_code(springcode, computer.InputQueue())
  display_hull(computer.OutputQueue())

def main():
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  intcode = [int(x) for x in f.read().split(',')]
  f.close()
  
  computer = Computer(intcode, Queue(), Queue())
  computer.daemon = True
  _ = system('clear')
  computer.start()
  display_prompt(computer.OutputQueue())
  if sys.argv[2] == 'a':
    walk_hull(computer)
  else:
    run_hull(computer)
    #manual_control(computer)
 
if __name__== "__main__":
  main()
