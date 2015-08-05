import codecs

from token import sentences
from graphs import Graph, reverse_head_graph
from perceptron import make_graph_compareable


def evaluate(args):
    sparse_graphs_gold = {}
    sparse_graphs_predicted = {}

    total = 0.0
    correct = 0.0

    total_arcs = 0.0
    correct_arcs = 0.0

    for sentence in sentences(codecs.open(args.gold, encoding='utf-8')):
        sparse_graph_gold = Graph(sentence, "sparse").heads
        sparse_graphs_gold[len(sparse_graphs_gold)] = sparse_graph_gold
    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):
        sparse_graph_predicted = Graph(sentence, "sparse").heads
        sparse_graphs_predicted[len(sparse_graphs_predicted)] = sparse_graph_predicted

    if len(sparse_graphs_gold) == len(sparse_graphs_predicted):
        for gold_graph in sorted(sparse_graphs_gold.keys()):
            total += 1
            if make_graph_compareable(sparse_graphs_gold[gold_graph]) == make_graph_compareable(
                    sparse_graphs_predicted[gold_graph]):
                correct += 1

    else:
        print "Error in file length, Gold: " + str(len(sparse_graphs_gold)) + ", Predicted: " + str(
            len(sparse_graphs_predicted))

    for predicted_graph in sorted(sparse_graphs_predicted.keys()):
        rev_predicted = reverse_head_graph(sparse_graphs_predicted[predicted_graph])
        rev_gold = reverse_head_graph(sparse_graphs_gold[predicted_graph])
        for dependent in rev_predicted:
            for arc in rev_predicted[dependent]:
                if arc.head == rev_gold[dependent][0].head:
                    correct_arcs += 1
                total_arcs += 1

    with open(args.out_file, "w") as out:
        print >> out, "Total: " + str(total)
        print >> out, "Correct: " + str(correct)
        print >> out, "%: " + str(round(correct/total, 2) * 100)
        print >> out, ""
        print >> out, "Total Arcs: " + str(total_arcs)
        print >> out, "Correct: " + str(correct_arcs)
        print >> out, "%: " + str(round(correct_arcs/total_arcs, 2) * 100)
