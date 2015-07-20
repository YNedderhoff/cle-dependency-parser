import codecs
from copy import deepcopy

from token import sentences

from scoring import score
from graphs import DepTree, FullGraph, SparseGraph, complete_graph
from cle import chu_liu_edmonds

def score_arcs(graph, w):  # f= feature vector, w = weight vector
    # the scoring function for arcs, the dot product of weight vector and feature vector
    g = deepcopy(graph)
    for head in g:
        for dependent in g[head]:
            score = 0
            for dimension in g[head][dependent][1]:
                score += dimension * w[dimension]
            g[head][dependent][0] = score
    return g

def sum_of_arc_feature_vectors(graph, l):
    # returns the added feature vectors of every arc
    sum_of_feat_vecs = []
    for i in range(l):
        sum_of_feat_vecs.append(0)
    for head in graph:
        for dependent in graph[head]:
            for feature in graph[head][dependent][1]:
                sum_of_feat_vecs[feature] += 1
    return sum_of_feat_vecs

def structured_perceptron(sparse_graph, feat_map, rev_feat_map, weight_vector, mode):

    y_gold = sparse_graph  # the correct tree

    g = complete_graph(sparse_graph, feat_map, rev_feat_map)  # the complete directed graph
    g_scored = score(g, weight_vector)

    y_predicted = chu_liu_edmonds(g_scored)

    if mode == "train":

        pass
        # adjust weights, return weight vector

    elif mode == "test":

        pass
        # write prediction into file

    else:

        print "This should not happen."

    return weight_vector

    """
        counter = 0
        for head in y_gold:
            for dependent in y_gold[head]:
                if y_gold[head][dependent][0] > 0.0:
                    counter+=1
        print counter
        y_scored = score_arcs(y_gold, w) # the scored, complete directed graph
        if not graph_sanity_check(g_scored): print "Error occurred in scored complete tree, perceptron"
        counter = 0
        for head in y_scored:
            for dependent in y_scored[head]:
                if y_scored[head][dependent][0] > 0.0:
                    counter+=1
        print counter
        counter = 0
        for head in g:
            for dependent in g[head]:
                if g[head][dependent][0] > 0.0:
                    counter+=1
        print counter
        counter = 0
        for head in g_scored:
            for dependent in g_scored[head]:
                if g_scored[head][dependent][0] > 0.0:
                    counter+=1
        print counter

        y_predicted = chu_liu_edmonds(g_scored) # the predicted graph
        if not graph_sanity_check(y_predicted): print "Error occurred in predicted tree, perceptron"
        if give_cycle(y_predicted, "0_Root", [], []): print "Predicted graph contains cycle."

        counter = 0
        for head in y_predicted:
            for dependent in y_predicted[head]:
                if y_predicted[head][dependent][0] > 0.0:
                    counter+=1
        print counter


        # print y_gold
        # print y_predicted

        if y_gold == y_predicted:

            correct += 1

        else:

            # adjust weights of the weight vector

            # print "Weights are being adjusted ..."

            tmp1 = sum_of_arc_feature_vectors(y_gold, len(w))
            tmp2 = sum_of_arc_feature_vectors(y_predicted, len(w))
            tmp3 = []
            for i in range(len(w)):
                tmp3.append(tmp1[i] - tmp2[i])
            tmp4 = []
            for i in range(len(w)):
                tmp4.append(tmp3[i] * 0.5)

            w_new = []
            for i in range(len(w)):
                w_new.append(w[i] + tmp4[i])

            if len(w_new) != len(w):
                print "The new weight vector has not the same length as the old one."

            w = w_new
        """



"""
    elif arguments.test:

        # the testing

        output = open(arguments.out_file, "w")
        output.close()

        total = 0

        for sentence in sentences(codecs.open(arguments.in_file, encoding='utf-8')):

            instance = Instance(sentence, feat_map)

            g = complete_directed_graph(instance, feat_map)  # the complete directed graph
            if not graph_sanity_check(g): print "Error occurred in complete tree, perceptron"

            g_scored = score_arcs(g, w) # the scored, complete directed graph
            if not graph_sanity_check(g_scored): print "Error occurred in scored complete tree, perceptron"

            y_predicted = chu_liu_edmonds(g_scored) # the predicted graph
            if not graph_sanity_check(y_predicted): print "Error occurred in predicted tree, perceptron"
            if give_cycle(y_predicted, "0_Root", [], []): print "Predicted graph contains cycle."

            # write predicted graph to the output file

            node_list = set()

            for head in y_predicted:
                for dependent in y_predicted[head]:
                    if not head == "0_Root":
                        node_list.add(head)
                    node_list.add(dependent)
            for element in sorted(node_list, key = lambda x: int(x.split("_")[0])):
                for head in y_predicted:
                    for dependent in y_predicted[head]:
                        if dependent == element:
                            output = open(arguments.out_file, "a")
                            print >> output, dependent.split("_")[0]+"\t"+ dependent.split("_")[1]+"\t"+instance.dep_tree.nodes[int(dependent.split("_")[0])].nodeToken.lemma+"\t"+instance.dep_tree.nodes[int(dependent.split("_")[0])].nodeToken.pos+"\t_\t_\t"+head.split("_")[0]+"\t"+"_"+"\t_\t_"
                            output.close()
            output = open(arguments.out_file, "a")
            print >> output, ""
            output.close()

            total += 1
            if total % 500 == 0:
                print "\t\t\tInstance Nr. " + str(total)
        print "\t\t" + str(total) + " sentences annotated."

    else:
        print "This should not happen."


    elif arguments.evaluate:
        print "Running in evaluation mode\n"
        out_stream = open(arguments.output_file, 'w')
        evaluate(arguments.in_file, out_stream)
        out_stream.close()
    elif arguments.tag:
        print "Running in tag mode\n"
        t.tag(arguments.in_file, arguments.model, arguments.output_file)

    """