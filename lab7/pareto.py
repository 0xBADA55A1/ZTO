#!/usr/bin/python
import flowshop
import copy
import matplotlib.pyplot as plt

##########################
# Testing
##########################

n = 50 # zadan
m = 3 # maszyn

problem = flowshop.FlowShop(n, m)

i = 1000
P = problem.sim_annealing(i)

F = copy.copy(P)
for a in P:
	if a in F:
		for b in F:
			if a != b:
				if b < a:
					F.remove(a)
					break

F.sort(key=lambda x: x.criterion_A(), reverse=True)

def gen_cryt_vectors(solutions):
	c_max = []
	t_max = []
	for s in solutions:
		c_max.append(s.criterion_A())
		t_max.append(s.criterion_B())
	return c_max, t_max

Pc_max, Pt_max = gen_cryt_vectors(P)
Fc_max, Ft_max = gen_cryt_vectors(F)


plt.grid(which='both')
plt.plot(Pc_max, Pt_max, 'b.')
plt.plot(Fc_max, Ft_max, 'r')
plt.plot(Fc_max, Ft_max, '.r')
plt.xlabel('C_max')
plt.ylabel('T_max')
plt.show()