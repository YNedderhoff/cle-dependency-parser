from modules.cle import chu_liu_edmonds

class SparseTestArc:
    def __init__(self, head, dependent, score):
        self.head = head
        self.dependent = dependent
        self.score = score
        self.feat_vec = []

        self.is_cycle = False
        self.former_dependent = None

class SparseTestGraph:
    def __init__(self):
        self.heads = {}
        
    def add_arc(self, head, arc):
        if head in self.heads:
            self.heads[head].append(arc)
        else:
            self.heads[head] = [arc]

a = SparseTestGraph()
a.add_arc(0, SparseTestArc(0, 1, 9))
a.add_arc(0, SparseTestArc(0, 2, 10))
a.add_arc(0, SparseTestArc(0, 3, 9))
a.add_arc(1, SparseTestArc(1, 2, 20))
a.add_arc(1, SparseTestArc(1, 3, 3))
a.add_arc(2, SparseTestArc(2, 1, 30))
a.add_arc(2, SparseTestArc(2, 3, 30))
a.add_arc(3, SparseTestArc(3, 1, 11))
a.add_arc(3, SparseTestArc(3, 2, 0))

y = chu_liu_edmonds(a.heads)