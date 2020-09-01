


items = [1,2,3,4,5,6,7,8]


item = next(filter(lambda x:x > 10, items), None)

print(item)