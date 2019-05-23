import sys
from collections import defaultdict
from contextlib import contextmanager
from lattice import SimpleNode


@contextmanager
def file_writer(file_name=None):
    if file_name is None:
        writer = sys.stdout
    else:
        writer = open(file_name, 'w')

    yield writer

    if file_name is not None:
        writer.close()


class LatexExporter(object):
    def __init__(self, lattice, width_coef=1., height_coef=1.):
        self.lattice = lattice
        self.width_coef = width_coef
        self.height_coef = height_coef

    def generate_node(self, node:SimpleNode, x, y):
        return '\\node ({}) at ({}, {}) {{{}}};\n'.format(
            node.id,
            x,
            y,
            node.latex_representation())

    def process_nodes(self):
        visited_nodes = set()
        total_nodes_by_level = defaultdict(int)
        for node in self.lattice:
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            level = node.height
            total_nodes_by_level[level] += 1

        s = ''
        current_total_by_level = defaultdict(int)
        visited_nodes.clear()
        for node in self.lattice:
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            level = node.height

            current_total_by_level[level] += 1

            if total_nodes_by_level[level] == 1:
                x = 0
            elif total_nodes_by_level[level] % 2 == 0:
                if current_total_by_level[level] / float(total_nodes_by_level[level]) > 0.5:
                    x = total_nodes_by_level[level] - current_total_by_level[level]
                else:
                    x = current_total_by_level[level] - total_nodes_by_level[level]
                x += 0.5
            else:
                median = total_nodes_by_level[level] // 2 + 1
                if current_total_by_level[level] == median:
                    x = 0
                else:
                    x = current_total_by_level[level] - median

            s += self.generate_node(node, x*self.width_coef, level*self.height_coef)

        return s

    def process_edges(self):
        s = ''
        for node in self.lattice:
            for child in node.successors:
                s += '\\draw ({}) -- ({});\n'.format(node.id, child.id)
        return s

    def export(self, generate_header_footer=True):
        if generate_header_footer:
            s = """
            \\documentclass{article}
            \\usepackage{tikz}
            \\begin{document}\n"""
        else:
            s = ''

        s += '\\begin{tikzpicture}\n'

        s = s + self.process_nodes()
        s = s + self.process_edges()

        s += '\\end{tikzpicture}'

        if generate_header_footer:
            s = s + '\\end{document}'

        return s


def export_latex(lattice, output_file_name=None, generate_document=True, width_coef=1, height_coef=1):
    le = LatexExporter(lattice,
                       width_coef=width_coef,
                       height_coef=height_coef)
    with file_writer(output_file_name) as writer:
        writer.write(le.export(generate_document))