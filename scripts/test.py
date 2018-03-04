from itertools import combinations

genotypes = ['A', 'B', 'C']
combs = combinations(genotypes, 2)
for item in combs:
	print(item[0])