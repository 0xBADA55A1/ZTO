#! /bin/python3

import csv, math, numpy

class RandomNumberGenerator:
    def __init__(self, seedVaule=None):
        self.__seed=seedVaule
    def nextInt(self, low, high):
        m = 2147483647
        a = 16807
        b = 127773
        c = 2836
        k = int(self.__seed / b)
        self.__seed = a * (self.__seed % b) - k * c;
        if self.__seed < 0:
            self.__seed = self.__seed + m
        value_0_1 = self.__seed
        value_0_1 =  value_0_1/m
        return low + int(math.floor(value_0_1 * (high - low + 1)))
    def nextFloat(self, low, high):
        low*=100000
        high*=100000
        val = self.nextInt(low,high)/100000.0
        return val



gen = RandomNumberGenerator(666)

n = 15
d_min = 1
d_max = 500
w_min = 1
w_max = 500

d = w = numpy.zeros(shape = (n,n), dtype=numpy.uint16)

for j in range(n):
    for i in range(n):
        if i != j:
            d[i, j] = gen.nextInt(d_min, d_max)
            w[i, j] = gen.nextInt(w_min, w_max)

with open('data.csv', mode='w') as data_out:
    out = csv.writer(data_out, escapechar=']', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    out.writerow(["W:"])
    out.writerows(w)
    out.writerow(["D:"])
    out.writerows(d)