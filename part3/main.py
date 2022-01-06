from z3 import *


solver = Solver()
constraints = []
Name, name_consts = EnumSort("Name", ["Germain", "Franklin", "Lovelace",
"Curie", "Noether"])
germain, franklin, lovelace, curie, noether = name_consts
Arrival, arrival_consts = EnumSort("Arrival",["Boat", "Train", "Plane",
"Foot", "Bus"])
boat, train, plane, foot, bus = arrival_consts
Food, food_consts = EnumSort("Food", ["Burger", "Soup", "Salad", "Cake",
"Chicken"])
burger, soup, salad, cake, chicken = food_consts
Object, object_consts = EnumSort("Object", ["Laptop", "Pencil",
"Scales", "Abacus", "Telescope"])
laptop, pencil, scales, abacus, telescope = object_consts
Pet, pet_consts = EnumSort("Pet", ["Rabbit", "Dog", "Cat", "Fish",
"Dont_know"])
rabbit, dog, cat, fish, dont_know = pet_consts
location = Function("location", Name, IntSort())
arrival = Function("arrival", Name, Arrival)
food = Function("food", Name, Food)
obj = Function("obj", Name, Object)
pet = Function("pet", Name, Pet)
constraints.append(Distinct([obj(name) for name in name_consts]))
constraints.append(Distinct([food(name) for name in name_consts]))
constraints.append(Distinct([arrival(name) for name in name_consts]))
constraints.append(Distinct([location(name) for name in name_consts]))
constraints.append(Distinct([pet(name) for name in name_consts]))
for name in name_consts:
 constraints.append(Or([location(name) == x for x in
range(len(name_consts))]))
 constraints.append(Or([arrival(name) == x for x in arrival_consts]))
 constraints.append(Or([food(name) == x for x in food_consts]))
 constraints.append(Or([obj(name) == x for x in object_consts]))
 constraints.append(Or([pet(name) == x for x in pet_consts]))
# Noether had many difficulties during the journey there by foot;
constraints.append(arrival(noether) == foot)
# Germain, who was at the far left, heard the woman sitting next to her telling
# tales of her journey by boat

constraints.append(location(germain) == 0)
name_clue1 = Const("name_clue1", Name)
constraints.append(location(name_clue1) == 1)
constraints.append(arrival(name_clue1) == boat)
# The woman who had got there by train sat left of someone who had got there by
# plane;
name_clue2 = Const("name_clue2", Name)
name_clue3 = Const("name_clue3", Name)
constraints.append(arrival(name_clue2) == train)
constraints.append(arrival(name_clue3) == plane)
constraints.append(location(name_clue2) < location(name_clue3))
# the woman eating burger mentioned that getting there was her first time
# traveling by train
name_clue4 = Const("name_clue4", Name)
constraints.append(arrival(name_clue4) == train)
constraints.append(food(name_clue4) == burger)
# The woman who had got there by bus mentioned how she had left her pet rabbit
# at home
name_clue5 = Const("name_clue5", Name)
constraints.append(arrival(name_clue5) == bus)
constraints.append(pet(name_clue5) == rabbit)
# One of the ladies opened her bag and took out her laptop;
# the woman next to her recalled how she used to have one of those too, but then
# her pet rabbit chewed it and spat it out completely useless.
name_clue6 = Const("name_clue6", Name)
name_clue7 = Const("name_clue7", Name)
constraints.append(pet(name_clue6) == rabbit)
constraints.append(obj(name_clue7) == laptop)
constraints.append(Or(location(name_clue6) == location(name_clue7) - 1,
location(name_clue6) == location(name_clue7) + 1))
# So Lovelace reached for her pocket and pulled out the pencil she had brought
# with her,
# at which the woman who owned a dog wondered whether it was more useful for her
# research than the scales that she herself owned
constraints.append(obj(lovelace) == pencil)
name_clue8 = Const("name_clue8", Name)
constraints.append(pet(name_clue8) == dog)
constraints.append(obj(name_clue8) == scales)
# One of the ladies waved her abacus close to her neighbor's face; the neighbor,
# who owned a cat, retaliated by flipping over her assailant's soup.
name_clue9 = Const("name_clue9", Name)
constraints.append(obj(name_clue9) == abacus)
constraints.append(food(name_clue9) == soup)
name_clue10 = Const("name_clue10", Name)
name_clue11 = Const("name_clue11", Name)
constraints.append(obj(name_clue10) == abacus)
constraints.append(pet(name_clue11) == cat)
constraints.append(Or(location(name_clue10) == location(name_clue11) -
1, location(name_clue10) == location(name_clue11) + 1))
# Franklin tried to ignore the noise and just eat her salad in peace

constraints.append(food(franklin) == salad)
# The woman who owned a fish was unhappily eating her cake, envying the chicken
# plate enjoyed by the guest at the center seat
name_clue12 = Const("name_clue12", Name)
constraints.append(pet(name_clue12) == fish)
constraints.append(food(name_clue12) == cake)
name_clue13 = Const("name_clue13", Name)
constraints.append(food(name_clue13) == chicken)
constraints.append(location(name_clue13) == 2)
# When all was said and done, Curie had learned a lot from her colleagues but
# was happy to go home to her pet fish.
constraints.append(pet(curie) == fish)
solver.add(constraints)
def print_model(m):
 s = [None] * len(name_consts)
 for name in name_consts:
  object_name = str(m.eval(obj(name)))
  s[m.eval(location(name)).as_long()] = "{} {}".format(name,
object_name.lower())
 print(" ".join(s))
while solver.check() == sat:
 m = solver.model()
 print_model(m)
 expressions = []
 for name in name_consts:
  expressions.append(location(name) != m.eval(location(name)))
  expressions.append(arrival(name) != m.eval(arrival(name)))
  expressions.append(food(name) != m.eval(food(name)))
  expressions.append(obj(name) != m.eval(obj(name)))
  expressions.append(pet(name) != m.eval(pet(name)))

 solver.add(Or(expressions))

# ----------------------------------------------------------------------------

from typing import Iterable
from itertools import zip_longest
import json, string, sys
ALPHABET = string.printable

def is_ordered_subset(target: Iterable, sample: Iterable) -> bool:

 ti = 0
 si = 0
 while ti < len(target) and si < len(sample):
  if target[ti] == sample[si]:
   ti += 1
   si +=1
  else:
   ti += 1
 return si == len(sample)


def solve(file: str, expected_output: str = None):
 exp_output = list(expected_output) if expected_output is not None else [None]
 match_count = 0
 with open(file) as f:
  j = json.loads(f.read())
  for expected_char, arr in zip_longest(exp_output, j):

   values = []
   for char in ALPHABET:
    flag = True
    for a in arr:

     if len(a) > 0:

      byte = "".join([str(x) for x in a])
      if not is_ordered_subset(format(ord(char), 'b').zfill(8), byte):
       flag = False
       break
    if flag is True:
     values.append(char)
   if expected_char is not None:
    print(f"[{expected_char}] | ", end='')
    if expected_char in values:
     match_count += 1
   print(values)
 if expected_output is not None:
  print("Match count: {}/{}".format(match_count, len(exp_output)))
solve(*["C:\\Users\\97252\\Documents\\cyber\\second_signal.txt"])

 #C:\Users\97252\Documents\cyber\Own Challange\Our Challange\second_signal.txt