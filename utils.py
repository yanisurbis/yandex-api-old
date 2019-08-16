def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


rel1 = [1, 2, 4]
rel2 = [4, 5]

# which elements were added
print(diff(rel1, rel2))
print(diff(rel2, rel1))
