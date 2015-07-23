from modules.cle import chu_liu_edmonds
from modules.graphs import ManualSparseGraph, SparseArc, cycle, highest_scoring_heads

from copy import deepcopy


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
c.add_arc(0, SparseArc(0, 1, 10.0))
c.add_arc(0, SparseArc(0, 2, 5.0))
c.add_arc(0, SparseArc(0, 3, 15.0))
c.add_arc(1, SparseArc(1, 2, 20.0))
c.add_arc(1, SparseArc(1, 3, 15.0))
c.add_arc(2, SparseArc(2, 1, 25.0))
c.add_arc(2, SparseArc(2, 3, 25.0))
c.add_arc(3, SparseArc(3, 1, 30.0))
c.add_arc(3, SparseArc(3, 2, 10.0))


for head in y:
    for arc in y[head]:
        print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
print "--"

graph_dict_b = {}
for head in b.heads:
    graph_dict_b[head] = []
    for arc in b.heads[head]:
        graph_dict_b[head].append(arc.dependent)
print graph_dict_b

graph_dict_c = {}
for head in c.heads:
    graph_dict_c[head] = []
    for arc in c.heads[head]:
        graph_dict_c[head].append(arc.dependent)
print graph_dict_c

if graph_dict_b == graph_dict_c:
    print "yes3"

d = ManualSparseGraph()
d.add_arc(0, SparseArc(0, 1, 5.0))
d.add_arc(0, SparseArc(0, 2, 1.0))
d.add_arc(0, SparseArc(0, 3, 1.0))
d.add_arc(1, SparseArc(1, 2, 11.0))
d.add_arc(1, SparseArc(1, 3, 4.0))
d.add_arc(2, SparseArc(2, 1, 10.0))
d.add_arc(2, SparseArc(2, 3, 5.0))
d.add_arc(3, SparseArc(3, 1, 9.0))
d.add_arc(3, SparseArc(3, 2, 8.0))

y = chu_liu_edmonds(d.heads)
print "finished"
for head in y:
    for arc in y[head]:
        print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
print "--"

e = ManualSparseGraph()
e.add_arc(0, SparseArc(0, 3, 1.0))
e.add_arc(1, SparseArc(1, 2, 11.0))
e.add_arc(2, SparseArc(2, 3, 5.0))
e.add_arc(3, SparseArc(3, 1, 9.0))

f = highest_scoring_heads(deepcopy(e.heads))

for head in f:
    for arc in f[head]:
        print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
print "--"


print cycle(f, [], sorted(f.keys())[0])
