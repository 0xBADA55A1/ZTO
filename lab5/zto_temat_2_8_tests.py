#!/usr/bin/python

import matplotlib.pyplot as plt
import time
import copy

import zto_temat_2_8 as zto


##########################
# Tests
##########################
n_list = [50, 100, 250, 500, 1000, 2500]
m_list = [10, 20,  30,  40,  50,   60]

i = 3

t_rs = []
f_rs = []
t_rs_sa = []
f_rs_sa = []

for test in range(len(n_list)):
	print('n:', n_list[test], 'm:', m_list[test])
	for _ in range(i):
		problem = zto.FlowShop(n_list[test], m_list[test])
		problem.pick_best_random_solution(1000)
		problem_c = copy.deepcopy(problem)

		distraction = problem_c.get_distraction(for_n_solutions = 1000)
		start_time = time.time()
		i_tmp = problem_c.random_search_sa(t=distraction, t_a=0.99, t_min=1)
		print('ts:',time.time() - start_time)
		print('fs:',problem_c.x.objective())

		start_time = time.time()
		problem.random_search(i_tmp)
		print('t:',time.time() - start_time)
		print('f:',problem.x.objective())
		print('   ')

	print(' --- ')

print(t_rs)
print(f_rs)
print(t_rs_sa)
print(f_rs_sa)