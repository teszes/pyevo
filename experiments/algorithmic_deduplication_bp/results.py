import os
from pickle import load

from matplotlib import pyplot as plt

plt.figure()
plt.title('Algorithmic identity')
plt.xlabel('Generation')
plt.ylabel('Max fitness')
axes = plt.gca()
axes.set_ylim([0, 1])

for file_number in range(len(os.listdir("raw_results"))):
    try:
        with open("raw_results/out{}.pickle".format(file_number), "rb") as result_file:
            results = load(result_file)
            plt.plot([result.generation for result in results], [result.max_fitness for result in results], )
    except FileNotFoundError:
        continue

plt.show()

plt.figure()
plt.title('Algorithmic identity')
plt.xlabel('Generation')
plt.ylabel('Avg fitness')
axes = plt.gca()
axes.set_ylim([0, .05])

for file_number in range(len(os.listdir("raw_results"))):
    try:
        with open("raw_results/out{}.pickle".format(file_number), "rb") as result_file:
            results = load(result_file)
            plt.plot([result.generation for result in results], [result.avg_fitness for result in results], )
    except FileNotFoundError:
        continue
plt.show()
