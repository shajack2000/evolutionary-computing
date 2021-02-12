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

import random

userstr1 = input("Enter the first string: ")
userstr2 = input("Enter the second string: ")
generation_cap = input("Enter the maximum number of generations")

short_str = userstr1
long_str = userstr2

if len(long_str) < len(short_str):
	short_str, long_str = long_str, short_str


# This effectively performs a coin flip at each index to determine whether the bit will be set to 1 or 0
def gen_string(length: int):
	return random.choices(["0", "1"], k=length)  # Produces a list of randomly selected 1's and 0's of the same length as str


# Generates a population of genomes (substrings)
def gen_population(length: int, size: int):
	return [gen_string(length) for _ in range(size)]


# Selects two parents from the previous population to reproduce (using roulette wheel selection)
def select_next_gen(population):
	return random.choices(population=population[0], weights=population[1], k=2)


# Perform single point crossover on two parent substrings, producing two new children substrings
def sp_crossover(str1, str2):

	if len(str1) != len(str2):  # Ensure that parents are the same length otherwise crossover doesn't work
		raise ValueError("Genomes must have the same length for crossover")

	if len(str1) < 2:  # Ensure that the two strings are at least of length 2, otherwise, crossover is meaningless
		return str1, str2
	else:
		x_point = random.randint(1, len(str1) - 1)  # Select a random point to perform crossover on the substrings
		return str1[0:x_point] + str2[x_point:0], str2[0:x_point] + str2[x_point:0]


# Mutate the given substring, num_mutations times, with prob probability
def mutate(genome, num_mutations=1, prob=0.5):

	for _ in range(num_mutations):
		index = random.randrange(len(str))  # Select random index from the given substring to possibly mutate
		genome[index] = genome[index] if random.random() > prob else str(abs(int(genome[index]) - 1))  # Flips 0's and 1's
	return genome


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


# Main lcs function
def lcs(short_str, long_str, generation_cap):

	# TODO: Calculate fitness limit

	# TODO: Generate genome population and their individual fitness

	# TODO: Loop generation_cap times

		# TODO: Sort genomes by fitness

		# TODO: Check if fitness limit has been met (break if so)

		# TODO: Produce next generation
		#		- select the two best from previous gen
		#		- loop half population length - 1 times
		#			- select two parents with selection function
		#			- apply crossover and mutation functions to the two children generated
		# 			- append children to the next generation

		# TODO: Population = next generation

	# TODO: Return best genome

	return


if __name__ == "__main__":
	lcs(short_str, long_str, generation_cap)