import itertools
for i in range(1, 4):
    result = itertools.combinations(flower_names, i)
    for item in result:
        print(item)
