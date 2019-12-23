import sys
from collections import deque
import copy
import intcode
import aoc
import Queue
import threading


class ScopedLock():
  def __init__(self, lock):
    self.lock = lock

  def __enter__(self):
    self.lock.acquire()

  def __exit__(self, exception_type, exception_value, traceback):
    self.lock.release()


class NicInputQueue():
  def __init__(self):
    self.lock = threading.Lock()
    self.q = deque()

  def get(self):
    with ScopedLock(self.lock):
      if self.q:
        v = self.q.popleft()
      else:
        v = -1
      return v

  # Sets the initial address for the queue.
  def write_addr(self, addr):
    with ScopedLock(self.lock):
      assert not self.q
      self.q.append(addr)
    
  def write_coords(self, x, y):
    with ScopedLock(self.lock):
      self.q.append(x)
      self.q.append(y)


class ForwardingQueue():
  def __init__(self, router):
    self.router = router
    self.buffer = []

  def put(self, v):
    self.buffer.append(v)
    if len(self.buffer) == 3:
      addr, x, y = self.buffer
      assert addr >= 0
      self.router.route_coords(addr, x, y)
      del self.buffer[:]


class Nic():
  def __init__(self, router, addr):
    self.router = router
    self.addr = addr
    self.in_q = NicInputQueue()
    self.in_q.write_addr(addr)
    self.out_q = ForwardingQueue(router)
    self.computer = intcode.Computer('day23.data', self.in_q, self.out_q)

  def write_coords(self, x, y):
    self.in_q.write_coords(x, y)

  def run_async(self):
    self.computer.run_async()


class Router():
  def __init__(self):
    self.nics = []
    self.lock = threading.Lock()
    for i in range(50):
      nic = Nic(self, i)
      self.nics.append(nic)

  def route_coords(self, addr, x, y):
    with ScopedLock(self.lock):
      assert addr >= 0
      if addr < 50:
        print('@%d: %d, %d' % (addr, x, y))
        nic = self.nics[addr]
        nic.write_coords(x, y)
      else:
        print('Output to address %d: %d, %d' % (addr, x, y))

  def run_all(self):
    for i in range(50):
      self.nics[i].run_async()

  def join_all(self):
    for i in range(50):
      self.nics[i].computer.wait()
    

router = Router()
router.run_all()
router.join_all()
