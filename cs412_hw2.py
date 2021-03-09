import random

# Fitness function
def eval(id):
	val = 21.5 + id[0] * math.sin(4 * math.pi * id[0]) + id[1] * math.sin(20 * math.pi * id[1])
	return val

# Produces one child
def recombination(parent_pool):
	# select two parents
	parents = random.choices(parent_pool, k=2)
	# get the length of the genotype
	genolen = len(parents[0])
	
	child = [random.choice([parents[0][i], parents[1][i]]) for i in range(genolen)]
	
	return child

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
		