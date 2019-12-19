import copy
import itertools
import queue
import sys
import threading

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  content = content_file.read()
  orig_tape = [int(x) for x in content.split(',') if x]

# print(orig_tape)

def compute(tape, input_queue, output_queue):
  tape = copy.deepcopy(tape)
  i = 0
  while True:
    instruction = tape[i]

    def get_mode(i, n):
      mode = instruction // 100
      # Find the Nth digit, counting right to left.
      for x in range(n):
        mode //= 10
      mode %= 10
      return mode

    def read_arg(i, n):
      mode = get_mode(i, n)
      index = i + 1 + n
      if mode == 0:
        result = tape[tape[index]]  # The number it points to.
      elif mode == 1:
        result = tape[index]  # The number itself.
      else:
        raise Exception('bad read mode %d' % mode)
      return result

    def write_arg(i, n, data):
      mode = get_mode(i, n)
      index = i + 1 + n
      if mode == 0:
        tape[tape[index]] = data
      else:
        raise Exception('bad write mode %d' % mode)

    op = instruction % 100
    jmp = -1  # -1 means "do not jump"

    if op == 1:  # ADD
      arg_count = 3
      arg1 = read_arg(i, 0)
      arg2 = read_arg(i, 1)
      write_arg(i, 2, arg1 + arg2)
    elif op == 2:  # MUL
      arg_count = 3
      arg1 = read_arg(i, 0)
      arg2 = read_arg(i, 1)
      write_arg(i, 2, arg1 * arg2)
    elif op == 3:  # WRITE FROM INPUT
      arg_count = 1
      write_arg(i, 0, input_queue.get())
    elif op == 4:  # OUTPUT
      arg_count = 1
      output_queue.put(read_arg(i, 0))
    elif op == 5:  # JUMP IF TRUE
      arg_count = 2
      if read_arg(i, 0) != 0:
        jmp = read_arg(i, 1)
    elif op == 6:  # JUMP IF FALSE
      arg_count = 2
      if read_arg(i, 0) == 0:
        jmp = read_arg(i, 1)
    elif op == 7:  # LESS THAN
      arg_count = 3
      result = 0
      if read_arg(i, 0) < read_arg(i, 1):
        result = 1
      write_arg(i, 2, result)
    elif op == 8:  # EQUALS
      arg_count = 3
      result = 0
      if read_arg(i, 0) == read_arg(i, 1):
        result = 1
      write_arg(i, 2, result)
    elif op == 99:
      return
    else:
      raise Exception('unknown op %s' % op)
    ints_to_skip = 1 + arg_count
    assert i + ints_to_skip < len(tape), 'i=%d, skip=%d, len=%d' % (i, ints_to_skip, len(tape))

    if jmp == -1:
      i += ints_to_skip
    else:
      i = jmp


max_thrust = 0
best_order = []
for order in itertools.permutations(range(5, 10)):
  # Inputs and outputs are the same queues, and are circular.
  output_queues = [queue.Queue() for x in order]
  input_queues = output_queues[-1:] + output_queues[:-1]

  # Each input gets the data from the permutation.
  for (q, x) in zip(input_queues, order):
    q.put(x)

  # Spin up a computer thread for each amplifier.
  threads = []
  for (in_q, out_q, x) in zip(input_queues, output_queues, order):
    threads.append(threading.Thread(target=compute, args=(orig_tape, in_q, out_q)))

  input_queues[0].put(0)  # Initial input to amplifier A.

  # Start all threads, wait for them to complete.
  for t in threads:
    t.start()
  for t in threads:
    t.join()

  # Retrieve result from last output queue.
  out_q = output_queues[-1]
  assert not out_q.empty()
  thrust = out_q.get()
  assert out_q.empty()

  if thrust > max_thrust:
    max_thrust = thrust
    best_order = order


print('max: = %d, order = %s' % (max_thrust, best_order))


