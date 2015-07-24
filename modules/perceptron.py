from scoring import score
from graphs import complete_graph, check_graph_sanity
from cle import chu_liu_edmonds

def sum_of_arc_feature_vectors(graph, l):
    # returns the added feature vectors of every arc
    sum_of_feat_vecs = []
    for i in range(l):
        sum_of_feat_vecs.append(0)
    for head in graph:
        for arc in graph[head]:
            for feature in arc.feat_vec:
                sum_of_feat_vecs[feature] += 1
    return sum_of_feat_vecs

def make_graph_compareable(graph):
    graph_dict = {}
    for head in sorted(graph.keys()):
        tmp_arcs = []
        for arc in graph[head]:
            tmp_arcs.append(arc.dependent)
        graph_dict[head] = sorted(tmp_arcs)
    return graph_dict

def structured_perceptron(graph, feat_map, rev_feat_map, weight_vector, correct, errors, mode, alpha=0.5):
    if mode == "train":
        y_gold = graph  # the correct tree
        g = complete_graph(graph, feat_map, rev_feat_map)  # the complete, directed graph
        g_scored = score(g, weight_vector) # the scored, complete, directed graph

        try:
            y_predicted = chu_liu_edmonds(g_scored)

            if not check_graph_sanity(y_gold, y_predicted):
                errors += 1
                y_predicted = {}

        except KeyError:
            errors += 1
            y_predicted = {}

        if make_graph_compareable(y_predicted) == make_graph_compareable(y_gold):

            correct +=1

            return weight_vector, correct, errors
        else:

            tmp1 = sum_of_arc_feature_vectors(y_gold, len(weight_vector))
            tmp2 = sum_of_arc_feature_vectors(y_predicted, len(weight_vector))

            tmp3 = []
            for i in range(len(weight_vector)):
                tmp3.append(tmp1[i] - tmp2[i])

            tmp4 = []
            for i in range(len(weight_vector)):
                tmp4.append(tmp3[i] * alpha)

            w_new = []
            for i in range(len(weight_vector)):
                w_new.append(weight_vector[i] + tmp4[i])

            if len(w_new) != len(weight_vector):
                print "The new weight vector has not the same length as the old one."

            weight_vector = w_new

            return weight_vector, correct, errors

        # adjust weights, return weight vector

    elif mode == "test":

        g_scored = score(graph, weight_vector) # the scored, complete, directed graph

        try:
            y_predicted = chu_liu_edmonds(g_scored)

            if not check_graph_sanity(graph, y_predicted):
                errors += 1
                y_predicted = {}

        except KeyError:
            errors += 1
            y_predicted = {}

        return y_predicted, errors
        # write prediction into file

    else:

        print "This should not happen."