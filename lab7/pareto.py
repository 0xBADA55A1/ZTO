#!/usr/bin/python
import flowshop
import copy
import matplotlib.pyplot as plt

##########################
# Pareto Testing
##########################


def gen_pareto(problem, i = 100, seed = None):

	P = problem.sim_annealing(i, seed)

	F = copy.copy(P)
	for a in P:
		if a in F:
			for b in F:
				if a != b:
					if b < a:
						F.remove(a)
						break

	F.sort(key=lambda x: x.criterion_A(), reverse=True)
	return P, F

def gen_cryt_vectors(solutions):
	c_max = []
	t_max = []
	for s in solutions:
		c_max.append(s.criterion_A())
		t_max.append(s.criterion_B())
	return c_max, t_max

def gen_Z(F):
	z1_k = 1.3
	z2_k = 1.3
	z1 = F[0].criterion_A() * z1_k
	z2 = F[-1].criterion_B() * z2_k

	return int(z1), int(z2)

def calc_HVI(F, z1, z2):
	HVI = 0
	for i in range(len(F) - 1):
		x = z1 - F[i].criterion_A()
		y = F[i+1].criterion_B() - F[i].criterion_B()
		HVI += x * y
		# print(i, x, y)

	x = z1 - F[-1].criterion_A()
	y = z2 - F[-1].criterion_B()
	HVI += x * y
	# print(x, y)

	return HVI

def plot_pareto(P, F, z1, z2, HVI, it):
	Pc_max, Pt_max = gen_cryt_vectors(P)
	Fc_max, Ft_max = gen_cryt_vectors(F)

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

	plt.figure()
	plt.grid(which='both')
	plt.plot([Fc_max[0]], [Ft_max[0]], 'xr')
	plt.plot(Pc_max, Pt_max, 'b.')
	plt.plot(Fc_max, Ft_max, 'r')
	plt.plot(Fc_max, Ft_max, '.r')
	plt.fill(hvi_c1, hvi_c2, '#AAFFAA')
	plt.plot([z1], [z2], 'og')
	plt.annotate("Z", (z1, z2))
	plt.xlabel('C_max')
	plt.ylabel('T_max')
	plt.title('it=' + str(it) + ', HVI=' + str(HVI))
	

# it = [80, 160, 320, 640, 1280]
it = [80, 150, 300, 650, 1400]

n = 50 # zadan
m = 3 # maszyn

problem = flowshop.FlowShop(n, m)

for idx, i in enumerate(it):
	problem_temp = copy.deepcopy(problem)
	p, f = gen_pareto(problem_temp, i, 1)
	if idx == 0: 
		z1, z2 = gen_Z(f)
	hvi = calc_HVI(f, z1, z2)
	plot_pareto(p, f, z1, z2, hvi, i)
'''
cycles = 10
for i in it:
	hvi_summ = 0
	problem = flowshop.FlowShop(n, m)
	for _ in range(cycles):
		
		problem_temp = copy.deepcopy(problem)
		p, f = gen_pareto(problem_temp, i)
		z1, z2 = gen_Z(f)
		hvi_summ += calc_HVI(f, z1, z2)
	print('it=', i, 'hvi=', hvi_summ / cycles)
'''
plt.show()


'''
$ ./pareto.py
it= 80 hvi= 2709.0
it= 150 hvi= 4382.7
it= 300 hvi= 3208.0
it= 650 hvi= 5559.8
it= 1300 hvi= 3666.5
'''