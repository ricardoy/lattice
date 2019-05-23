import numpy as np
from argparse import ArgumentParser
from lattice import Lattice, export_latex


def contains(a, b):
    for xa, xb in zip(a, b):
        if xb > xa:
            return False
    return True


def main(output_file_name):
    lattice = Lattice()

    nodes = dict()
    for x in [0, 1]:
        for y in [0, 1]:
            key = (x, y)
            nodes[key] = lattice.add_node(str(key))

    for key1, node1 in nodes.items():
        for key2, node2 in nodes.items():
            if key1 == key2:
                continue

            sum1 = sum(key1)
            sum2 = sum(key2)
            if sum1 > sum2 and sum1 - sum2 == 1:
                if contains(key1, key2):
                    lattice.add_edge(node1, node2)

    lattice.supremum = nodes[(1, 1)]

    export_latex(lattice, output_file_name, height_coef=1.5, width_coef=2)


if __name__ == '__main__':
    parser = ArgumentParser('Lattice helper')
    parser.add_argument('-output', type=str, help='Output file name.', required=False)
    args = parser.parse_args()

    main(args.output)