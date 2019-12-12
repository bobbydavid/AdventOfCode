import sys

# Initial positions (x, y, z)
#
# Sorry, this file includes part A and part B.

class Body():
  def __init__(self, initial_p):
    self.pos  = initial_p
    self.vel = [0 for p in initial_p]

  def __str__(self):
    return '{pos=%s, vel=%s}' % (self.pos, self.vel)

  def __repr__(self):
    return self.__str__()

  def energy(self):
    return sum(abs(n) for n in self.pos) * sum(abs(n) for n in self.vel)  # WTF


argc = len(sys.argv)
if argc != 3:
  print('Usage: python %s <data_name> <part>' % (sys.argv[0]))
  print('')
  print('  data_name = "real" or "test1" or "test2"')
  print('  part = "a" or "b"')
  print('')
  sys.exit(1)
else:
  data_name = sys.argv[1]
  part_name = sys.argv[2]

# Part A
if data_name == 'real':
  bodies = [
    Body([-13, 14, -7]),
    Body([-18, 9, 0]),
    Body([0, -3, -3]),
    Body([-15, 3, -13]),
  ]
  iteration_count = 1000
elif data_name == 'test1':
  bodies = [
    Body([-1, 0, 2]),
    Body([2, -10, -7]),
    Body([4, -8, 8]),
    Body([3, 5, -1]),
  ]
  iteration_count = 10
elif data_name == 'test2':
  bodies = [
    Body([-8, -10, 0]),
    Body([5, 5, 10]),
    Body([2, -7, 3]),
    Body([9, -8, -3]),
  ]
  iteration_count = 100
else:
  raise Exception('Unknown input: %s' % data_name)
  
print('Initial data:')
for b in bodies:
  print(b)
print('')


def apply_gravity(bodies):
  for i, body_a in enumerate(bodies):
    for body_b in bodies[i + 1:]:
      for d in range(len(body_a.pos)):
        if body_a.pos[d] < body_b.pos[d]:
          body_a.vel[d] += 1
          body_b.vel[d] -= 1
        elif body_a.pos[d] > body_b.pos[d]:
          body_a.vel[d] -= 1
          body_b.vel[d] += 1


def apply_velocity(bodies):
  for b in bodies:
    b.pos = [sum(nums) for nums in zip(b.pos, b.vel)]
          
def total_energy(bodies):
  return sum(b.energy() for b in bodies)


def advance_time(bodies):
  apply_gravity(bodies)
  apply_velocity(bodies)
  

def calc_state(bodies):
  state = []
  for b in bodies:
    state.append(tuple(b.pos + b.vel))
  return tuple(state)


def analyze_dimension(bodies, d):
  assert d >= 0 and d < len(bodies[0].pos)
  slices = [Body([body.pos[d]]) for body in bodies]
  i = 0
  target = calc_state(slices)
  count = 0
  while True:
    advance_time(slices)
    i += 1
    current_state = calc_state(slices)

    if current_state == target:
      return i

if part_name == 'a':
  for i in range(iteration_count):
    advance_time(bodies)
  print('total_energy=%d' % total_energy(bodies))
elif part_name == 'b':
  sys.stdout.write('answer:')
  for d in range(3):
    result = analyze_dimension(bodies, d)
    sys.stdout.write(' ' + str(result))
  sys.stdout.write('\n')
  # To find the actual answer, I plugged these into an online LCM calculator.
else:
  raise Exception('unknown part %s' % part_name)

