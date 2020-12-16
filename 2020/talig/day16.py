import sys
import functools
import operator
import re
import collections
import copy
import math


DAY = 16
RULES = r'^(.*?): (\d+)\-(\d+) or (\d+)\-(\d+)$'

class TicketMaster():
  def __init__(self):
    self.rules = {}
    self.valid = set()
    self.valid_tickets = []
    self.my_ticket = []
    self.invalid_numbers = []
    self.mapping = {}

  def Rules(self,lines):
    for i in range(len(lines)):
      if not lines[i]:
        return i+2 # Skip the empty line and 'your ticket:'
      parsed = re.findall(RULES, lines[i])[0]
      rule = parsed[0]
      parsed = [int(x) for x in parsed[1:]]
      rule_set = set(range(parsed[0], parsed[1]+1)).union(
                 set(range(parsed[2], parsed[3]+1)))
      self.rules[rule] = rule_set
      self.valid = self.valid.union(rule_set)

  def InvalidNumbers(self, tickets):
    for i in range(len(tickets)):
      valid = True
      for number in tickets[i]:
        if number not in self.valid:
          self.invalid_numbers.append(number)
          valid = False
      if valid:
        self.valid_tickets.append(tickets[i])

  def IdentifyRuleFromFields(self):
    # All we have left are valid tickets. 
    # A field might match a rule if all of the values are valid.
    # One of these fields presumably only fits one rule and then
    # can work backwards. 
    rule_to_field = dict((rule, []) for rule in self.rules.keys())

    for field in range(len(self.my_ticket)): # all tickets have the same length
      for rule in self.rules:
        possible = True
        for ticket in self.valid_tickets:
          if ticket[field] not in self.rules[rule]:
            possible = False
            break
        if possible:
          rule_to_field[rule].append(field)

    # Now lets backtrack
    ordered_rules = sorted(rule_to_field.items(), key=lambda x: len(x[1]))
    used = []
    for i in range(len(ordered_rules)):
      possibilities = ordered_rules[i][1] 
      if len(possibilities) == 1:
        used.extend(possibilities)
      else:
        for choice in used:
          ordered_rules[i][1].remove(choice)
        # This option should now have only one :)
        assert(len(possibilities)==1)
        used.extend(possibilities)
    
    # Map from field number to rule
    self.mapping = dict((x[1][0], x[0]) for x in ordered_rules)

  def DecypherMyTicket(self, prefix):
    assert(self.mapping)
    prefix_values = []
    for i in range(len(self.my_ticket)):
      if self.mapping[i].startswith(prefix):
        prefix_values.append(self.my_ticket[i])
    return functools.reduce(operator.mul, prefix_values)
    

def ParseTicket(line):
  return [int(x) for x in line.split(',')]

def NearbyTickets(start_idx, lines):
  tickets = []
  for i in range(start_idx, len(lines)):
    tickets.append(ParseTicket(lines[i]))
  return tickets

def BuildTicketMaster(lines):
  t = TicketMaster()
  next_idx = t.Rules(lines)
  t.my_ticket =  ParseTicket(lines[next_idx])
  tickets = NearbyTickets(next_idx + 3, lines) # skip the empty line and 'nearby tickets'.
  t.InvalidNumbers(tickets)
  return t


def Test():
  lines = ['class: 1-3 or 5-7',
           'row: 6-11 or 33-44',
           'seat: 13-40 or 45-50',
           '',
           'your ticket:',
           '7,1,14',
           '',
           'nearby tickets:',
           '7,3,47',
           '40,4,50',
           '55,2,20',
           '38,6,12']
  t = BuildTicketMaster(lines)
  print('Error rate:', sum(t.invalid_numbers), '==', 71)

  lines = ['class: 0-1 or 4-19',
           'row: 0-5 or 8-19',
           'seat: 0-13 or 16-19',
           '',
           'your ticket:',
           '11,12,13',
           '',
           'nearby tickets:',
           '3,9,18',
           '15,1,5',
           '5,14,9']
  t = BuildTicketMaster(lines)
  t.IdentifyRuleFromFields()

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]
  
  Test()
  print('Day', DAY, ' part 1')
  t = BuildTicketMaster(lines)
  print('Error rate for nearby tickets:', sum(t.invalid_numbers)) # 26009

  
  print('Day', DAY, ' part 2')
  t.IdentifyRuleFromFields()
  print('Product of departure fields:', t.DecypherMyTicket('departure')) # 26009
  

if __name__== '__main__':
  main()
