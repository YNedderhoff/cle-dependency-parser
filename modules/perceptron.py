from graphs import check_graph_sanity, make_graph_compareable
from cle import chu_liu_edmonds
import time

def sum_of_arc_feature_vectors(graph):

    # adds up the feature vectors of every arc of the graph. Returns it in a sparse representation:
    # {<index in feat_map>: <sum>}

    sum_of_feat_vecs = {}
    for head in graph:
        for arc in graph[head]:
            for feature in arc.feat_vec:
                try:
                    sum_of_feat_vecs[feature] += 1
                except KeyError:
                    sum_of_feat_vecs[feature] = 1
    return sum_of_feat_vecs

def structured_perceptron(complete_graph, weight_vector, correct, errors, mode, sparse_graph, alpha=0.5):

    if mode == "train":

        # try to make a prediction. if a KeyError occurs or the result is not in reasonable format, an error is counted.

        try:

            y_predicted = chu_liu_edmonds(complete_graph)

            if not check_graph_sanity(y_predicted, complete_graph):
                errors += 1

        except KeyError:
            y_predicted = {}
            errors += 1

        # if the prediction matches the gold graph: return, else: adjust weight vector

        if make_graph_compareable(y_predicted) == make_graph_compareable(sparse_graph):

            correct += 1
            return weight_vector, correct, errors

        else:
            tmp1 = sum_of_arc_feature_vectors(sparse_graph)
            tmp2 = sum_of_arc_feature_vectors(y_predicted)

            for i in (i for i in tmp1 if i in tmp2):
                weight_vector[i] += alpha * (tmp1[i] - tmp2[i])
            for i in (i for i in tmp1 if i not in tmp2):
                weight_vector[i] += (alpha * tmp1[i])
            for i in (i for i in tmp2 if i not in tmp1):
                weight_vector[i] += (alpha * (0 - tmp2[i]))

            return weight_vector, correct, errors

    elif mode == "test":

        try:

            y_predicted = chu_liu_edmonds(complete_graph)

            if not check_graph_sanity(y_predicted, complete_graph):
                print "sanity check not passed."
                errors += 1
                y_predicted = {}

        except KeyError:
            print "Key Error."
            errors += 1
            y_predicted = {}

        return y_predicted, errors

    else:

        print "This should not happen."
