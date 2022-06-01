#!/usr/bin/python

import zto_temat_2_8 as zto
import copy

##########################
# Testing
##########################

n = 1000 # zadan
m = 50 # maszyn

problem = zto.FlowShop(n, m)
problem_backup = copy.deepcopy(problem)

problem_c = copy.deepcopy(problem)


distraction = problem.get_distraction(for_n_solutions = 1000)
print('distraction:', distraction)

print('f(x_0):', problem.x.objective() )
i = problem.random_search_sa(
	t=distraction,
	t_a=0.99,
	t_min=0.1,
	# visual=True
	visual=False
)
print('Random Search SA f(x):', problem.x.objective() )
print("iterations done:", i)

problem_c.random_search(i)
print('Random Search (', i, 'iterations) f(x):', problem_c.x.objective() )


# Same problem with pre-picking best solution from 1000 random
print('\n\n# Same problem with pre-picking best solution from 1000 random:\n')
problem = copy.deepcopy(problem_backup)
problem.pick_best_random_solution(1000)

problem_c = copy.deepcopy(problem)


distraction = problem.get_distraction(for_n_solutions = 1000)
print('distraction:', distraction)


print('f(x_0):', problem.x.objective() )
i = problem.random_search_sa(
	t=distraction,
	t_a=0.99,
	t_min=0.1,
	# visual=True
	visual=False
)
print('Random Search SA f(x):', problem.x.objective() )
print("iterations done:", i)

problem_c.random_search(i)
print('Random Search (', i, 'iterations) f(x):', problem_c.x.objective() )
