# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re
import collections
import copy

DAY = 7
MAP_TO_RE = r'(\d+) (.*?) bags?[,.]'
MAP_FROM = r'^(.*?) bags contain.*?$'


def BuildMapping(lines):
  mapping = {}
  reverse_mapping = {}
  for line in lines:
    # Risky, but I have reliable input.
    key = re.match(MAP_FROM, line).group(1)
    to = re.findall(MAP_TO_RE, line)
    mapping[key] = to
    for t in to:
      if t[1] not in reverse_mapping:
        reverse_mapping[t[1]] = set()
      reverse_mapping[t[1]].add(key)
  return mapping, reverse_mapping

def GetContainers(bag_color, reverse_mapping):
  # Get the size of the inverse graph rooted in the given bag color.
  queue = collections.deque([bag_color])
  containers = set()
  discovered = {bag_color: True}
  while queue:
    current = queue.popleft()
    if current in reverse_mapping:
      for w in reverse_mapping[current]:
        if w not in discovered:
          discovered[w] = True
          queue.append(w)
  return discovered


def GetContained(bag_color, mapping, bags_contained):
  if not mapping[bag_color]:
    # No contained bags.
    return 0
  total = 0
  for bag in mapping[bag_color]:
    b = int(bag[0])
    if bag[1] in bags_contained: 
      total += b + b * bags_contained[bag[1]]
    else:
      contained = GetContained(bag[1], mapping, bags_contained)
      bags_contained[bag[1]] = contained
      total += b + b * contained
  return total

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]
   
  mapping, reverse_mapping = BuildMapping(lines)
  my_bag = 'shiny gold'
  
  #print(mapping)
  containers = GetContainers(my_bag, reverse_mapping)
   
  print('Day', DAY, ' part 1')
  print('The number of container bags is: ', len(containers) - 1) # Exclude shiny gold, 355

  print('Day', DAY, ' part 2')
  print('The number of bags contained in a shiny gold bag: ', GetContained(my_bag, mapping, {})) # 5312


if __name__== '__main__':
  main()
