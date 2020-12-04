# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re
import collections
import copy

DAY = 4
#Passport = collections.namedtuple('Passport', ['byr','iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'])
PASSPORT_FIELDS_ = ['byr','iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
PASSPORT_DICT_ = dict([x, None] for x in PASSPORT_FIELDS_)
VALID_HAIR = r'^#[0-9a-f]{6}$'
VALID_EYE_COLORS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
VALID_PID = r'^\d{9}$'

def MakePassports(lines):
  passports = []
  passport = copy.deepcopy(PASSPORT_DICT_)
  for line in lines:
    if not line: # If it's empty. Note: I added a newline in the end of my data file. 
      passports.append(copy.deepcopy(passport))
      passport = copy.deepcopy(PASSPORT_DICT_)
    else:
      passport.update(dict([x.split(':') for x in line.split(' ')]))
  return passports

def AllMandatoryFieldsExist(passport):
  # CID is optional
  values = list(passport.values())
  return values.count(None) == 0 or (values.count(None) == 1 and passport['cid'] == None)

def BirthYearValid(byr):
  return byr >= 1920 and byr <= 2002

def IssueYearValid(iyr):
  return iyr >= 2010 and iyr <= 2020

def ExpirationYearValid(eyr):
  return eyr >= 2020 and eyr <= 2030

def HeightValid(hgt):
  try:
    val = int(hgt[:-2])
  except:
    return False
  if hgt[-2:] == 'cm':
    return val >= 150 and val <= 193
  elif hgt[-2:] == 'in':
    return val >= 59 and val <= 76
  return False

def HairColorValid(hcl):
  return re.match(VALID_HAIR, hcl)

def EyeColorValid(ecl):
  return ecl in VALID_EYE_COLORS 

def PIDValid(pid):
  return re.match(VALID_PID, pid)
  

def IsValid(passport):
  return (AllMandatoryFieldsExist(passport) and
          BirthYearValid(int(passport['byr'])) and 
          IssueYearValid(int(passport['iyr'])) and 
          ExpirationYearValid(int(passport['eyr'])) and
          HeightValid(passport['hgt']) and
          bool(HairColorValid(passport['hcl'])) and 
          EyeColorValid(passport['ecl']) and 
          PIDValid(passport['pid']))

def CountValid(passports, valid_func):
  count = 0
  for p in passports:
    count += 1 if valid_func(p) else 0
  return count  

def TestPart2():
  # Test BYR
  print('Testing Birth Year Validations')
  byr_tests = {1919: False, 1920: True, 1974: True, 2002:True, 2003: False}
  for year, result in byr_tests.items():
    if BirthYearValid(year) != result:
      print('Test failed for year: ', year)
  # Test IYR
  print('Testing Issue Year Validations')
  iyr_tests = {2009: False, 2010: True, 2015: True, 2020:True, 2021: False}
  for year, result in iyr_tests.items():
    if IssueYearValid(year) != result:
      print('Test failed for year: ', year)
  # Test EYR
  print('Testing Expiration Year Validations')
  eyr_tests = {2019: False, 2020: True, 2025: True, 2030:True, 2031: False}
  for year, result in eyr_tests.items():
    if ExpirationYearValid(year) != result:
      print('Test failed for year: ', year)
  # Test HGT
  print('Testing Height Validations')
  hgt_tests = {'190cm': True, '60in': True, 'kkkcm': False, 'blah': False}
  for hgt, result in hgt_tests.items():
    if HeightValid(hgt) != result:
      print('Test failed for height: ', hgt)
  # Test HCL
  print('Testing Hair Color Validations')
  hcl_tests = {'#95f96b': True, '#kkkcmm': False, '#abcdefg': False}
  for hcl, result in hcl_tests.items():
    if bool(HairColorValid(hcl)) != result:
      print('Test failed for hair color: ', hcl)
  # Test ECL
  print('Testing Eye Color Validations')
  ecl_tests = {'brn': True, 'kkkcmm': False}
  for ecl, result in ecl_tests.items():
    if bool(EyeColorValid(ecl)) != result:
      print('Test failed for hair color: ', ecl)
  # Test ECL
  print('Testing PID Validations')
  pid_tests = {'notnumbers': False, '000111222': True, '12345678': False, '9': False, '12345678999': False}
  for pid, result in pid_tests.items():
    if bool(PIDValid(pid)) != result:
      print('Test failed for hair color: ', pid)
    
  

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  lines = [x.strip() for x in lines]
  f.close()
  
  # Convert lines to passports.
  passports = MakePassports(lines)
  TestPart2()

  print('Day', DAY, ' part 1')
  print('There are ', CountValid(passports, AllMandatoryFieldsExist), ' valid passports.') # 182 for my input

  print('Day', DAY, ' part 2')
  print('There are ', CountValid(passports, IsValid), ' valid passports.') # 109 for my input



if __name__== '__main__':
  main()
