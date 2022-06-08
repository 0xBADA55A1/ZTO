#!/usr/bin/python
import flowshop
import copy

##########################
# Testing
##########################

n = 50 # zadan
m = 3 # maszyn

problem = flowshop.FlowShop(n, m)
# problem_backup = copy.deepcopy(problem)
# problem_c = copy.deepcopy(problem)

# distraction = problem.get_distraction(for_n_solutions = 1000)
# print('distraction:', distraction)
i = 100
print('f(x_0)=', problem.x.objective(), "T_max=", problem.x.tardiness())
problem.random_search(i)
print('Random Search (', i, 'iterations) f(x)=', problem.x.objective(), "T_max=", problem.x.tardiness() )