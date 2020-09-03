items = [1,2,3,4,5]

mapped_items = list(map(lambda x: x + 5, items))

transformed_items = [x +1 for x in items]

print(mapped_items)

print(transformed_items)