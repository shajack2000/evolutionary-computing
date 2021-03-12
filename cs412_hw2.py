# Benjamin Good and Sha Jackson
# bcgood@alaska.edu and shajack2000@gmail.com
# 3/22/2021

import random, math
from numpy import random as nprand

# Fitness function
def eval(x):
	if x[0] < -3.0 or x[0] > 12.0:
		return -100
	if x[1] < 4.0 or x[1] > 6.0:
		return -100
	val = 21.5 + x[0] * math.sin(4 * math.pi * x[0]) + x[1] * math.sin(20 * math.pi * x[1])
	return val
	
# An individual will consist of two x values and the mutation step.	
def init_pool(poolsize):
	pool = [ [random.uniform(-3.0, 12.0), random.uniform(4.0, 6.0), 1] for i in range(poolsize)]
	return pool

# Produces one child
def recombination(parent_pool, sigma):
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
	sigma_p = sigma*math.exp(tao*nprand.normal(0, sigma))
	return sigma_p

# changes the mutation step
def adjust_mutstep(sigma, prob, c):
	
	# Adjust the mutation step depending on the differences in fitness.
	if prob > 0.2:
		sigma = sigma / c
	elif prob < 0.2:
		sigma = sigma * c
	
	return sigma

# checks of x values
def check_viability(x):
	if x[1] < 4.0 or x[1] > 6.0:
		return False
	if x[0] < -3.0 or x[0] > 12.0:
		return False
	return True

def mutation(ind):
	# mutation equation: x' = x + sigma * N(0, sigma')
	sigma = ind[2]
	mut_ind = ind
	sigma_prime = mutstep(sigma)
	mut_ind[2] = sigma_prime
	for i in range(2):
		mut_ind[i] = mut_ind[i] + sigma * nprand.normal(0, sigma_prime)
	
	if eval(mut_ind) > eval(ind):
		return mut_ind
	return ind

# Global recombination, taking the current population, number of parents(np)
# and number number of offspring(no) as arguments
def globalrec(pool, sigma, np, no):
	offspring_pool = []
	# This looks very inefficient, but it is a start.
	for i in range(no):
		child = recombination(pool, sigma)
		
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

# Returns the fittest individual in the pool.
def get_highest_fitness(pool):
	best = None
	best_fitness = 0
	for ind in pool:
		fitness = eval(ind)
		if best is None:
			best = ind
			best_fitness = fitness
		elif fitness > best_fitness:
			best = ind
			best_fitness = fitness
	
	return ind

def main(poolsize, generations, k, np = 3, no = 21):
	pool = init_pool(poolsize)
	
	# Maintain a count of the generation to check for k iterations.
	gen_counter = 0
	
	sigma = 1
	
	# Declare a variable to count the number of successful mutations.
	success = 0
	
	for g in range(generations):
		gen_counter += 1
		
		pool = globalrec(pool, sigma, np, no)
		
		for ind in pool:
			# Compare the fitness of the original values to the mutated
			og_fitness = eval(ind)
			ind = mutation(ind)
			mut_fitness = eval(ind)
			
			if mut_fitness > og_fitness:
				# Increment the success counter if the mutated values lead to
				# greater fitness.
				success += 1
		
		if gen_counter == k:
			# Calculate the % of successful mutations.
			prob_succ = success / (poolsize * k)
			for ind in pool:
				ind[2] = adjust_mutstep(ind[2], prob_succ, random.uniform(0.8, 1.0))
			# Reset the success and gen_counter variables for future calculations.
			success = 0
			gen_counter = 0
	
	# Return the fittest individual.
	
	best = get_highest_fitness(pool)
		
	return best

if __name__ == "__main__":
	values = main(10, 10000, 10)
	
	print(values)