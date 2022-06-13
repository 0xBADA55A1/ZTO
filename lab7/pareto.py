#!/usr/bin/python
import flowshop
import copy
import matplotlib.pyplot as plt

##########################
# Pareto Testing
##########################

n = 50 # zadan
m = 3 # maszyn

problem = flowshop.FlowShop(n, m)

i = 60
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

z1_k = 1.005
z2_k = 1.05
z1 = F[0].criterion_A() * z1_k
z2 = F[-1].criterion_B() * z2_k


hvi_c1 = [z1]
hvi_c2 = [z2]
hvi_c1.append(z1)
hvi_c2.append(F[0].criterion_B())

for i in range(len(F)):
	hvi_c1.append(F[i].criterion_A())
	hvi_c2.append(F[i].criterion_B())

	if i != len(F) - 1:
		hvi_c1.append(F[i].criterion_A())
		hvi_c2.append(F[i+1].criterion_B())

hvi_c1.append(F[-1].criterion_A())
hvi_c2.append(z2)
hvi_c1.append(z1)
hvi_c2.append(z2)

plt.grid(which='both')
plt.plot(Pc_max, Pt_max, 'b.')
plt.plot(Fc_max, Ft_max, 'r')
plt.plot(Fc_max, Ft_max, '.r')
plt.fill(hvi_c1, hvi_c2, '#AAFFAA')
plt.plot([z1], [z2], 'og')
plt.annotate("Z", (z1, z2))
plt.xlabel('C_max')
plt.ylabel('T_max')
plt.show()