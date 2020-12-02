# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re

DAY = 2
LINE_RE = '(\d+)-(\d+) (\w): (\w+)'

def Part1Valid(lower, upper, letter, password):
  incidents = password.count(letter)
  return incidents >= int(lower) and incidents <= int(upper)

def Part2Valid(first, second, letter, password):
  return operator.xor(password[first-1] == letter, password[second - 1] == letter)

def ParsePasswords(lines):
  passwords = []
  for line in lines:
    m = re.match(LINE_RE, line)
    (lower, upper, letter, password) = m.groups()
    passwords.append((password, int(lower), int(upper), letter))
  return passwords

def Validate(passwords, valid_func):
  valid_count = 0
  for password, lower, upper, letter in passwords:
    valid = valid_func(lower, upper, letter, password)
    valid_count += 1 if valid else 0
  return valid_count 

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  
  passwords = ParsePasswords(lines)
  print('Day', DAY, ' part 1')
  valid_count = Validate(passwords, Part1Valid)
  print('There are ', valid_count, ' valid passwords.') # 625 for my input

  print('Day', DAY, ' part 2')
  valid_count = Validate(passwords, Part2Valid)
  print('There are ', valid_count, ' valid passwords.') # 391 for my input



if __name__== '__main__':
  main()
