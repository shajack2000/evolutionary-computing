# Benjamin Good and Sha Jackson
# bcgood@alaska.edu and shajack2000@gmail.com
# 3/22/2021

import random, math
from numpy import random as nprand
import decimal

PI = decimal.Decimal(math.pi)

# Fitness function
def eval(x):
	viable = True
	val = 0
	
	if x[0] < -3.0 or x[0] > 12.0:
		val -= 50
	# trying to guide x[1] closer to the valid range
	if x[1] < 0.0 or x[1] > 10.0:
		val -= 200
	elif x[1] < 2.0 or x[1] > 8.0:
		val -= 100
	elif x[1] < 4.0 or x[1] > 6.0:
		val -= 50
	if viable == 0:
		val = 21.5 + x[0] * math.sin(4 * math.pi * x[0]) + x[1] * math.sin(20 * math.pi * x[1])
		
	return val
	
# An individual will consist of two x values and two mutation steps.	
def init_pool(poolsize, sigma):
	pool = [ [random.uniform(-3.0, 12.0), random.uniform(4.0, 6.0), 
	sigma, sigma] for i in range(poolsize)]
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

# checks viability of x values
def check_viability(x):
	if x[1] < 4.0 or x[1] > 6.0:
		return False
	if x[0] < -3.0 or x[0] > 12.0:
		return False
	return True

# based on mutation case #2
def mutation(ind):
	# mutation equation: sigma' = sigma * exp(tao' * N(0,1) + tao * N'(0, 1))
	# x' = x + sigma' * N'(0, 1)
	mut_ind = ind.copy()
	n = 2
	tao_p = 1/math.sqrt(2*n)
	tao = 1/math.sqrt(2*math.sqrt(n))
	global_distr = nprand.normal(0, 1)
	
	for i in range(2):
		sigma = ind[i+2]
		sigma_p = sigma * math.exp((tao_p * global_distr) + (tao * nprand.normal(0, 1)) )
		mut_ind[i+2] = sigma_p
		mut_ind[i] = ind[i] + sigma_p * nprand.normal(0, 1)
	
	if nanorinf(mut_ind):
		return ind
	
#	print("chromosome: {}, mutated chromosome: {}, chromosome fitness: {}, mutant fitness: {}".format(ind, mut_ind, eval(ind), eval(mut_ind)))
#	print("Break")
	if eval(mut_ind) > eval(ind):
		return mut_ind
	return ind

def get_lowest_fitness(pool):
	worst = None
	worst_fitness = 0
	for ind in pool:
		fitness = eval(ind)
		if worst is None:
			worst = ind
			worst_fitness = fitness
		elif fitness < worst_fitness:
			worst = ind
			worst_fitness = fitness
	
	return worst

# Global recombination, taking the current population, number of parents(np)
# and number of offspring(no) as arguments
def globalrec(pool, np, no):
	offspring_pool = []
	# This looks very inefficient, but it is a start.
	for i in range(no):
		child = recombination(pool)
		
		# Check to see if the length of the population has been exceed
		# and then check if the least fit individual currently in the offspring pool
		# has a lower fitness value than the newly created child,
		# otherwise just add the child to the offspring pool.
		
		if i > np:
			child_fitness = eval(child)
			worst = get_lowest_fitness(offspring_pool)
			if child_fitness > eval(worst):
				offspring_pool.remove(worst)
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

# tries to round all of the values in an individual
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
	
	# I had to revise some of the source code using the decimal module.
	decimal.getcontext().prec = 5
	
	for g in range(generations):
#		gen_counter += 1
		
		pool = globalrec(pool, np, no)
		
		# Commenting out the 1/5 success part
		
		for ind in pool:
			# Compare the fitness of the original values to the mutated
#			og_fitness = eval(ind)
			ind = mutation(ind)
#			mut_fitness = eval(ind)
			
#			if mut_fitness > og_fitness:
#				# Increment the success counter if the mutated values lead to
#				# greater fitness.
#				success += 1

#		if gen_counter == k:
#			# Calculate the % of successful mutations.
#			prob_succ = success / (poolsize * k)
#			for ind in pool:
#				r1 = decimal.Decimal(random.uniform(0.8, 1.0))
#				r2 = decimal.Decimal(random.uniform(0.8, 1.0))
#				ind[2] = adjust_mutstep(ind[2], prob_succ, r1)
#				ind[3] = adjust_mutstep(ind[3], prob_succ, r2)
#			# Reset the success and gen_counter variables for future calculations.
#			success = 0
#			gen_counter = 0
	
	# Return the fittest individual.
	# I was printing the pool to see where the program is going wrong.
#	for p in pool:
#		print(p)
#		print(p[0])
#		print(p[1])
#		print(eval(p))
#		print("End of genotype")
	best = get_highest_fitness(pool)
		
	return best

if __name__ == "__main__":
	values = main(10, 1000, 10)
	
	print(values)