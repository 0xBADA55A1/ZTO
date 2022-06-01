#!/usr/bin/python

from RandomNumberGenerator import RandomNumberGenerator
from random import randrange
import copy
import math


Z = 1
generator = RandomNumberGenerator(Z)


class FlowShopSolution:
	def generate_random_solution(self):
		for n in range(self.n):
			pos_b = generator.nextInt(0, self.n - 1)
			while n == pos_b:
				pos_b = generator.nextInt(0, self.n - 1)
			self.swap(n, pos_b)
	
	def __init__(self, tasks_n, machines_m, execution_time):
		self.n = tasks_n
		self.m = machines_m
		self.p = execution_time
		self.queue = [n for n in range(self.n)]
		self.generate_random_solution()
	
	def objective(self):
		C = [[0 for x in range(self.m)] for y in range(self.n)]

		j = 0
		i = 0
		#[j][i]
		C[j][i] = self.p[self.queue[j]][i]
		
		i = 0
		for j in range(1,self.n):
			C[j][i] = C[j-1][i] + self.p[self.queue[j]][i]
		
		j = 0
		for i in range(1, self.m):
			C[j][i] = C[j][i-1] + self.p[self.queue[j]][i]

		for j in range(1,self.n):
			for i in range(1, self.m):
				c_tmp = max(C[j-1][i], C[j][i-1])
				C[j][i] = c_tmp + self.p[self.queue[j]][i]

		# print(C[self.n - 1][self.m - 1])
		return C[self.n - 1][self.m - 1]

	def swap(self, pos_a, pos_b):
		self.queue[pos_a], self.queue[pos_b] = self.queue[pos_b], self.queue[pos_a]
		# print(self.queue)

class FlowShop:
	def generate_data(self, tasks_n, machines_m):
		execution_time = []
		for n in range(tasks_n):
			execution_time.append([generator.nextInt(1, 99) for m in range(machines_m)])
		return execution_time

	def __init__(self, tasks_n, machines_m):
		self.n = tasks_n
		self.m = machines_m
		self.execution_t = self.generate_data(self.n, self.m)
		self.x = FlowShopSolution(self.n, self.m, self.execution_t)

	def pick_best_random_solution(self, solutions_n):
		for _ in range(solutions_n):
			x_tmp = FlowShopSolution(self.n, self.m, self.execution_t)
			if x_tmp.objective() < self.x.objective():
				self.x = x_tmp

	def get_distraction(self, for_n_solutions):
		f_min = self.n * self.m
		f_max = 0

		for _ in range(for_n_solutions):
			x_tmp = FlowShopSolution(self.n, self.m, self.execution_t)
			if x_tmp.objective() < f_min: f_min = x_tmp.objective()
			if x_tmp.objective() > f_max: f_max = x_tmp.objective()

		# print(f_min, f_max)
		return f_max - f_min

	
	def gen_rand_solution(self):
		x_tmp = copy.deepcopy(self.x)

		pos_a = generator.nextInt(0, self.n - 1)
		pos_b = generator.nextInt(0, self.n - 1)
		while pos_a == pos_b:
			pos_b = generator.nextInt(0, self.n - 1)

		x_tmp.swap(pos_a, pos_b)

		return x_tmp


	def random_search(self, iterations_n):
		print('iteration: 0, f(x) =', self.x.objective())
		for _ in range(iterations_n):
			x_tmp = self.gen_rand_solution()

			if x_tmp.objective() < self.x.objective():
				self.x = x_tmp
				print('iteration: ', _ +1 , ', f(x) =', self.x.objective())


	def calc_prob(self, f_x, f_x_tmp, t):
		return pow(
			math.e,
			-(f_x_tmp - f_x) / t
		)


	def random_search_sa(self, t, t_a, t_min, visual = False):
		x_best = self.x

		iterations = 0
		while t >= t_min:
			x_tmp = self.gen_rand_solution()
			
			if x_tmp.objective() < self.x.objective():
				self.x = x_tmp
			else:
				if visual: print("f(x') > f(x), p: ", self.calc_prob(self.x.objective(), x_tmp.objective(), t) )
				if generator.nextFloat(0, 1) < self.calc_prob(self.x.objective(), x_tmp.objective(), t):
					if visual: print("x' -> x")
					self.x = x_tmp

			if self.x.objective() < x_best.objective():
				x_best = self.x
				# print("f(x_best) > f(x)")

			# print(t)
			t *= t_a
			iterations += 1
		self.x = x_best
		return iterations

