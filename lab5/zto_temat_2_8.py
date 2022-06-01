#!/usr/bin/python

from RandomNumberGenerator import RandomNumberGenerator
from random import randrange

import matplotlib.pyplot as plt
import time


Z = 1
generator = RandomNumberGenerator(Z)

n = 100 # zadan
m = 10 # maszyn


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
		self.solution = []

	def calc_time(self, solution = None):
		if solution is None:
			solution = self.solution
		execution_time_on_machine = []
		for machine in range(self.m):
			duration = 0
			for task in range( len(solution[machine]) ):
				duration += self.execution_t[
					solution[machine][task] # task_n
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
		return machine_found != to_machine_m

	def generate_random_solution(self):
		self.solution = [[] for _ in range(self.m)] 
		for task in range(self.n):
			# ----------------------------------------------------<first solution>-----------------
			# self.solution[randrange(self.m)].append(task)
			self.solution[generator.nextInt(0, self.m - 1)].append(task)



problem = FlowShop(n, m)
problem.generate_random_solution()
print(problem.solution)
print(problem.calc_time())
print(problem.move(66, 7))
print(problem.calc_time())

# def basic():
