# Benjamin Good and Sha Jackson
# bcgood@alaska.edu and shajack2000@gmail.com
import string
import random

userstr1 = input("Enter the first string: ")
userstr2 = input("Enter the second string: ")
gen_limit = input("Enter the number of generations to simulate: ")
k = len(userstr1)
ref = userstr1

if len(userstr2) < len(userstr1):
	k = len(userstr2)
	ref = userstr2
	
# This effectively performs a coin flip at each index to determine whether the bit will be set
# to 1 or 0
def gen_string(str):
	new_str = ""
	for s in str:
		if random.randint(1, 2) == 1:
			new_str = new_str + "0"
		else:
			new_str = new_str + "1"
	return new_str

# This iterates through the candidate string and tests if the two strings the user entered
# match at any index where a bit is set to 1.
def eval(cand, str1, str2):
	score = 0
	for i in range(len(cand)):
		if cand[i] == "1":
			if str1[i] == str2[i]:
				score += 1
				# print("hit")
			else:
				score -= 1
				# print("miss")
	return score

def crossover(p1, p2):
	point = random.randint(0, len(p1) - 1)
	c1 = p1[0:point] + p2[point:]
	c2 = p2[0:point] + p2[point:]
	return c1, c2

def mutation(geno):
	for g in geno:
		pm = random.randint(1, len(geno))
		if pm == 1:
			if g == "0":
				g = "1"
			else:
				g = "0"
	return geno

def gen_population(poplen):
	population = []
	for i in range(poplen):
		population.append(gen_string(ref))
		
	return population

def parent_selection(pop, w):
	return random.choices(pop, weights = w, k = 2)

def lcs(str1, str2, gen_limit):
	# generate the initial population
	pop = gen_population(100)
	
	fitlim = k
	
	for g in range(gen_limit):
		# data structures for storing population fitness, weights for parent selection, and the next generation
		pop_fitness = []
		pop_weights = []
		new_gen = []
		
		for i in pop:
			val = eval(i, str1, str2)
			# immediately return solution if its value equals k
			if val == k:
				return i
			pop_fitness.append(val)
			pop_weights.append(val)
			
			# previous approad to adding weights
#			if val > 0:
#				pop_weights.append(3)
#			elif val < 0:
#				pop_weights.append(2)
#			else:
#				pop_weights.append(1)
		
				
		for o in range(len(pop) // 2):
			parents = parent_selection(pop, pop_weights)
			c1, c2 = crossover(parents[0], parents[1])
			c1 = mutation(c1)
			c2 = mutation(c2)
			new_gen.append(c1)
			new_gen.append(c2)
		
		pop = new_gen
	
	fittest = None
	fit_val = None
	
	for i in pop:
		val = eval(i, str1, str2)
		if fittest is None or val > fit_val:
			fittest = i
			fit_val = val
	
	return fittest

if __name__ == "__main__":
	geno = lcs(userstr1, userstr2, int(gen_limit))
	out = ""
	for i in range(k):
		if geno[i] == '1':
			out += ref[i]
	print(out)