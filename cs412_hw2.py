# Benjamin Good and Sha Jackson
# bcgood@alaska.edu and shajack2000@gmail.com
# 3/22/2021

import random, math
from numpy import random as nprand

# Fitness function
def eval(x):
	val = 21.5 + x[0] * math.sin(4 * math.pi * x[0]) + x[1] * math.sin(20 * math.pi * x[1])
	return val
	
# individual will consist of two x values and the mutation step	
def init_pool(poolsize):
	pool = [random.uniform(-3.0, 12.0), random.uniform(4.0, 6.0), 1]
	return pool

# Produces one child
def recombination(parent_pool):
	# select two parents
	parents = random.choices(parent_pool, k=2)
	# get the length of the genotype
	genolen = len(parents[0])
	
	child = [random.choice([parents[0][i], parents[1][i]]) for i in range(genolen)]
	
	return child

# based on mutation case #1
def mutstep(sigma):
	n = 3
	tao = 1/math.sqrt(2*n)
	sigma_p = sigma*math.exp(tao*nprand.normal(0, sigma, 100))
	return sigma_p

# changes the mutation step
def adjust_mutstep(sigma, prob, c):
	
	# Adjust the mutation step depending on the differences in fitness.
	if prob > 0.2:
		sigma = sigma / c
	elif prob < 0.2:
		sigma = sigma * c
	
	return sigma


def mutation(ind):
	# mutation equation: x' = x + N(0, sigma)
	sigma = ind[2]
	for i in range(2):
		ind[i] = ind[i] + nprand.normal(0, sigma, 100)
	# Possible TODO: check to see if fitness is better due to mutation and
	# revert back to original values it it isn't.
	
	return ind
		

# Global recombination, taking the current population, number of parents(np)
# and number number of offspring(no) as arguments
def globalrec(pool, np, no):
	offspring_pool = []
	# This looks very inefficient, but it is a start.
	for i in range(no):
		child = recombination(pool)
		
		# Check to see if the length of the population has been exceed
		# and then check if any individuals currently in the offspring pool
		# have a lower fitness value than the newly created child,
		# otherwise just add the child to the offspring pool.
		
		if i > np:
			child_fitness = eval(child)
			for j in range(len(offspring_pool)):
				ind = offspring_pool[j]
				
				if eval(ind) < child_fitness:
					offspring_pool.remove(ind)
					offspring_pool.append(child)
		else:
			offspring_pool.append(child)
	
	return offspring_pool

def main(poolsize, generations, k):
	pool = init_pool(poolsize)
	
	
		