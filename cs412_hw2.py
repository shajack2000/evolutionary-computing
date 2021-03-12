# Benjamin Good and Sha Jackson
# bcgood@alaska.edu and shajack2000@gmail.com
# 3/22/2021

import random, math
from numpy import random as nprand
import decimal

# Fitness function
def eval(x):
	if x[0] < -3.0 or x[0] > 12.0 or math.isnan(x[0]) or math.isinf(x[0]):
		return -100
	if x[1] < 4.0 or x[1] > 6.0 or math.isnan(x[1]) or math.isinf(x[1]):
		return -100
	val = 21.5 + x[0] * math.sin(4 * math.pi * x[0]) + x[1] * math.sin(20 * math.pi * x[1])
	return val
	
# An individual will consist of two x values and two mutation steps.	
def init_pool(poolsize, sigma):
	pool = [ [random.uniform(-3.0, 12.0), random.uniform(4.0, 6.0), sigma, sigma] for i in range(poolsize)]
	return pool

# Produces one child
def recombination(parent_pool):	
	child = []
	
	# Index 0 and 1 will contain x values selected via discrete global recombination.
	for i in range(2):
		parents = random.choices(parent_pool, k=2)
		child.append(random.choice([parents[0][i], parents[1][i]]))
	
	# Index 2 and 3 will contain sigma values seleccted via intermediary global recombination.
	for i in range(2, 4):
		parents = random.choices(parent_pool, k=2)
		avg = (parents[0][i] + parents[1][i]) / 2
		child.append(avg)
	
	return roundind(child)

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
	
	return round(sigma, 4)

# checks of x values
def check_viability(x):
	if x[1] < 4.0 or x[1] > 6.0:
		return False
	if x[0] < -3.0 or x[0] > 12.0:
		return False
	return True

# based on mutation case #2
def mutation(ind):
	# mutation equation: sigma' = sigma * exp(tao' * N(0,1) + tao * N'(0, 1))
	# x' = x + sigma' * N(0, 1)
	mut_ind = ind
	n = 4
	tao_p = 1/math.sqrt(2*n)
	tao = 1/math.sqrt(2*math.sqrt(n))
	global_distr = nprand.normal(0, 1)
	
	for i in range(2):
		sigma = ind[i+2]
		sigma_p = sigma * math.exp(tao_p * global_distr + tao * nprand.normal(0, 1))
		mut_ind[i+2] = sigma_p
		mut_ind[i] = ind[i] + sigma_p * nprand.normal(0, 1)
	
	mut_ind = roundind(mut_ind)
	
	if nanorinf(mut_ind):
		return ind
	
	if eval(mut_ind) > eval(ind):
		return mut_ind
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
					break
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

# tries to round all of the values in a chromosome
def roundind(ind):

	for i in ind:
		i = round(i, 4)
	
	print(ind)
	return ind

# checks for nan or inf
def nanorinf(ind):
	for c in ind:
		if math.isnan(c) or math.isinf(c):
			return True
	
	return False

def main(poolsize, generations, k, np = 3, no = 21):
	pool = init_pool(poolsize, 1)
	
	# Maintain a count of the generation to check for k iterations.
	gen_counter = 0
	
	# Declare a variable to count the number of successful mutations.
	success = 0
	
	for g in range(generations):
		gen_counter += 1
		
		pool = globalrec(pool, np, no)
		
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
				ind[3] = adjust_mutstep(ind[3], prob_succ, random.uniform(0.8, 1.0))
			# Reset the success and gen_counter variables for future calculations.
			success = 0
			gen_counter = 0
	
	# Return the fittest individual.
	# print(pool) I was printing the pool to see where the program is going wrong.
	best = get_highest_fitness(pool)
		
	return best

if __name__ == "__main__":
	values = main(10, 10000, 10)
	
	print(values)