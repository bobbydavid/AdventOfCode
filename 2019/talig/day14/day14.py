import sys
from os import system
import copy
import collections
import itertools
import re
import math
from dag import DAG

class Chemistry:
  def __init__(self, data):
    self.reactions = collections.defaultdict(list)
    pattern = r'(\d+ \w+)'
    self.dag = DAG('FUEL')
    self.dag.AddNode('ORE', 1)
    for line in data:
      chems = re.findall(pattern, line)
      # Only one result for these inputs.
      result = chems.pop().split(' ')
      # result = (X, node_name)
      self.dag.AddNode(result[1], result[0])
      reactors = dict([(n, int(x)) for x,n in [
                  p.strip().split(' ') for p in chems]])
      value = (int(result[0]), reactors)
      self.reactions[result[1]] = value
    for k in self.reactions:
      self.dag.AddEdges(k, self.reactions[k][1])

  def GetDesired(self, desired, formula_source, formula_dest):
    return int(math.ceil(desired/(formula_dest * 1.0)) * formula_source)

  def ComputeIngredients(self, desired_fuel=1):
    sorted_nodes = self.dag.TopologicalSort()
    desired_amounts = collections.defaultdict(int)
    desired_amounts['FUEL'] = desired_fuel
    for node in sorted_nodes:
      if node == 'ORE':
        break
      formula_dest, reactors = self.reactions[node]
      desired = desired_amounts[node]
      for reactor_name in reactors:
        formula_source = reactors[reactor_name]
        new = self.GetDesired(desired, formula_source, formula_dest)
        desired_amounts[reactor_name] += new
    return desired_amounts['ORE']

  def ComputeMaxFuel(self, total_ore):
    ore_start = self.ComputeIngredients()
    start_fuel = total_ore/ore_start
    end_fuel = 2 * start_fuel
    while abs(end_fuel - start_fuel) > 1:
      mid_fuel = (start_fuel + end_fuel)/2
      ore = self.ComputeIngredients(mid_fuel)
      
      if ore  < total_ore:
        start_fuel = mid_fuel
      if ore  > total_ore:
        end_fuel = mid_fuel
    return start_fuel
    
def Expect(expected, found):
  if expected == found:
    print 'Pass'
  else:
    print 'Nope! Found ', found, ' vs. Expected ', expected

def Test(filename, data, total_ore):
  tests = {'test1.data': 31, 
           'test2.data': 165,
           'test3.data': 13312,
           'test4.data': 180697,
           'test5.data': 2210736}
  c = Chemistry(data)
  res =  c.ComputeIngredients()
  Expect(tests[filename], res)
  tests_b = {'test3.data': 82892753,
             'test4.data': 5586022,
             'test5.data': 460664}
  max_f = c.ComputeMaxFuel(total_ore)
  Expect(tests_b[filename], max_f)
  
def main():
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  filename = sys.argv[1]
  f = open(filename)
  data = [l.strip() for l in f.readlines()]
  f.close()

  total_ore = 1000000000000
  #TestB()
  if (filename.startswith('test')):
    Test(filename, data, total_ore)

  c = Chemistry(data)
  # (a) ==> 136771
  ore_for_1_fuel = c.ComputeIngredients()
  print 'We need %d units of ORE to produce 1 FUEL.' % ore_for_1_fuel

  # (b) ===> 
  c = Chemistry(data)
  max_fuel = c.ComputeMaxFuel(total_ore)
  print '1 Trillion ORE produces %d FUEL' % max_fuel
    
  

    
if __name__== "__main__":
  main()
