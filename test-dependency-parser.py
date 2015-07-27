from modules.cle import chu_liu_edmonds
from modules.graphs import ManualSparseGraph, SparseArc, cycle, highest_scoring_heads

from copy import deepcopy

"""
a = ManualSparseGraph()
a.add_arc(0, SparseArc(0, 1, 10.0))
a.add_arc(0, SparseArc(0, 2, 9.0))
a.add_arc(0, SparseArc(0, 3, 9.0))
a.add_arc(1, SparseArc(1, 2, 30.0))
a.add_arc(1, SparseArc(1, 3, 30.0))
a.add_arc(2, SparseArc(2, 1, 20.0))
a.add_arc(2, SparseArc(2, 3, 3.0))
a.add_arc(3, SparseArc(3, 1, 0.0))
a.add_arc(3, SparseArc(3, 2, 11.0))



y = chu_liu_edmonds(a.heads)

print "finished"

for head in y:
    for arc in y[head]:
        print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
print "--"


b = ManualSparseGraph()
b.add_arc(0, SparseArc(0, 1, 10.0))
b.add_arc(0, SparseArc(0, 2, 5.0))
b.add_arc(0, SparseArc(0, 3, 15.0))
b.add_arc(1, SparseArc(1, 2, 20.0))
b.add_arc(1, SparseArc(1, 3, 15.0))
b.add_arc(2, SparseArc(2, 1, 25.0))
b.add_arc(2, SparseArc(2, 3, 25.0))
b.add_arc(3, SparseArc(3, 1, 30.0))
b.add_arc(3, SparseArc(3, 2, 10.0))

y = chu_liu_edmonds(b.heads)

print "finished"

for head in y:
    for arc in y[head]:
        print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
print "--"

c = ManualSparseGraph()
c.add_arc(33, SparseArc(33, 32, 0))
c.add_arc(4, SparseArc(4, 3, 0))
c.add_arc(4, SparseArc(4, 5, 0))
c.add_arc(4, SparseArc(4, 8, 0))
c.add_arc(4, SparseArc(4, 20, 0))
c.add_arc(4, SparseArc(4, 23, 0))
c.add_arc(4, SparseArc(4, 25, 0))
c.add_arc(4, SparseArc(4, 27, 0))
c.add_arc(4, SparseArc(4, 34, 0))
c.add_arc(4, SparseArc(4, 35, 0))
c.add_arc(5, SparseArc(5, 7, 0))
c.add_arc(7, SparseArc(7, 6, 0))
c.add_arc(9, SparseArc(9, 10, 0))
c.add_arc(11, SparseArc(11, 12, 0))
c.add_arc(13, SparseArc(13, 1, 0))
c.add_arc(13, SparseArc(13, 4, 0))
c.add_arc(13, SparseArc(13, 15, 0))
c.add_arc(15, SparseArc(15, 14, 0))
c.add_arc(19, SparseArc(19, 2, 0))
c.add_arc(19, SparseArc(19, 9, 0))
c.add_arc(19, SparseArc(19, 11, 0))
c.add_arc(19, SparseArc(19, 13, 0))
c.add_arc(19, SparseArc(19, 16, 0))
c.add_arc(19, SparseArc(19, 17, 0))
c.add_arc(19, SparseArc(19, 18, 0))
c.add_arc(19, SparseArc(19, 22, 0))
c.add_arc(19, SparseArc(19, 26, 0))
c.add_arc(19, SparseArc(19, 31, 0))
c.add_arc(19, SparseArc(19, 33, 0))
c.add_arc(20, SparseArc(20, 19, 0))
c.add_arc(20, SparseArc(20, 21, 0))
c.add_arc(23, SparseArc(23, 24, 0))
c.add_arc(24, SparseArc(24, 28, 0))
c.add_arc(28, SparseArc(28, 29, 0))
c.add_arc(29, SparseArc(29, 30, 0))

print cycle(c.heads)
"""
d = ManualSparseGraph()
# d.add_arc(0, SparseArc(0, 7, 0))
d.add_arc(16, SparseArc(16, 1, 0))
d.add_arc(16, SparseArc(16, 2, 0))
d.add_arc(16, SparseArc(16, 3, 0))
d.add_arc(16, SparseArc(16, 4, 0))
d.add_arc(16, SparseArc(16, 5, 0))
d.add_arc(16, SparseArc(16, 6, 0))
d.add_arc(16, SparseArc(16, 7, 0))
d.add_arc(16, SparseArc(16, 8, 0))
d.add_arc(16, SparseArc(16, 9, 0))
d.add_arc(16, SparseArc(16, 10, 0))
d.add_arc(16, SparseArc(16, 11, 0))
d.add_arc(16, SparseArc(16, 12, 0))
d.add_arc(16, SparseArc(16, 13, 0))
d.add_arc(16, SparseArc(16, 14, 0))
d.add_arc(16, SparseArc(16, 15, 0))
d.add_arc(20, SparseArc(20, 16, 0))
d.add_arc(16, SparseArc(16, 17, 0))
d.add_arc(16, SparseArc(16, 18, 0))
d.add_arc(16, SparseArc(16, 19, 0))
d.add_arc(16, SparseArc(16, 20, 0))
d.add_arc(16, SparseArc(16, 21, 0))
d.add_arc(20, SparseArc(20, 16, 0))
d.add_arc(7, SparseArc(7, 22, 0))

print cycle(d.heads)