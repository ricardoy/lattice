import numpy as np
from pprint import pprint
from argparse import ArgumentParser
from lattice import Lattice, export_latex_grid, get_pyramids


def contains(a, b):
    for xa, xb in zip(a, b):
        if xb > xa:
            return False
    return True


def to_tuple(v):
    return tuple(map(tuple, v))


def binaryze(v, threshold):
    if type(v) == list:
        v = np.array(v)
    mask = v > threshold
    return mask.astype(np.int8)


def binaryze_as_tuple(v, threshold):
    return to_tuple(binaryze(v, threshold))


def main_old():
    pyramids = get_pyramids()

    p = np.array(pyramids[0])

    lattice = Lattice()

    a = lattice.add_node(binaryze_as_tuple(p, 0))
    b = lattice.add_node(binaryze_as_tuple(p, 1))
    c = lattice.add_node(binaryze_as_tuple(p, 2))
    d = lattice.add_node(binaryze_as_tuple(p, 3))
    e = lattice.add_node(binaryze_as_tuple(p, 4))
    f = lattice.add_node(binaryze_as_tuple(p, 5))
    g = lattice.add_node(binaryze_as_tuple(p, 6))

    lattice.add_edge(a, b)
    lattice.add_edge(a, c)
    lattice.add_edge(a, d)

    lattice.add_edge(b, e)
    lattice.add_edge(b, f)

    lattice.add_edge(c, e)
    lattice.add_edge(c, f)

    lattice.add_edge(d, e)
    lattice.add_edge(d, f)

    lattice.add_edge(e, g)
    lattice.add_edge(f, g)

    lattice.supremum = a

    export_latex_grid(lattice, width_coef=2.5, height_coef=2.5)


def main():
    pyramids = get_pyramids()
    # pyramids = [pyramids[1]]
    lattice = Lattice()
    data = dict()

    # print(len(pyramids))

    key = binaryze_as_tuple(pyramids[0], 0)
    supremum = lattice.add_node(key)

    data[key] = supremum

    all_chains = []

    for pyramid in pyramids:
        chain = [supremum]
        all_chains.append(chain)
        for i in np.unique(pyramid)[:-1]:
            pyramid_level = binaryze_as_tuple(pyramid, i)
            if pyramid_level not in data:
                data[pyramid_level] = lattice.add_node(pyramid_level)
            chain.append(data[pyramid_level])

    for chain in all_chains:
        for parent, child in zip(chain[0:-1], chain[1:]):
            # print(type(parent), type(child))
            lattice.add_edge(parent, child)



    # for key1, node1 in data.items():
    #     for key2, node2 in data.items():
    #         sum1 = np.sum(np.array(key1)).sum()
    #         sum2 = np.sum(np.array(key2)).sum()
    #         if key1 == key2:
    #             continue
    #         # if sum1 > sum2 and sum1 - sum2 == 1:
    #         if contains(key1, key2):
    #             lattice.add_edge(node1, node2)

    lattice.supremum = supremum

    export_latex_grid(lattice, width_coef=2.5, height_coef=2.5)


if __name__ == '__main__':
    main()
