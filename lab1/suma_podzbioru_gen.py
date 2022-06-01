from RandomNumberGenerator import RandomNumberGenerator
import csv

Z = 1
n = 10

generator = RandomNumberGenerator(Z)

s = [generator.nextInt(-100, 100) for i in range(1,n)]
T =  generator.nextInt(-50*n, 50*n)

with open('suma_podzbioru_data.csv', mode='w') as f:
    wr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wr.writerow(s)
    wr.writerow([T])
