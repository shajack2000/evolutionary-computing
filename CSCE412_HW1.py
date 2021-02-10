########################################################################################################################
# NAME: Sha Jackson and Benjamin Good
# COURSE: CSCE 412 - Evolutionary Computing, Frank Moore
# ASSIGNMENT: Project 1 - Genetic Algoritms
# DESCRIPTION:
#
# HELPFUL SOURCES:
#	- https://www.youtube.com/watch?v=nhT56blfRpE&ab_channel=KieCodes
#	- http://gpbib.cs.ucl.ac.uk/gecco2006/docs/p609.pdf
########################################################################################################################

import string
import random

userstr1 = input("Enter the first string: ")
userstr2 = input("Enter the second string: ")

short_str = userstr1
long_str = userstr2

if len(long_str) < len(short_str):
	short_str, long_str = long_str, short_str
	
# This effectively performs a coin flip at each index to determine whether the bit will be set to 1 or 0
def gen_string(length: int):
	return random.choices([0, 1], length)  # Produces a list of randomly selected 1's and 0's of the same length as str

def gen_population(length: int, size: int):
	return [gen_string(length) for _ in size]

# TODO: Generate next generation of candidate solutions using fitness_proportionate roulette wheel selection
def next_gen():
	return

# Evaluates the candidate string
def eval(cand, short_str, long_str):

	sub_str = ""

	for i, bit in enumerate(cand):  # Produces the substring represented by the candidate binary string
		if bit:
			sub_str += short_str[i]

	j = 0
	match = False

	for char in long_str:  # Searches through the longer of the strings to see if it contains the substring
		if sub_str[j] == char:
			j += 1
		if j == len(sub_str):
			match = True
			break

	val = len(cand)  # Initial val equals the length of the candidate
	if match:  # If the candidate matches, it's value is multiplied by 100, else it is negatively multiplied by 1000
		val *= 100
	else:
		val *= -1000

	if len(cand) == len(short_str):  # If the candidate is the length of the shortest string, it gets a bonus
		val *= 10

	return val  # Return the produced value of the candidate


if __name__ == "__main__":
	test_cand = gen_string(len(short_str))
	print(test_cand)
	print(eval(test_cand, short_str, long_str))