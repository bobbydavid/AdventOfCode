from collections import defaultdict
from collections import deque
import curses
import copy
import itertools
import sys
import threading


# Simple queue for interacting with the Computer.
class SimpleQueue():
  def __init__(self):
    self.q = deque()

  def get(self):
    x = self.q.popleft()
    assert type(x) is int
    return x

  def put(self, x):
    assert type(x) is int
    self.q.append(x)

  def empty(self):
    return self.q

  def __repr__(self):
    return self.q

  def __str__(self):
    return str(self.q)


# IntOp computer.
#
# Read from input_queue using get()
# Write to output_queue using put(x)
class Computer():
  def __init__(self, tape, input_queue, output_queue):
    self.tape = defaultdict(int, enumerate(tape))
    self.input_queue = input_queue
    self.output_queue = output_queue
    self.instruction_pointer = 0
    self.relative_base = 0
    self.stopped = False

    self.debug_level = 0

  # Returns the mode for the Nth argument.
  def _get_mode(self, i, n):
    instruction = self.tape[i]
    self.dbg(5, '# _get_mode: instruction=%d, n=%d' % (instruction, n))
    mode = instruction // 100
    # Find the Nth digit, counting right to left.
    self.dbg(5, '# mode=%d n=%d' % (mode, n))
    for x in range(n):
      mode //= 10
      self.dbg(5, '# mode=%d n=%d' % (mode, n))
    mode %= 10
    self.dbg(5, '# mode=%d n=%d' % (mode, n))
    return mode

  # Reads the Nth argument for the instruction at i.
  def _read_arg(self, i, n):
    instruction = self.tape[i]
    self.dbg(5, '## instruction=%d' % instruction)
    mode = self._get_mode(i, n)
    index = i + 1 + n
    # print('# read_arg(%d, %d): mode=%d' % (i, n, mode))
    if mode == 0:
      result = self.tape[self.tape[index]]  # The number it points to.
    elif mode == 1:
      result = self.tape[index]  # The number itself.
    elif mode == 2:
      # Points to + offset
      result = self.tape[self.relative_base + self.tape[index]]
    else:
      raise Exception('bad read mode %d' % mode)
    self.dbg(3, '# _read_arg(%d, %d): result=%d' % (i, n, result))
    return result

  # Writes `data` into the location specified by the Nth argument.
  def _write_arg(self, i, n, data):
    assert type(data) is int, 'data=%s' % (data,)
    mode = self._get_mode(i, n)
    index = i + 1 + n
    if mode == 0:
      loc = self.tape[index]
    elif mode == 2:
      loc = self.tape[index] + self.relative_base
    else:
      raise Exception('bad write mode %d' % mode)
    self.dbg(3, '# _write_arg(%d, %d, %d): location=%d' % (i, n, data, loc))
    self.tape[loc] = data

  # Runs until the program halts.
  def run(self):
    assert not self.stopped
    while not self.stopped:
      self.run_next_instruction()

  # Runs one instruction.
  def run_next_instruction(self):
    i = self.instruction_pointer
    instruction = self.tape[i]
    self.dbg(4, '# @%d: instruction=%d' % (i, instruction))
    op = instruction % 100
    jmp = -1  # -1 means "do not jump"

    if op == 1:
      op_name = 'ADD'
      arg_count = 3
      arg1 = self._read_arg(i, 0)
      arg2 = self._read_arg(i, 1)
      self._write_arg(i, 2, arg1 + arg2)
    elif op == 2:
      op_name = 'MUL'
      arg_count = 3
      arg1 = self._read_arg(i, 0)
      arg2 = self._read_arg(i, 1)
      self._write_arg(i, 2, arg1 * arg2)
    elif op == 3:
      op_name = 'READ'
      arg_count = 1
      inp = self.input_queue.get()
      if type(inp) is not int:
        raise Exception('read bad input: %s' % inp)
      self._write_arg(i, 0, inp)
    elif op == 4:
      op_name = 'WRITE'
      arg_count = 1
      out = self._read_arg(i, 0)
      self.output_queue.put(out)
    elif op == 5:
      op_name = 'JNZ'  # JUMP IF NOT ZERO
      arg_count = 2
      if self._read_arg(i, 0) != 0:
        jmp = self._read_arg(i, 1)
    elif op == 6:
      op_name = 'JZ'  # JUMP IF ZERO
      arg_count = 2
      if self._read_arg(i, 0) == 0:
        jmp = self._read_arg(i, 1)
    elif op == 7:
      op_name = 'LESS'
      arg_count = 3
      result = 0
      if self._read_arg(i, 0) < self._read_arg(i, 1):
        result = 1
      self._write_arg(i, 2, result)
    elif op == 8:
      op_name = 'EQ'
      arg_count = 3
      result = 0
      if self._read_arg(i, 0) == self._read_arg(i, 1):
        result = 1
      self._write_arg(i, 2, result)
    elif op == 9:
      op_name = 'REL'  # Modify relative base.
      arg_count = 1
      delta = self._read_arg(i, 0)
      self.relative_base += delta
      self.dbg(2, '# base + %d = %d' % (delta, self.relative_base))
    elif op == 99:
      op_name = 'STOP'
      arg_count = 0
      self.stopped = True
    else:
      raise Exception('unknown op %s' % op)
    ints_to_skip = 1 + arg_count
    assert i + ints_to_skip < len(self.tape), (
        '%s: i=%d, skip=%d, len=%d' % (op_name, i, ints_to_skip, len(self.tape)))

    self.dbg(1, '%s [done]: ip=%d, tape[%d:%d]=[%s]' % (
        op_name, self.instruction_pointer, i, i + arg_count,
        ', '.join([str(self.tape[i + x]) for x in range(arg_count + 1)])))

    if self.stopped:
      return

    if jmp == -1:
      i += ints_to_skip
    else:
      self.dbg(2, '# Jumping to %d' % jmp)
      i = jmp
    self.instruction_pointer = i



  def dbg(self, level, msg):
    if level <= self.debug_level:
      print(msg)

