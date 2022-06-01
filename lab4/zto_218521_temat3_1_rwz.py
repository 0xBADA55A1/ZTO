from docplex.mp.model import Model


w =[]
c =[]
B = 0

m = Model(name='test')
n = 10
list(m.binary_var(name='x{0}'.format(i)) for i in range(0,n))

m.maximize(m.sum(x[i]*c[i] for i in range(n)))

m.add_constraint(m.sum(w[i] for i in range(n)) <= B)

