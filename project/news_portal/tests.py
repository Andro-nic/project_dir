list=[
      'ура',
      'привет',
     ]
test = 'ура супер привет'

words = []
for i in len(test.split()):
    if i in list:
        words += i
        print(words)