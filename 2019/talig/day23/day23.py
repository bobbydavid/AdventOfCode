import sys
from os import system
from collections import deque
from computer import Computer
import time
import threading
from grid import Point

class ScopedLock():
  def __init__(self, lock):
    self.lock = lock

  def __enter__(self):
    self.lock.acquire()

  def __exit__(self, exception_type, exception_value, traceback):
    self.lock.release()

class NetworkQueue:
  def __init__(self, address, router):
    self.queue = deque()
    self.lock = threading.Lock()
    self.address = address
    self.router = router

  def get(self):
    v = -1
    with ScopedLock(self.lock):
      if self.queue:
        v = self.queue.popleft()
    if v != -1:
      self.router.set_last_active(self.address)
    return v

  def read_computer(self):
    #self.router.set_last_active(self.address)
    c = self.get()
    with ScopedLock(self.lock):
      if len(self.buffer) >=3:
        address, x, y = self.buffer[:3]
        self.buffer = self.buffer[3:]
        return (address, x, y)
    return None

  def put(self, value):
    with ScopedLock(self.lock):
      self.queue.append(value)
      self.router.set_last_active(self.address)
      if len(self.queue)==3:
        address, x, y = self.queue
        assert (address >=0 and address < 50) or address == 255
        self.router.send_packet((address, x, y))
        self.queue.clear()

  def write_computer(self, x, y):
    self.router.set_last_active(self.address)
    with ScopedLock(self.lock):
      self.queue.append(x)
      self.queue.append(y)

class Router:
  def __init__(self, intcode):
    self.nat = None
    self.first_nat = True
    now = time.time()
    self.last_active = [now] * 50
    self.computers = []
    for i in range(50):
      c = Computer(intcode, NetworkQueue(i, self), NetworkQueue(i, self), name='Computer%d'%i)
      # Give the computer its own address, need to bypass the guard for this one.
      c.InputQueue().put(i)
      c.daemon = True
      self.computers.append(c)
    print('Router initialized.')
  
  def set_last_active(self, address):
    self.last_active[address] = time.time()
  
  def is_all_idle(self):
    now = time.time()
    threshold = 0.1
    return all([now -x > threshold for x in self.last_active])

  def send_packet(self, packet):
    address, x, y = packet
    if address < 50:
      in_q = self.computers[address].InputQueue()
      in_q.write_computer(x,y)
    elif address == 255:
      self.nat = Point(x, y)
      if self.first_nat:
        print('First time writing to NAT: %s' % (self.nat))
        self.first_nat = False
    else:
      print('This should not happen... ')
    
  def run_all(self):
    now = time.time()
    self.last_active = [now] * 50
    for c in self.computers:
      c.start()
    print('Router running.')

  def join_all(self):
    last_y = None
    while True:
      while self.nat is None or not self.is_all_idle():
        time.sleep(0.2)

      # All is idle  
      self.send_packet((0, self.nat.x, self.nat.y))
      if last_y == self.nat.y:
        return self.nat.y
      last_y = self.nat.y

def main():
  if (len(sys.argv) < 2):
    test()
    print('Missing data file!')
    print('Usage: python [script] [data]')
    sys.exit(1)

  f = open(sys.argv[1])
  intcode = [int(x) for x in f.read().strip().split(',')] 
  f.close()

  router = Router(intcode)
  router.run_all()
  y = router.join_all()
  print('Got y %d twice' % y)
 
if __name__== "__main__":
  main()
