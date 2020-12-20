import sys
import functools
from os import system
import operator
import re
import collections
import copy
import math
import grid

DAY = 19
RULES = r'^(\d+): (.*?)$'


def RemoveSuperfluousCharacters(rule):
  rule = rule.replace('"','').replace('(a)','a').replace('(b)','b')
  return rule

def Interpret(rule, rules):
  or_array = [')', '|', '(']
  content = re.sub('[()|"+?]','', rules[rule])
  if not content.isalpha():
    unparsed = rules[rule].split(' ')
    parsed = []
    for k in unparsed:
      if k == '|':
        parsed.extend(or_array)
      else:
        term = Interpret(int(k), rules)
        if '|' in term:
          term = '(' + term + ')'
        parsed.append(term)
    rules[rule] = '(' + RemoveSuperfluousCharacters(''.join(parsed)) + ')'
  rules[rule] = RemoveSuperfluousCharacters(rules[rule])
  return rules[rule]

def ParseRules(lines):
  rules = {}
  for line in lines:
    if line == '':
      break
    m = re.match(RULES, line)
    if m:
      rules[int(m.group(1))] = m.group(2)
  return rules
    
def IsValid(rule, line):
  return bool(re.match('^' + rule + '$', line))

def GetValid(rule, lines):
  return [x for x in lines if IsValid(rule, x)]

def Rule11(r42, r31, depth):
  if depth == 0:
    return ''.join(['(',r42,r31,')', '?'])
  depth -= 1
  return ''.join(['(',r42, Rule11(r42, r31, depth), r31, ')','?'])

def AdjustRulesForPart2(rules, depth=5):
  Interpret(31, rules)
  Interpret(42, rules)
  r31 = '(' + rules[31] + ')'
  r42 = '(' + rules[42] + ')'
  rules[8] = '(' + r42+ ')+?' # One or more. Don't be greedy.
  # This should be enough for our inputs.
  # '42 (42 (42 (42 31)? 31)? 31)? 31' (this includes 42 31)
  rules[11] = ''.join([r42, Rule11(r42, r31, depth), r31])
  Interpret(0, rules)


def TestRule11():
  rules = {42: 'a', 31: 'b', 11: '42 31', 8: '42', 0: '8 11'}
  AdjustRulesForPart2(rules)
  tests = ['aab','aaabb','aaabbb','aaaabbbb', 'aaabbbbbbb','aaaaaaaaaaaaabb', '']
  for t in tests:
    print(t, ' ', IsValid(rules[0], t))
  

def Test():
  lines1 = ['0: 1 2',
           '1: "a"',
           '2: 1 3 | 3 1',
           '3: "b"']
  rules = ParseRules(lines1)
  # Now let's interpret the rules
  Interpret(0, rules)
  print(rules[0])

  lines2 = ['0: 4 1 5',
            '1: 2 3 | 3 2',
            '2: 4 4 | 5 5',
            '3: 4 5 | 5 4',
            '4: "a"',
            '5: "b"',
            '',
            'ababbb',
            'bababa',
            'abbbab',
            'aaabbb',
            'aaaabbb']
  rules2 = ParseRules(lines2)
  Interpret(0, rules2)
  lines2 = lines2[len(rules2) + 1:]
  valid = [x for x in lines2 if IsValid(rules2[0], x)]
  print('Test part 1: ', len(valid) == 2)
  
  f = open('day19test.data')
  lines3 = f.readlines()
  f.close()
  lines3 = [x.strip() for x in lines3]
  
  rules3 = ParseRules(lines3)
  rulecopy = copy.deepcopy(rules3)
  Interpret(0, rulecopy)
  lines3 = lines3[len(rules3) + 1:]
  valid3 = GetValid(rulecopy[0], lines3)
  print('Test part 2:', len(valid3), '==', 3)
  AdjustRulesForPart2(rules3, 5)
  new_valid = GetValid(rules3[0], lines3)
  print('Test part 2:', len(new_valid), '==', 12)

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]
  
  #TestRule11()
  Test()
  print('Day', DAY, ' part 1')
  rules = ParseRules(lines)
  old_rules = copy.deepcopy(rules)
  Interpret(0, rules)
  lines = lines[len(rules) + 1:]
  valid = GetValid(rules[0], lines)
  print('There are', len(valid), 'valid messages.') # 104

  # Note: The updated rules can only ADD more options.
  print('Day', DAY, ' part 2')
  update_rules = copy.deepcopy(old_rules)
  AdjustRulesForPart2(update_rules, 2) # Some searching on the minimal depth I need :) 
  new_valid = GetValid(update_rules[0], lines)
  print('There are', len(new_valid) , 'valid messages.') # 314
  

if __name__== '__main__':
  main()
