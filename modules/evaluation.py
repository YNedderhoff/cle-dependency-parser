import codecs

from token import sentences
from graphs import FullGraph
from perceptron import make_graph_compareable

def evaluate(args):
    full_graphs_gold = {}

    total = 0
    correct = 0

    for sentence in sentences(codecs.open(args.gold, encoding='utf-8')):
        full_graph_gold = FullGraph(sentence).heads
        full_graphs_gold[len(full_graphs_gold)] = full_graph_gold
    full_graphs_predicted ={}
    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):
        full_graph_predicted = FullGraph(sentence).heads
        full_graphs_predicted[len(full_graphs_predicted)] = full_graph_predicted

    if len(full_graphs_gold) == len(full_graphs_predicted):
        for gold_graph in sorted(full_graphs_gold.keys()):
            total += 1
            if make_graph_compareable(full_graphs_gold[gold_graph]) == make_graph_compareable(full_graphs_predicted[gold_graph]):
                correct += 1
    else:
        print "Error in file length, Gold: " + str(len(full_graphs_gold)) + ", Predicted: " +str(len(full_graphs_predicted))

    out = open(args.out_file, "w")
    print >> out, "Total: " + str(total)
    print >>out, "Correct: " + str(correct)
    out.close()
