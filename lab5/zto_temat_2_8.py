#!/usr/bin/python

from RandomNumberGenerator import RandomNumberGenerator
from random import randrange
import copy

import matplotlib.pyplot as plt
import time


Z = 1
generator = RandomNumberGenerator(Z)

n = 10000 # zadan
m = 100 # maszyn

class FlowShopSolution:
	def generate_random_solution(self):
		self.solution = [[] for _ in range(self.m)] 
		for task in range(self.n):
			# ----------------------------------------------------<first solution>-----------------
			# self.solution[randrange(self.m)].append(task)
			self.solution[generator.nextInt(0, self.m - 1)].append(task)
	
	def __init__(self, tasks_n, machines_m):
		self.n = tasks_n
		self.m = machines_m
		self.generate_random_solution()
	
	def calc_time(self, execution_time):
		execution_time_on_machine = []
		for machine in range(self.m):
			duration = 0
			for task in range( len(self.solution[machine]) ):
				duration += execution_time[
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
		self.s = FlowShopSolution(self.n, self.m)

	def pick_best_random_solution(self, solutions_n):
		for _ in range(solutions_n):
			tmp = FlowShopSolution(self.n, self.m)
			if tmp.calc_time(self.execution_t) < self.s.calc_time(self.execution_t):
				self.s = tmp
	
	def random_search(self, iterations_n):
		for _ in range(iterations_n):
			tmp = copy.deepcopy(self.s)
			moved = tmp.move(
				generator.nextInt(0, self.n - 1),
				generator.nextInt(0, self.m - 1)	
			)
			
			# while moved:
			# 	moved = tmp.move(
			# 		generator.nextInt(0, self.n - 1),
			# 		generator.nextInt(0, self.m - 1)	
			# 	)

			if tmp.calc_time(self.execution_t) < self.s.calc_time(self.execution_t):
				self.s = tmp








problem = FlowShop(n, m)
problem.pick_best_random_solution(20)

print(problem.s.calc_time(problem.execution_t))
problem.random_search(2000)
print(problem.s.calc_time(problem.execution_t))

# def basic():
