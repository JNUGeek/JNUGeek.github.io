import os, uuid

a = os.path.dirname(__file__)
print(a)
b = os.path.dirname(a)
print(b)
print(str(uuid.uuid4()))
print('大一')

args = {'a': 1,
        'b': 2,
        'c': "",
        'd': 4}

for info in args.keys():
            if not args[info]:
                continue
            print(args[info])

x = [1, 2, 3]
y = [4, 5, 6]
print(zip(x, y))
for i in zip(x, y):
    print(i)

number = []
for num in range(10):
    number.append(num)
print(number)


