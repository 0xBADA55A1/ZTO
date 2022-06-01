#!/usr/bin/python

import matplotlib
import matplotlib.pyplot as plt
import time
import copy

import zto_temat_2_8 as zto


##########################
# Tests
##########################
n_list = [20, 40, 80, 160, 2048, 4096]
m_list = [2,  4,  8,  16,   45,   64]  # m = sqrt(n)

i = 1
llen = 4

t_rs = []
f_rs = []
t_rs_sa = []
f_rs_sa = []

for test in range(llen):
	print('n:', n_list[test], 'm:', m_list[test])
	t_rs_sa_acc = 0
	f_rs_sa_acc = 0
	t_rs_acc = 0
	f_rs_acc = 0

	for _ in range(i):
		print('i:', _)
		problem = zto.FlowShop(n_list[test], m_list[test])
		problem.pick_best_random_solution(1000)
		problem_c = copy.deepcopy(problem)

		distraction = problem_c.get_distraction(for_n_solutions = 1000)
		start_time = time.time()
		i_tmp = problem_c.random_search_sa(t=distraction, t_a=0.99, t_min=1)
		t_rs_sa_acc += time.time() - start_time
		f_rs_sa_acc += problem_c.x.objective()

		start_time = time.time()
		problem.random_search(i_tmp)
		t_rs_acc += time.time() - start_time
		f_rs_acc += problem.x.objective()

	t_rs_sa.append(t_rs_sa_acc / i)
	f_rs_sa.append(f_rs_sa_acc / i)
	t_rs.append(t_rs_acc / i)
	f_rs.append(f_rs_acc / i)

print(t_rs)
print(f_rs)
print(t_rs_sa)
print(f_rs_sa)

fig, ax1 = plt.subplots()

ax1.plot(n_list[0:llen], t_rs, 'b')
ax1.plot(n_list[0:llen], t_rs_sa, 'b--')
ax1.set_xlabel('n')
ax1.set_xscale("log")
ax1.set_ylabel('time [s]', color='tab:blue')
ax1.grid(True, 'both')

ax2 = ax1.twinx()
ax2.set_ylabel('f(x)', color='tab:red')
ax2.plot(n_list[0:llen], f_rs, 'r')
ax2.plot(n_list[0:llen], f_rs_sa, 'r--')
ax2.tick_params(axis='y', labelcolor='tab:red')

fig.tight_layout()
plt.show()
