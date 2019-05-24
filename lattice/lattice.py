from __future__ import annotations
from collections import defaultdict
from collections import deque

c = 0
def _generate_id():
    global c
    c += 1
    return 'latticeobject{}'.format(c)


class SimpleNode(object):
    def __init__(self, value):
        self.value = value
        self.predecessors = list()
        self.successors = list()
        self.id = _generate_id()
        self._height = None

    def is_leaf(self):
        return len(self.successors) == 0

    def add_predecessor(self, n:SimpleNode):
        self.predecessors.append(n)

    def add_successor(self, n:SimpleNode):
        self.successors.append(n)

    @property
    def height(self):
        if self._height is not None:
            return self._height
        max_children_height = -1
        for c in self.successors:
            h = c.height
            if h > max_children_height:
                max_children_height = h
        self._height = max_children_height + 1
        return self._height

    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            raise AttributeError()
        if self._height is None:
            self._height = value
        if value > self._height:
            self._height = value


class LatticeIterator(object):
    def __init__(self, lattice):
        self.queue = deque()
        self.lattice = lattice

        if lattice.supremum is not None:
            self.queue.append(lattice.supremum)

    def __next__(self):
        if len(self.queue) > 0:
            e = self.queue.popleft()
            for successor in e.successors:
                self.queue.append(successor)
            return e
        raise StopIteration


class Lattice(object):
    def __init__(self):
        self._supremum = None
        self._infimum = None
        self.nodes = list()

    @property
    def supremum(self):
        return self._supremum

    @supremum.setter
    def supremum(self, value):
        if isinstance(value, SimpleNode):
            self._supremum = value
        else:
            raise AttributeError()

    @property
    def infimum(self):
        return self._infimum

    @infimum.setter
    def infimum(self, value):
        if isinstance(value, SimpleNode):
            self._infimum = value
        else:
            raise AttributeError()

    def add_node(self, node):
        if not isinstance(node, SimpleNode):
            node = SimpleNode(node)
        for x in self.nodes:
            if node.value == x.value:
                return x
        self.nodes.append(node)
        return node

    def add_edge(self, origin:SimpleNode, destination:SimpleNode):
        origin.add_successor(destination)
        destination.add_predecessor(origin)

    def height(self):
        if self._supremum is None:
            return -1
        return self.supremum.height

    def width(self):
        count = defaultdict(int)
        for n in self.nodes:
            count[n.height] += 1
        return max(count.values())

    def __iter__(self):
        return LatticeIterator(self)

