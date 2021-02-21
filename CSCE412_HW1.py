########################################################################################################################
# NAME: Sha Jackson and Benjamin Good
# COURSE: CSCE 412 - Evolutionary Computing, Frank Moore
# ASSIGNMENT: Project 1 - Genetic Algorithms
# DESCRIPTION: Uses genetic algorithm methods like single-point crossover
# 				and single point mutation to solve the LCS problem
#
# HELPFUL SOURCES:
#	- https://www.youtube.com/watch?v=nhT56blfRpE&ab_channel=KieCodes
#	- http://gpbib.cs.ucl.ac.uk/gecco2006/docs/p609.pdf
########################################################################################################################

# TODO:
#		- Comment
#		- User input for probabilites
#		- test driver
#		- summarize report

import random

MATCH_MULTI = 100
DIFF_MULTI = -1000
MAX_MULTI = 10
POP_SIZE = 100

userstr1 = str.lower(input("Enter the first string: "))
userstr2 = str.lower(input("Enter the second string: "))
known_lcs = str.lower(input("Enter the known LCS (or nothing if it is unknown): "))
generation_cap = int(input("Enter the maximum number of generations: "))

short_str = userstr1
long_str = userstr2

if len(long_str) < len(short_str):
	short_str, long_str = long_str, short_str


# This effectively performs a coin flip at each index to determine whether the bit will be set to 1 or 0
def gen_string(length: int):
	return "".join(random.choices(["0", "1"], k=length))  # Produces a list of randomly selected 1's and 0's of the same length as str


# Generates a population of genomes (substrings)
def gen_population(length: int, size: int):
	return [gen_string(length) for _ in range(size)]


# Selects two parents from the previous population to reproduce (using roulette wheel selection)
def select_next_gen(population):
	return random.choices(population=population[0], weights=population[1], k=2)


# Perform single point crossover on two parent substrings, producing two new children substrings
def sp_crossover(str1, str2, prob):

	if len(str1) != len(str2):  # Ensure that parents are the same length otherwise crossover doesn't work
		raise ValueError("Genomes must have the same length for crossover")

	if len(str1) < 2 or random.random() > prob:  # Ensure that the two strings are at least of length 2, otherwise, crossover is meaningless
		return str1, str2
	else:
		x_point = random.randint(1, len(str1) - 1)  # Select a random point to perform crossover on the substrings
		return str1[:x_point] + str2[x_point:], str2[:x_point] + str2[x_point:]


# Mutate the given substring, num_mutations times, with prob probability
def mutate(genome, prob, num_mutations):

	for _ in range(num_mutations):
		index = random.randrange(len(genome))  # Select random index from the given substring to possibly mutate
		genome = genome if random.random() > prob else genome[:index] + str(abs(int(genome[index]) - 1)) + genome[index+1:]  # Flips 0's and 1's
	return genome

def bits_to_str(bits, short_str):
	sub_str = ''
	for i, bit in enumerate(bits):  # Produces the substring represented by the candidate binary string
		if int(bit):
			sub_str += short_str[i]
	return sub_str


# Evaluates the candidate string
def eval(cand, short_str, long_str):

	sub_str = bits_to_str(cand, short_str)

	j = 0
	match = False

	for char in long_str:  # Searches through the longer of the strings to see if it contains the substring
		if j == len(sub_str):
			match = True
			break
		if sub_str[j] == char:
			j += 1

	val = len(sub_str)  # Initial val equals the length of the candidate
	if match:  # If the candidate matches, it's value is multiplied by 100, else it is negatively multiplied by 1000
		val *= MATCH_MULTI
	else:
		val *= DIFF_MULTI

	if len(sub_str) == len(short_str):  # If the candidate is the length of the shortest string, it gets a bonus
		val *= MAX_MULTI

	return val  # Return the produced value of the candidate

# Main lcs function
def lcs(short_str, long_str, generation_cap, fitness_lim, prob_mutate=1/len(short_str), num_mutations=1, prob_cross=.95):

	p = gen_population(len(short_str), POP_SIZE)
	pop = [p, [eval(cand, short_str, long_str) for cand in p]]

	best = ""
	best_g = 0

	for gen in range(generation_cap):

		pop[1], pop[0] = (list(t) for t in zip(*sorted(zip(pop[1], pop[0]), reverse=True)))
		if best != pop[0][0]:
			best = pop[0][0]
			best_g = gen

		if pop[1][0] >= fitness_lim:
			break

		next_gen = [pop[0][0:2], pop[1][0:2]]

		for i in range(int(len(pop[0]) / 2) - 1):

			parents = select_next_gen(pop)
			a, b = sp_crossover(parents[0], parents[1], prob_cross)
			a = mutate(a, prob_mutate, num_mutations)
			b = mutate(b, prob_mutate, num_mutations)
			next_gen[0].extend([a, b])
			next_gen[1].extend([eval(a, short_str, long_str), eval(b, short_str, long_str)])

		pop = next_gen

	pop[1], pop[0] = (list(t) for t in zip(*sorted(zip(pop[1], pop[0]), reverse=True)))
	return pop[0][0], best_g+1

def test_driver():
	return

if __name__ == "__main__":
	if known_lcs != '':
		fitness_lim = len(known_lcs) * MATCH_MULTI
		if len(known_lcs) == len(short_str):
			fitness_lim *= MAX_MULTI
	else:
		fitness_lim = len(short_str) * MATCH_MULTI * MAX_MULTI
	ans, gen = lcs(short_str, long_str, generation_cap, fitness_lim)
	print(f"The Longest Common Substring of {short_str.upper()} and {long_str.upper()} after {gen} generations is {bits_to_str(ans, short_str).upper()} and is represented by the bitstring {ans}")