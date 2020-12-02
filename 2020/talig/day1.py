# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator

SUM_TO = 2020

def MakeDict(lines, target):
  expense_map = {}
  for line in lines:
    num = int(line) # No need to remove the newline
    expense_map[num] = target - num
  return expense_map

def TwoSumTo(expense_map):
  for key in expense_map:
    if expense_map[key] in expense_map:
      return key
    
def ThreeSumTo(expense_map, target):
  # Find 3 numbers that sum to 2020.
  # Thoughts: sum all choices of 3. Sum all pairs and see if 2020-that exists. 
  # The latter has less options. 
  expenses = list(expense_map.keys())
  for i in range(len(expenses)):
    for j in range(i, len(expenses)):
      remainder = target - expenses[i] - expenses[j]
      # Return when first option comes along.
      if remainder in expense_map:
        return (remainder, expenses[i], expenses[j])
      
    

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  expenses = MakeDict(lines, SUM_TO)
  print("Day 1 part 1")
  key = TwoSumTo(expenses)
  print("Found numbers: ", key, expenses[key])
  print("Product is: ", key * expenses[key])
  print("Day 1 part 2")
  triplet = ThreeSumTo(expenses, SUM_TO)
  print("Found numbers: ", triplet)
  print("Product is: ", functools.reduce(operator.mul, triplet))


if __name__== "__main__":
  main()
