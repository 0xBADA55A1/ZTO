from RandomNumberGenerator import RandomNumberGenerator
import csv

Z = 1
n = 10

generator = RandomNumberGenerator(Z)

c = []
w = []
for i in range(n):
    c.append(generator.nextInt(1,30))
    w.append(generator.nextInt(1,30))

B = generator.nextInt(5*n, 10 * n)

with open('f.csv', mode='w') as f:
    wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wr.writerow(c)
    wr.writerow(w)
    wr.writerow([B])
