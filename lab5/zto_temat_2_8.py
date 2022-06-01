#!/usr/bin/python

from RandomNumberGenerator import RandomNumberGenerator
from random import randrange
import copy
import math

import matplotlib.pyplot as plt
import time


Z = 1
generator = RandomNumberGenerator(Z)

n = 1000 # zadan
m = 50 # maszyn

class FlowShopSolution:
	def generate_random_solution(self):
		self.solution = [[] for _ in range(self.m)] 
		for task in range(self.n):
			# ----------------------------------------------------<first solution>-----------------
			# self.solution[randrange(self.m)].append(task)
			self.solution[generator.nextInt(0, self.m - 1)].append(task)
	
	def __init__(self, tasks_n, machines_m, execution_time):
		self.n = tasks_n
		self.m = machines_m
		self.execution_time = execution_time
		self.generate_random_solution()
	
	def calc_time(self):
		duration = 0
		for machine in range(self.m):
			for task in range( len(self.solution[machine]) ):
				duration += self.execution_time[
					self.solution[machine][task] # task_n
				][machine]					   # machine_m (duration)
		return duration
	
	def calc_worst_queue_time(self):
		execution_time_on_machine = []
		for machine in range(self.m):
			duration = 0
			for task in range( len(self.solution[machine]) ):
				duration += self.execution_time[
					self.solution[machine][task] # task_n
				][machine]					   # machine_m (duration)
			execution_time_on_machine.append(duration)
		return max(execution_time_on_machine)

	def move(self, task_n, to_machine_m):
		machine_found = None

		for machine in range(self.m):
			try:
				machine_found = machine
				self.solution[machine].remove(task_n)
				self.solution[to_machine_m].append(task_n)
				break
			except ValueError:
				pass
		
		if machine_found is None:
			raise Exception('FlowShop.move: task_n=' + str(task_n) + ' not found')
		return machine_found == to_machine_m  # return True if moved to same solution

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
			if x_tmp.calc_time() < self.x.calc_time():
				self.x = x_tmp
	
	def gen_rand_solution(self):
		x_tmp = copy.deepcopy(self.x)
		moved = x_tmp.move(
			generator.nextInt(0, self.n - 1),
			generator.nextInt(0, self.m - 1)	
		)
		while moved: # move if random selected the same solution
			moved = x_tmp.move(
				generator.nextInt(0, self.n - 1),
				generator.nextInt(0, self.m - 1)	
			)
		return x_tmp


	def random_search(self, iterations_n):
		for _ in range(iterations_n):
			x_tmp = self.gen_rand_solution()

			if x_tmp.calc_time() < self.x.calc_time():
				self.x = x_tmp


	def calc_prob(self, f_x, f_x_tmp, t):
		return pow(
			math.e,
			-(f_x_tmp - f_x) / t
		)


	def random_search_sa(self, iterations_n, t, t_a, t_min):
		x_best = self.x

		while t >= t_min:
			x_tmp = self.gen_rand_solution()
			
			if x_tmp.calc_time() < self.x.calc_time():
					self.x = x_tmp
			else:
				print("f(x') > f(x), p: " + str(self.calc_prob(self.x.calc_time(), x_tmp.calc_time(), t)))
				if generator.nextFloat(0, 1) < self.calc_prob(self.x.calc_time(), x_tmp.calc_time(), t):
					print("x' -> x")
					self.x = x_tmp

			if self.x.calc_time() < x_best.calc_time():
				x_best = self.x
				# print("f(x_best) > f(x)")

			# print(t)
			t *= t_a








problem = FlowShop(n, m)
problem.pick_best_random_solution(20)

print(problem.x.calc_time())

# problem.random_search(200)

problem.random_search_sa(20, 2000, 0.98, 1)

print(problem.x.calc_time())

# def basic():
