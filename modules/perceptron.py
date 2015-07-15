import codecs
from copy import deepcopy

from graph import complete_directed_graph, graph_sanity_check, Instance
from cle import chu_liu_edmonds
from token import sentences

def score_arcs(graph, w):  # f= feature vector, w = weight vector
    g = deepcopy(graph)
    # the score function for Arcs, the dot product of weight vector and feature vector
    for head in g:
        for dependent in g[head]:
            score = 0
            for dimension in g[head][dependent][1]:
                score += dimension * w[dimension]
            g[head][dependent][0] = score
    return g

def sum_of_arc_feature_vectors(graph, l):
    sum_of_feat_vecs = []
    for i in range(l):
        sum_of_feat_vecs.append(0)
    for head in graph:
        for dependent in graph[head]:
            for feature in graph[head][dependent][1]:
                sum_of_feat_vecs[feature] += 1
    return sum_of_feat_vecs

def structured_perceptron(arguments, feat_map, weight_vector):  # training
    w = deepcopy(weight_vector)
    e = int(arguments.epochs)
    if arguments.train:
        for epoch in range(1, e + 1):
            print "\t\tEpoch: " + str(epoch)
            total = 0
            correct = 0
            instances = 0
            for sentence in sentences(codecs.open(arguments.in_file, encoding='utf-8')):

                instance = Instance(sentence, feat_map)

                instances += 1
                
                y_gold = instance.graph  # the correct tree
                if not graph_sanity_check(y_gold): print "Error occurred in gold tree, perceptron"

                g = complete_directed_graph(instance, feat_map)  # the complete directed graph
                if not graph_sanity_check(g): print "Error occurred in complete tree, perceptron"

                g_scored = score_arcs(g, w)
                if not graph_sanity_check(g_scored): print "Error occurred in scored complete tree, perceptron"

                y_predicted = chu_liu_edmonds(g_scored)
                if not graph_sanity_check(y_predicted): print "Error occurred in predicted tree, perceptron"

                # print y_gold
                # print y_predicted

                if not y_gold == y_predicted:
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

                else:
                    correct += 1
                total += 1
                if total % 500 == 0:
                    print "\t\t\tInstance Nr. " + str(total)
            print "\t\tTrained on " + str(total) + " sentences, with " + str(correct) + "classified correctly."
            print "Current weight vector:"
            print w
        return w

    elif arguments.test:

        output = open(arguments.out_file, "w")
        output.close()

        total = 0

        for sentence in sentences(codecs.open(arguments.in_file, encoding='utf-8')):

            instance = Instance(sentence, feat_map)

            g = complete_directed_graph(instance, feat_map)  # the complete directed graph
            if not graph_sanity_check(g): print "Error occurred in complete tree, perceptron"

            g_scored = score_arcs(g, w)
            if not graph_sanity_check(g_scored): print "Error occurred in scored complete tree, perceptron"

            y_predicted = chu_liu_edmonds(g_scored)
            if not graph_sanity_check(y_predicted): print "Error occurred in predicted tree, perceptron"

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

        """
    elif arguments.evaluate:
        print "Running in evaluation mode\n"
        out_stream = open(arguments.output_file, 'w')
        evaluate(arguments.in_file, out_stream)
        out_stream.close()
    elif arguments.tag:
        print "Running in tag mode\n"
        t.tag(arguments.in_file, arguments.model, arguments.output_file)
    """