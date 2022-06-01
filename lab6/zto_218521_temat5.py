import random
from itertools import accumulate
import matplotlib.pyplot as plt
import time

from array import array

from RandomNumberGenerator import RandomNumberGenerator

random.seed(100)
Z = 1
generator = RandomNumberGenerator(Z)

n = 10


def generate_d(n):
    d = []
    for _ in range(n):
        d.append([generator.nextInt(1, 30) for _ in range(n)])
    return d


# p1 =     [1,3,|4,5]
# p2 =     [4,3,|1,5]

# child1 = [1,3,1,5]
# child2 = [4,3,4,5]

# child1 = [1,3,| 1,5]
# child2 = [4,3,| 4,5]
def _crossover_pmx_r(main_genom_cuted,
                     secondary_genom_cuted, before_secondary_genom_cuted, after_secondary_genom_cuted,
                     before_secondary_genom_cuted_set, after_secondary_genom_cuted_set,
                     bad_gene_index, orginal_value_to_replace):
    main_gene = main_genom_cuted[bad_gene_index]
    secondary_gene = main_genom_cuted[bad_gene_index]
    # if main_gene not in secondary_genom_cuted:  # not necessary
    if main_gene in before_secondary_genom_cuted_set:
        before_secondary_genom_cuted[before_secondary_genom_cuted.index(main_gene)] = orginal_value_to_replace
    elif main_gene in after_secondary_genom_cuted_set:
        after_secondary_genom_cuted[after_secondary_genom_cuted.index(main_gene)] = orginal_value_to_replace
    else:
        secondary_genom_cuted_index = secondary_genom_cuted.index(main_gene)
        _crossover_pmx_r(main_genom_cuted,
                         secondary_genom_cuted, before_secondary_genom_cuted, after_secondary_genom_cuted,
                         before_secondary_genom_cuted_set, after_secondary_genom_cuted_set,
                         secondary_genom_cuted_index, orginal_value_to_replace)


def crossover_pmx_get_child(main_genom_cuted, main_genom_cuted_set,
                            secondary_genom_cuted, before_secondary_genom_cuted, after_secondary_genom_cuted):
    after_secondary_genom_cuted_set = set(after_secondary_genom_cuted)
    before_secondary_genom_cuted_set = set(before_secondary_genom_cuted)
    bad_copy_genes_i = []
    for secondary_gene_index, secondary_gene in enumerate(secondary_genom_cuted):
        if secondary_gene not in main_genom_cuted_set:
            # if a_gene in before_secondary_genom_cuted or a_gene in after_secondary_genom_cuted:
            bad_copy_genes_i.append(secondary_gene_index)

    for bad_gene_index in bad_copy_genes_i:
        bad_gene_second_genom_value = secondary_genom_cuted[bad_gene_index]
        _crossover_pmx_r(
            main_genom_cuted,
            secondary_genom_cuted, before_secondary_genom_cuted, after_secondary_genom_cuted,
            before_secondary_genom_cuted_set, after_secondary_genom_cuted_set,
            bad_gene_index, bad_gene_second_genom_value
        )
    return [*before_secondary_genom_cuted, *main_genom_cuted, *after_secondary_genom_cuted]


def crossover_pmx(genom_a, genom_b, crossover_start=0, crossover_end=0):
    genom_a_cuted = genom_a[crossover_start: crossover_end]
    genom_b_cuted = genom_b[crossover_start: crossover_end]

    before_genom_a_cuted = genom_a[:crossover_start]
    before_genom_b_cuted = genom_b[:crossover_start]

    after_genom_a_cuted = genom_a[crossover_end:]
    after_genom_b_cuted = genom_b[crossover_end:]
    genom_a_cuted_set = set(genom_a_cuted)
    genom_b_cuted_set = set(genom_b_cuted)
    child1 = crossover_pmx_get_child(genom_a_cuted, genom_a_cuted_set,
                                     genom_b_cuted, [*before_genom_b_cuted],
                                     [*after_genom_b_cuted])
    child2 = crossover_pmx_get_child(genom_b_cuted, genom_b_cuted_set,
                                     genom_a_cuted, [*before_genom_a_cuted],
                                     [*after_genom_a_cuted])

    # if len(child1) != len(set(child1)):
    #     print("dupa3")
    # if len(child2) != len(set(child2)):
    #     print("dupa4")
    # if len(child1) != 10:
    #     print("dupa")
    # if len(child2) != 10:
    #     print("dupa2")
    return [child1, child2]


def extend_child_crossover_ox(child, v, cuted_part, cuted_part_set, crossover_start):
    if 0 == crossover_start and len(child) == 0:
        child.extend(cuted_part)

    if v not in cuted_part_set:
        child.append(v)

    if len(child) == crossover_start:
        child.extend(cuted_part)


def crossover_ox(genom_a, genom_b, crossover_start=0, crossover_end=0):
    child1 = []
    child2 = []
    genom_a_cuted = genom_a[crossover_start: crossover_end]
    genom_b_cuted = genom_b[crossover_start: crossover_end]

    genom_a_cuted_set = set(genom_a_cuted)
    genom_b_cuted_set = set(genom_b_cuted)

    for a_v, b_v in zip(genom_a, genom_b):
        extend_child_crossover_ox(child1, b_v, genom_a_cuted, genom_a_cuted_set, crossover_start)
        extend_child_crossover_ox(child2, a_v, genom_b_cuted, genom_b_cuted_set, crossover_start)

    #    if len(child1) != len(set(child1)):
    #        print("dupa3")
    #    if len(child2) != len(set(child2)):
    #        print("dupa4")
    #    if len(child1) != 10:
    #        print("dupa")
    #    if len(child2) != 10:
    #        print("dupa2")
    return [child1, child2]


def random_point_crossover_decorator(function):
    def inner(*args, **kwargs):
        cros_n_1 = random.randint(0, len(args[0]))
        cros_n_2 = random.randint(0, len(args[0]))
        return function(*args, **kwargs, crossover_start=min(cros_n_1, cros_n_2), crossover_end=max(cros_n_1, cros_n_2))

    return inner


@random_point_crossover_decorator
def random_point_crossover_ox(genom_a, genom_b, crossover_start=0, crossover_end=0):
    return crossover_ox(
        genom_a,
        genom_b,
        crossover_start, crossover_end)


@random_point_crossover_decorator
def random_point_crossover_pmx(genom_a, genom_b, crossover_start=0, crossover_end=0):
    return crossover_pmx(
        genom_a,
        genom_b,
        crossover_start, crossover_end)


def multiple_genes_mutator(prob=0.1):
    def _multiple_genes_mutator(genom):
        elements_to_mutate = [random.random() < prob for _ in genom]
        genes_to_shuffle = [gene for gene, should_mutate in zip(genom, elements_to_mutate) if should_mutate]
        random.shuffle(genes_to_shuffle)  # I'm not sure if set() will shuffle array on alone
        genes_set = set(genes_to_shuffle)
        for i in range(len(genom)):
            if genom[i] in genes_set:
                genom[i] = genes_to_shuffle.pop()
        #        if len(genom) != len(set(genom)):
        #            print("wtf")
        return genom

    return _multiple_genes_mutator


def calc_cost(d, genom):  # reverse calc fitness
    cost = 0
    for i in range(len(genom)):
        cost += d[genom[i]][genom[(i + 1) % len(genom)]]
    return cost


def roulette_parent_selection(population_fitness_scores, children_size):
    population_fitness_scores_acc = list(accumulate(population_fitness_scores))
    parents_numbers = []
    for _ in range(children_size // 2):
        parents_numbers.append([random.uniform(
            0, population_fitness_scores_acc[-1]
        ), random.uniform(0, population_fitness_scores_acc[-1])])

    parents_indexes = [[0, 0] for _ in parents_numbers]

    for i in range(len(population_fitness_scores_acc)):
        if i == 0:
            for j in range(len(parents_numbers)):
                for k in range(len(parents_numbers[j])):
                    if parents_numbers[j][k] <= population_fitness_scores_acc[i]:
                        parents_indexes[j][k] = i
        else:
            for j in range(len(parents_numbers)):
                for k in range(len(parents_numbers[j])):
                    if population_fitness_scores_acc[i - 1] < parents_numbers[j][k] <= \
                            population_fitness_scores_acc[i]:
                        parents_indexes[j][k] = i

    return parents_indexes

def tournament_parent_selection(tournament_size=3):
    def _tournament_parent_selection(population_fitness_scores, children_size):
        parent_indexes = []
        for i in range(children_size // 2):
            torunament_indexes_a = random.sample(range(len(population_fitness_scores)), tournament_size)
            max_element_index_a = max(torunament_indexes_a,
                                      key=lambda el_index: population_fitness_scores[el_index])
            torunament_indexes_b = random.sample(range(len(population_fitness_scores)), tournament_size)
            max_element_index_b = max(torunament_indexes_b,
                                      key=lambda el_index: population_fitness_scores[el_index])
            parent_indexes.append((max_element_index_a, max_element_index_b))

        return parent_indexes

    return _tournament_parent_selection


def ordered_initializer(gene):
    gene.sort()
    return gene


# need to have scores over 1
def run_ga(d, n, calc_fitness_fn=calc_cost, crossover_parent_selection=tournament_parent_selection(),
           mutation_fn=multiple_genes_mutator(), crossover_fn=random_point_crossover_ox,
           pop_size=1000,
           sim_len=1000, mode='minimalise', initializer=random.shuffle):
    corrected_fitness_fn = None

    def reverse_fitness(*args, **kwargs):
        return 1 / (calc_fitness_fn(*args, **kwargs) + 0.0000000001)

    if mode == 'minimalise':
        corrected_fitness_fn = reverse_fitness
    else:
        corrected_fitness_fn = calc_fitness_fn

    population = [list(range(n)) for _ in range(pop_size)]
    [initializer(i) for i in population]
    for ep in range(sim_len):
        #        print("ep " + str(ep))
        population_fitnes_scores = [corrected_fitness_fn(d, i) for i in population]
        new_parents = crossover_parent_selection(population_fitnes_scores, len(population))
        new_parents = [(population[i[0]], population[i[1]]) for i in new_parents]
        new_childrens = [crossover_fn(*parents) for parents in new_parents]
        new_childrens = [j for i in new_childrens for j in i]
        population.extend(new_childrens)
        population = [mutation_fn(i) for i in population]
        population.sort(key=lambda genom: corrected_fitness_fn(d, genom), reverse=True)
        population = population[:pop_size]
    return population[0]


def run_optimalization(n, params, avg=10):
    result_cost_avg = 0
    start = time.process_time()
    result = None
    for i in range(avg):
        d = generate_d(n)
        result = run_ga(d, n, **params)
        result_cost_avg += calc_cost(d, result) / avg
    elapsed = time.process_time() - start / avg
    return result, result_cost_avg, elapsed


plots = [
        [{'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(), 'crossover_fn': random_point_crossover_ox,
          'pop_size': -1,
          'sim_len': 1000, 'mode': 'minimalise', 'initializer': random.shuffle},
         {'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(), 'crossover_fn': random_point_crossover_ox,
          'pop_size': 100,
          'sim_len': -1, 'mode': 'minimalise', 'initializer': random.shuffle}, 'standard'],

        [{'calc_fitness_fn': calc_cost, 'crossover_parent_selection': tournament_parent_selection(10),
          'mutation_fn': multiple_genes_mutator(), 'crossover_fn': random_point_crossover_ox,
          'pop_size': -1,
          'sim_len': 1000, 'mode': 'minimalise', 'initializer': random.shuffle},
         {'calc_fitness_fn': calc_cost, 'crossover_parent_selection': tournament_parent_selection(10),
          'mutation_fn': multiple_genes_mutator(), 'crossover_fn': random_point_crossover_ox,
          'pop_size': 100,
          'sim_len': -1, 'mode': 'minimalise', 'initializer': random.shuffle}, 'tournament_parent_selection(10)'],

        [{'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.01), 'crossover_fn': random_point_crossover_ox,
          'pop_size': -1,
          'sim_len': 1000, 'mode': 'minimalise', 'initializer': random.shuffle},
         {'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.01), 'crossover_fn': random_point_crossover_ox,
          'pop_size': 100,
          'sim_len': -1, 'mode': 'minimalise', 'initializer': random.shuffle}, 'multiple_genes_mutator(0.01)'],

        [{'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.05), 'crossover_fn': random_point_crossover_ox,
          'pop_size': -1,
          'sim_len': 1000, 'mode': 'minimalise', 'initializer': random.shuffle},
         {'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.05), 'crossover_fn': random_point_crossover_ox,
          'pop_size': 100,
          'sim_len': -1, 'mode': 'minimalise', 'initializer': random.shuffle}, 'multiple_genes_mutator(0.05)'],

        [{'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.2), 'crossover_fn': random_point_crossover_ox,
          'pop_size': -1,
          'sim_len': 1000, 'mode': 'minimalise', 'initializer': random.shuffle},
         {'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.2), 'crossover_fn': random_point_crossover_ox,
          'pop_size': 100,
          'sim_len': -1, 'mode': 'minimalise', 'initializer': random.shuffle}, 'multiple_genes_mutator(0.2)'],

        [{'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.4), 'crossover_fn': random_point_crossover_ox,
          'pop_size': -1,
          'sim_len': 1000, 'mode': 'minimalise', 'initializer': random.shuffle},
         {'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(0.4), 'crossover_fn': random_point_crossover_ox,
          'pop_size': 100,
          'sim_len': -1, 'mode': 'minimalise', 'initializer': random.shuffle}, 'multiple_genes_mutator(0.4)'],

        [{'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(), 'crossover_fn': random_point_crossover_pmx,
          'pop_size': -1,
          'sim_len': 1000, 'mode': 'minimalise', 'initializer': random.shuffle},
         {'calc_fitness_fn': calc_cost, 'crossover_parent_selection': roulette_parent_selection,
          'mutation_fn': multiple_genes_mutator(), 'crossover_fn': random_point_crossover_pmx,
          'pop_size': 100,
          'sim_len': -1, 'mode': 'minimalise', 'initializer': random.shuffle}, 'random_point_crossover_pmx']
]
#print(plots[0][0][0])

Ns = [12, 20]#, 40, 80, 160, 360]

# big
# population_sizes = [10, 20, 40, 50, 100, 200, 400, 800, 1000]
# sim_lens =         [10, 20, 40, 50, 100, 200, 400, 800, 1000, 2000, 4000, 5000, 10000, 20000, 40000, 80000, 100000]

# small
population_sizes = [10, 20, 40]#, 50, 100]
sim_lens = [10, 20, 40, 50, 100]#, 200, 400, 800, 1000]

figure, axis = plt.subplots(len(Ns), 2)

for i, _ in enumerate(Ns):
    for j, _ in enumerate(plots):
        print(f'plotting: {i} {j}')
        result_avg_a = []
        for pop in population_sizes:
            plots[j][0]["pop_size"] = pop
            _, result_avg, _ = run_optimalization(Ns[i], plots[j][0])
            result_avg_a.append(result_avg)

        axis[i, 0].plot(population_sizes,result_avg_a, label=plots[j][2])
        axis[i, 0].legend(loc="upper left")

        result_avg_a = []
        for sim_len in sim_lens:
            plots[j][1]["sim_len"] = sim_len
            _, result_avg, _ = run_optimalization(Ns[i], plots[j][1])
            result_avg_a.append(result_avg)

        axis[i, 1].plot(sim_lens,result_avg_a, label=plots[j][2])
        axis[i, 1].legend(loc="upper left")
plt.show()




