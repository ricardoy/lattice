from argparse import ArgumentParser
from lattice import Lattice, export_latex


def main3(output_file_name):
    lattice = Lattice()

    root = lattice.add_node('(1, 1)')
    left = lattice.add_node('(1, 0)')
    right = lattice.add_node('(0, 1)')
    right2 = lattice.add_node('(0, 2)')
    bottom = lattice.add_node(('(0, 0)'))


    lattice.add_edge(root, left)
    lattice.add_edge(root, right)
    lattice.add_edge(left, bottom)
    # lattice.add_edge(right, bottom)

    lattice.add_edge(right, right2)
    lattice.add_edge(right2, bottom)

    lattice.supremum = root

    export_latex(lattice, output_file_name)


def main2(output_file_name):
    lattice = Lattice()

    a = lattice.add_node('a')
    b = lattice.add_node('b')
    c = lattice.add_node('c')
    d = lattice.add_node('d')
    e = lattice.add_node('e')
    f = lattice.add_node('f')
    g = lattice.add_node('g')

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

    export_latex(lattice, output_file_name)


if __name__ == '__main__':
    parser = ArgumentParser('Lattice helper')
    parser.add_argument('-output', type=str, help='Output file name.', required=False)
    args = parser.parse_args()

    main2(args.output)