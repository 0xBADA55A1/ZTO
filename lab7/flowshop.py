#!/usr/bin/python

from RandomNumberGenerator import RandomNumberGenerator
from random import randrange
import copy
import math

# Problem: Flowshop
# Kryteria: 1,3,4,5
# Wizualizacja: 1,4,5,7
# Zadania na 5.0: - :(

Z = 1
generator = RandomNumberGenerator(Z)


class FlowShopSolution:
	def generate_random_solution(self):
		for n in range(self.n):
			pos_b = generator.nextInt(0, self.n - 1)
			while n == pos_b:
				pos_b = generator.nextInt(0, self.n - 1)
			self.swap(n, pos_b)
		self.C = None
	
	def __init__(self, tasks_n, machines_m, execution_time, d):
		self.n = tasks_n
		self.m = machines_m
		self.p = execution_time
		self.d = d
		self.queue = [n for n in range(self.n)]
		self.generate_random_solution()
		self.C = None

	def swap(self, pos_a, pos_b):
		self.queue[pos_a], self.queue[pos_b] = self.queue[pos_b], self.queue[pos_a]
		self.C = None
		# print(self.queue)

	def calc_C(self):
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

		self.C = C


	def objective(self):
		if self.C is None:
			self.calc_C()
		# print(C[self.n - 1][self.m - 1])
		return self.C[self.n - 1][self.m - 1]
	
	# Kryterium 1 (C_max) To nie to samo co objective???????
	def makespan(self):
		return self.objective()
		# if self.C is None:
		# 	self.calc_C()
		# C_max = 0
		# for j in range(self.n):
		# 	C_t = self.C[j][self.m - 1]
		# 	if C_t > C_max:
		# 		C_max = C_t
		# return C_max

	# Kryterium 2 (ΣF)
	def total_flowtime(self):
		if self.C is None:
			self.calc_C()

		sumC = 0
		for j in range(self.n):
			sumC += self.C[j][self.m - 1]
		return sumC

	# Kryterium 3 (T_max)
	def tardiness(self):
		if self.C is None:
			self.calc_C()
		
		t_max = 0
		for j in range(self.n):
			t = self.C[j][self.m - 1] - self.d[j]
			if t > t_max:
				t_max = t
		return t_max
	
	# Criterion Selection

	def criterion_A(self):
		return self.total_flowtime()

	def criterion_B(self):
		return self.tardiness()

	# Misc
	def __ne__(self, other):
		for i in range( len(self.queue) ):
			if self.queue[i] != other.queue[i]:
				return True
		return False
	
	def __lt__(self, other):
		if self.criterion_A() <= other.criterion_A():
			if self.criterion_B() < other.criterion_B():
				return True
		elif self.criterion_B() <= other.criterion_B():
			if self.criterion_A() < other.criterion_A():
				return True
		return False

class FlowShop:
	def generate_data(self, tasks_n, machines_m):
		execution_time = []
		A = 0
		for n in range(tasks_n):
			m_p = []
			for m in range(machines_m):
				p = generator.nextInt(1, 99)
				m_p.append(p)
				A += p
			execution_time.append(m_p)
		
		B = int(A / 2)
		A = int(A / 6)
		d = [generator.nextInt(A, B) for _ in range(tasks_n)]
		
		return execution_time, d

	def __init__(self, tasks_n, machines_m):
		self.n = tasks_n
		self.m = machines_m
		self.execution_t, self.d = self.generate_data(self.n, self.m)
		self.x = FlowShopSolution(self.n, self.m, self.execution_t, self.d)

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

	
	def gen_rand_solution_neighbour(self):
		x_tmp = copy.deepcopy(self.x)

		pos_a = generator.nextInt(0, self.n - 1)
		pos_b = generator.nextInt(0, self.n - 1)
		while pos_a == pos_b:
			pos_b = generator.nextInt(0, self.n - 1)

		x_tmp.swap(pos_a, pos_b)

		return x_tmp


	def random_search(self, iterations_n):
		# print('iteration: 0, f(x) =', self.x.objective())
		for _ in range(iterations_n):
			x_tmp = self.gen_rand_solution_neighbour()

			if x_tmp.objective() < self.x.objective():
				self.x = x_tmp
				# print('iteration: ', _ +1 , ', f(x) =', self.x.objective())

	def calc_prob(self, f_x, f_x_tmp, t):
		return pow(
			math.e,
			-(f_x_tmp - f_x) / t
		)


	def random_search_sa(self, t, t_a, t_min, visual = False):
		x_best = self.x

		iterations = 0
		while t >= t_min:
			x_tmp = self.gen_rand_solution_neighbour()
			
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

	# Zadanie 1

	def sim_annealing(self, iterations_n):
		def prob(it_):
			# return pow(0.995, it_)
			return 0.7
		# print('iteration: 0, f(x) =', self.x.objective())
		P = [self.x]
		for it in range(iterations_n):
			x_tmp = self.gen_rand_solution_neighbour()

			# if x_tmp.objective() <= self.x.objective():
			if x_tmp < self.x:
				self.x = x_tmp
				P.append(self.x)
			elif generator.nextFloat(0, 1) < prob(it):
				self.x = x_tmp
				P.append(self.x)

		return P
