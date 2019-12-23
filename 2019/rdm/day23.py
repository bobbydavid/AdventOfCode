import sys
from collections import deque
import copy
import intcode
import time
import aoc
import threading


class ScopedLock():
  def __init__(self, lock):
    self.lock = lock

  def __enter__(self):
    self.lock.acquire()

  def __exit__(self, exception_type, exception_value, traceback):
    self.lock.release()


# Thread-safe way of providing data to the intcode computer.
class NicInputQueue():
  def __init__(self, router, addr):
    self.q_lock = threading.Lock()
    self.q = deque()
    self.router = router
    self.addr = addr

    self.q.append(addr)  # Set the address of this queue.

  # Provides data to the computer.
  def get(self):
    with ScopedLock(self.q_lock):
      if self.q:
        v = self.q.popleft()
      else:
        v = -1
    if v != -1:
      # Activity on this address (it's reading).
      self.router.notify_activity(self.addr)
    else:
      time.sleep(0.01) # Try to reduce spin-waiting.
    return v
    
  # Queues some data to be sent.
  def write_coords(self, x, y):
    with ScopedLock(self.q_lock):
      self.q.append(x)
      self.q.append(y)


# Forwards data it receives in batches of 3 to the router.
class ForwardingQueue():
  def __init__(self, router, addr):
    self.router = router
    self.addr = addr
    self.buffer = []

  def put(self, v):
    self.buffer.append(v)
    self.router.notify_activity(self.addr)
    if len(self.buffer) == 3:
      addr, x, y = self.buffer
      assert addr >= 0
      self.router.route_coords(addr, x, y)
      del self.buffer[:]


# Wraps the computer and handles input/output.
#
# Data will be forwarded to the router with the destination address.
class Nic():
  def __init__(self, router, addr):
    self.router = router
    self.addr = addr
    self.in_q = NicInputQueue(router, addr)
    self.out_q = ForwardingQueue(router, addr)
    self.computer = intcode.Computer('day23.data', self.in_q, self.out_q)

  def write_coords(self, x, y):
    self.in_q.write_coords(x, y)

  def run_async(self):
    self.computer.run_async()


# Runs all 50 NICs.
#
# Accepts data, 
class Router():
  def __init__(self):
    self.nics = []
    self.nat_lock = threading.Lock()
    self.nat_packet = None
    self.y_delivered = set()

    self.last_activity = [time.time()] * 50

    for i in range(50):
      nic = Nic(self, i)
      self.nics.append(nic)

  def route_coords(self, addr, x, y):
    assert addr >= 0
    if addr < 50:
      #print('@%d: %d, %d' % (addr, x, y))
      nic = self.nics[addr]
      nic.write_coords(x, y)
    else:
      with ScopedLock(self.nat_lock):
        if not self.y_delivered:
          print('First output to address %d: %d, %d' % (addr, x, y))
        self.nat_packet = (x, y)

  def run_all(self):
    for i in range(50):
      self.nics[i].run_async()
      self.last_activity[i] = time.time()


  def notify_activity(self, addr):
    self.last_activity[addr] = time.time()


  def all_idle(self):
    now = time.time()
    for ts in self.last_activity:
      if now - ts < 0.3:
        return False
    return True


  def join_all(self):
    while True:
      while not self.all_idle() or self.nat_packet is None:
        time.sleep(0.1)
      # Send the NAT packet to restart the network.
      with ScopedLock(self.nat_lock):
        x = self.nat_packet[0]
        y = self.nat_packet[1]
        if y in self.y_delivered:
          print('*** Repeated y value delivered: %d ***' % y)
          sys.exit(0)
        print('Sending NAT coords: %s' % (self.nat_packet,))
        self.y_delivered.add(y)
        self.nics[0].write_coords(x, y)
        self.nat_packet = None

    

router = Router()
router.run_all()
router.join_all()
