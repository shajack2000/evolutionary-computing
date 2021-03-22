########################################################################################################################
# NAME: Benjamin Good and Sha Jackson
# COURSE: CSCE 412 - Evolutionary Computing, Frank Moore
# ASSIGNMENT: Project 2 - Evolution Strategies
# DESCRIPTION: Implements evolutionary strategies to maximize the function
#
#               f(x1, x1) = 21.5 + x1 * sin(4*pi*x1) + x2 * sin(20*pi*x2)
#
#               within the constraints:
#                   -3.0 <= x1 <= 12.0\n4.0 <= x2 <= 6.0
#
########################################################################################################################

import random, math
from numpy import random as nprand

NUMBER_PARENTS = 3
NUMBER_OFFSPRING = 21
MUTATION_STEP_SIZE = 1
TERMINATION_COUNT = 10000
N_TAU = 2
SEED = 1337

# Fitness function
def eval(x):
    viable = True
    val = 0

    if x[0] < -3.0 or x[0] > 12.0:
        val -= 50

    if x[1] < 4.0 or x[1] > 6.0:
        val -= 50
    if val == 0:
        val = 21.5 + x[0] * math.sin(4 * math.pi * x[0]) + x[1] * math.sin(20 * math.pi * x[1])

    return val


# An individual will consist of two x values and two mutation steps.
def init_pool(poolsize, sigma):
    pool = [[random.uniform(-3.0, 12.0), random.uniform(4.0, 6.0),
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


# based on mutation case #2
def mutation(ind):
    # mutation equation: sigma' = sigma * exp(tao' * N(0,1) + tao * N'(0, 1))
    # x' = x + sigma' * N'(0, 1)
    mut_ind = ind.copy()
    n = N_TAU
    tao_p = 1 / math.sqrt(2 * n)
    tao = 1 / math.sqrt(2 * math.sqrt(n))
    global_distr = nprand.normal(0, 1)

    for i in range(2):
        sigma = mut_ind[i + 2]
        sigma_p = sigma * math.exp((tao_p * global_distr) + (tao * nprand.normal(0, 1)))
        mut_ind[i + 2] = sigma_p
        mut_ind[i] = mut_ind[i] + sigma_p * nprand.normal(0, 1)

    return mut_ind


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


# returns a pool of the n fittest members in the pool passed to it.
def pool_selection(pool, size):
    fit_pool = []
    for i in range(size):
        ind = get_highest_fitness(pool)
        pool.remove(ind)
        fit_pool.append(ind)

    return fit_pool


# Global recombination, taking the current population, number of parents(np)
# and number of offspring(no) as arguments
def globalrec(pool, np, no, k):
    offspring_pool = []

    for i in range(no):
        child = recombination(pool)

        child = mutation(child)

        # now just append to pool and pass it to another function
        # that returns a pool of the fittest individuals

        offspring_pool.append(child)

    return pool_selection(offspring_pool, np)


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

    return best


# checks for nan or inf
def nanorinf(ind):
    for c in ind:
        if math.isnan(c) or math.isinf(c):
            return True

    return False


def main(generations, np=NUMBER_PARENTS, no=NUMBER_OFFSPRING):
    pool = init_pool(np, MUTATION_STEP_SIZE)

    # Maintain a count of the generation to check for k iterations.
    gen_counter = 0

    # Declare a variable to count the number of successful mutations.
    success = 0

    for g in range(generations):

        gen_counter += 1

        pool = globalrec(pool, np, no, gen_counter)

    best = get_highest_fitness(pool)

    return (best[0], best[1])

def getUserInput():
    print("Welcome\n\nThis program implements evolutionary strategies to maximize the folllowing function:\n")
    print("f(x1, x1) = 21.5 + x1 * sin(4*pi*x1) + x2 * sin(20*pi*x2)\n")
    print("within the constraints: \n-3.0 <= x1 <= 12.0\n4.0 <= x2 <= 6.0\n")

    SEED = get_int("\nEnter the random seed to be used in generation (any number will do): ")
    NUMBER_PARENTS = get_int("\nEnter the number of parents for each offspring (rec. 3): ")
    NUMBER_OFFSPRING = get_int("\nEnter the number of offspring produced each generation (rec. 21): ")
    print("\nCurrently only (Mu, Lamba) selection is available so we will skip that parameter input...")
    MUTATION_STEP_SIZE = get_int("\nEnter the initial value of the mutation step size in each dimension (rec. 1): ")
    TERMINATION_COUNT = get_int("\nEnter the number of fitness evaluations to be run (rec. 10000): ")
    N_TAU = get_int("\nEnter the number, N, to calculate Tau (rec. 2) where\n\nt` = 1 / sqrt(2 * n)\nt = 1 / sqrt(2 * sqrt(n))\n")
    print("\nComputing...\n")


def get_int(message):
    try:
        userIn = int(input(message))
        if isinstance(userIn, int):
            return userIn
    except:
        print("An invalid input was given. Please try again.")


if __name__ == "__main__":

    getUserInput()

    random.seed(SEED)
    values = main(TERMINATION_COUNT)

    print("Best (x1, x2) found:")
    print("f({}, {}) = {}".format(values[0], values[1], eval(values)))