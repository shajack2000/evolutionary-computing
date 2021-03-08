import random

# Produces one child
def recombination(parent_pool):
	# select two parents
	parents = random.choices(parent_pool, k=2)
	# get the length of the genotype
	genolen = len(parents[0])
	
	child = [random.choice([parents[0][i], parents[1][i]]) for i in range(genolen)]
	
	return child

# Global recombination
def globalrec(pool, np, no):
	pass

# Fitness function
def eval(id):
	val = 21.5 + id[0] * math.sin(4 * math.pi * id[0]) + id[1] * math.sin(20 * math.pi * id[1])
	return val