########################################################################################################################
# NAME: Sha Jackson and Benjamin Good
# COURSE: CSCE 412 - Evolutionary Computing, Frank Moore
# ASSIGNMENT: Final Project - Solving the Subset Sum Problem Using Genetic Algorithms
# DESCRIPTION:
#
########################################################################################################################

import random
import os

POP_SIZE = 500

num_list = [1]  # Default

TEST_DRIVER = True


# This effectively performs a coin flip at each index to determine whether the bit will be set to 1 or 0
def gen_list(length: int):
    return "".join(random.choices(["0", "1"], k=length))  # Produces a list of randomly selected 1's and 0's of the same length as str


# Generates a population of genomes (substrings)
def gen_population(length: int, size: int):
    return [gen_list(length) for _ in range(size)]


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


def translate_candidate(cand_list, num_list):

    out_list = []

    for i, bit in enumerate(cand_list):  # Produces the sum represented by the candidate list
        if int(bit):
            out_list.append(num_list[i])

    return out_list


# Evaluates the candidate string
def eval(cand_list, num_list, num_sum):

    cand_size = 0
    cand_sum = 0

    for i, bit in enumerate(cand_list):  # Produces the sum represented by the candidate list
        if int(bit):
            cand_sum += num_list[i]

    # Fitness = difference between desired sum and candidate sum with added weight towards less elements used
    # val = abs(num_sum - cand_sum) + ((cand_size - 1) * 0.1)
    val = abs(num_sum - cand_sum)

    return val  # Return the produced value of the candidate


# Main subset sum function
def subsetsum(num_list, num_sum, generation_cap, prob_mutate=1/len(num_list), num_mutations=1, prob_cross=.95):

    p = gen_population(len(num_list), POP_SIZE)  # Initialize population of candidate subsets
    pop = [p, [eval(cand_list, num_list, num_sum) for cand_list in p]]  # Pair population with respective fitness levels

    best_fit = float('inf')  # Best fitness found
    best_subset = []  # Best subset found
    best_g = 0  # Amount of generations to best subset

    for gen in range(generation_cap):  # Loop for generation cap times

        pop[1], pop[0] = (list(t) for t in zip(*sorted(zip(pop[1], pop[0]))))  # Sort the population based on fitness levels
        if best_fit > pop[1][0]:  # Update the best current best subset as necessary
            best_subset = pop[0][0]
            best_fit = pop[1][0]
            best_g = gen+1
        elif best_fit == pop[1][0] and len(pop[0][0]) < len(best_subset):
            best_subset = pop[0][0]
            best_fit = pop[1][0]
            best_g = gen + 1

        #if best_fit == 0:  # Break if we've reached our fitness limit
        #    break

        next_gen = [pop[0][0:2], pop[1][0:2]]  # Start the next generation with the two best strings from the previous

        for i in range(int(len(pop[0]) / 2) - 1):  # Loop through the previous population, generating two children per pair of strings selected (roulette wheel selection)

            parents = select_next_gen(pop)  # Select parents (roulette)
            a, b = sp_crossover(parents[0], parents[1], prob_cross)  # Crossover
            a = mutate(a, prob_mutate, num_mutations)  # Mutate first child
            b = mutate(b, prob_mutate, num_mutations)  # Mutate second child
            next_gen[0].extend([a, b])  # Add strings to next generation
            next_gen[1].extend([eval(a, num_list, num_sum), eval(b, num_list, num_sum)])  # Add fitness levels of new strings

        pop = next_gen  # Replace previous generation with next

    pop[1], pop[0] = (list(t) for t in zip(*sorted(zip(pop[1], pop[0]))))  # Final sort of generation

    if best_fit > pop[1][0]:  # Update the best current best subset as necessary
        best_subset = pop[0][0]
        best_fit = pop[1][0]
        best_g = generation_cap
    elif best_fit == pop[1][0] and len(pop[0][0]) < len(best_subset):
        best_subset = pop[0][0]
        best_fit = pop[1][0]
        best_g = generation_cap

    return translate_candidate(pop[0][0], num_list), best_g


def test_driver():

    for filename in os.listdir("Test Data"):
        if filename.endswith(".txt"):

            num_list = []

            with open("Test Data/" + filename) as file:
                for line in file:
                    num_list.append(int(line))

            generation_cap = num_list.pop()
            num_sum = num_list.pop()

            subset, gens = subsetsum(sorted(num_list), num_sum, generation_cap)

            print(f"The best subset found from {filename} for the sum of {num_sum} was {subset} in {gens} generations.\nThe sum of the subset is {sum(subset)}")


if __name__ == "__main__":

    print("Welcome to the Subset Sum Solver...\n")

    print("Would you like to run the test driver (if no, you will be prompted to input a subset yourself). Y/N?")
    while True:
        userin = input()
        if userin.upper() == "Y":
            test_driver()
            break
        elif userin.upper() == "N":
            while True:
                try:
                    num_list = list(map(int, input("Enter a list of space separated integers: ").split()))
                    num_sum = int(input("Enter a number representing the sum you would like to search for: "))
                    break
                except():
                    print("Invalid list of numbers given")

            generation_cap = int(input("Enter the maximum number of generations: "))

            print(subsetsum(num_list, num_sum, generation_cap))
            break
        else:
            print("Invalid input given")

