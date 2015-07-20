from modules.cle import chu_liu_edmonds
from modules.graphs import SparseOwnGraph, SparseOwnArc


a = SparseOwnGraph()
a.add_arc(0, SparseOwnArc(0, 1, 9))
a.add_arc(0, SparseOwnArc(0, 2, 10))
a.add_arc(0, SparseOwnArc(0, 3, 9))
a.add_arc(1, SparseOwnArc(1, 2, 20))
a.add_arc(1, SparseOwnArc(1, 3, 3))
a.add_arc(2, SparseOwnArc(2, 1, 30))
a.add_arc(2, SparseOwnArc(2, 3, 30))
a.add_arc(3, SparseOwnArc(3, 1, 11))
a.add_arc(3, SparseOwnArc(3, 2, 0))

y = chu_liu_edmonds(a.heads)