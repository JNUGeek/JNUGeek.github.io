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
z = [7, 8, 9]
print(zip(x, y, z))
for (i, j, k) in zip(x, y, z):
    print(i)

number = []
for num in range(10):
    number.append(num)
print(number)

list = [1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1]

print(list[3])

print(range(len(x)))

argss = {'1': {'introduction': None, 'qq': None, 'name': 'paul', 'school': 'ist', 'student_id': 2015000000, 'grade': None, 'department': '技术组', 'major': 'cst'},
         'b': {'f': 2},
         'c': {'g': 3},
         'd': {'h': 4}}
print(argss['1'])


#                data={'name': ['paul', 'ban'],
 #                     'student_id': [2015000000, 2015000002],
  #                    'grade': ['', ''],
   #                   'school': ['ist', 'aaa'],
    #                  'major': ['cst', 'bbb'],
     #                 'phone': ['15500000000', '15500000003'],
      #                'qq': ['', ''],
       #               'department': ['技术组', '媒宣组'],
        #              'introduction': ['', '']}