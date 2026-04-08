# Problem Statement:
# Optimization of genetic algorithm parameter in hybrid genetic algorithm-neural network modelling:
# Application to spray drying of coconut milk.

import random
from deap import base, creator, tools, algorithms

# -------------------------------
# Evaluation Function (Mock)
# -------------------------------
def evaluate(individual):
    # 'individual' represents NN parameters
    # Currently using random fitness (dummy)
    return (random.random(),)


# -------------------------------
# GA Parameters
# -------------------------------
POPULATION_SIZE = 10
GENERATIONS = 5


# -------------------------------
# Create Fitness & Individual
# (Fixed warning issue)
# -------------------------------
if "FitnessMin" not in creator.__dict__:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

if "Individual" not in creator.__dict__:
    creator.create("Individual", list, fitness=creator.FitnessMin)


# -------------------------------
# Toolbox Initialization
# -------------------------------
toolbox = base.Toolbox()

# Attributes
toolbox.register("attr_neurons", random.randint, 1, 100)
toolbox.register("attr_layers", random.randint, 1, 5)

# Individual & Population
toolbox.register(
    "individual",
    tools.initCycle,
    creator.Individual,
    (toolbox.attr_neurons, toolbox.attr_layers),
    n=1
)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# -------------------------------
# Genetic Operators
# -------------------------------
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=100, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)


# -------------------------------
# Create Population
# -------------------------------
population = toolbox.population(n=POPULATION_SIZE)


# -------------------------------
# Run Genetic Algorithm
# -------------------------------
for gen in range(GENERATIONS):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

    fitnesses = list(map(toolbox.evaluate, offspring))

    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit

    population = toolbox.select(offspring, k=len(population))


# -------------------------------
# Best Individual
# -------------------------------
best_individual = tools.selBest(population, k=1)[0]
best_params = best_individual


# -------------------------------
# Output
# -------------------------------
print("Best Parameters:", best_params)