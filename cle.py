# !/bin/python
#  -*- coding: utf-8 -*-

import sys
import time
import numpy as np
from copy import deepcopy

from modules.graph import complete_directed_graph, create_instances
from modules.featmap import fm



def expand_feature_vector(sparse_feature_vector, feature_count):
    # convert sparse representation of feature vector to full feature vector
    feat_vec = np.zeros(shape=(feature_count, 1))
    for f_index in sparse_feature_vector.keys():
        feat_vec[f_index] = [sparse_feature_vector[f_index]]
    return feat_vec

def generate_weight_vector(l):
    # returns lx1 vector, filled with zeroes
    # w = np.ones(shape=(l,1))
    # w = np.zeros(shape=(l,1))
    w = np.empty(shape=(l,1))
    w.fill(0.5)
    return w


def score_arcs(graph, w):  # f= feature vector, w = weight vector
    g = deepcopy(graph)
    # the score function for Arcs, the dot product of weight vector and feature vector
    for node in g.keys():
        for arc in g[node].keys():
            g[node][arc][0] = np.vdot(w, expand_feature_vector(g[node][arc][1], len(w)))
    return g

def cycle(graph):
    # doesn't find cycles with more than two nodes, have to change that
    for node in graph.keys():
        for arc in graph[node].keys():
            if arc in graph.keys():
                if node in graph[arc].keys():
                    return True
                else:
                    return False
            else: return False

def give_cycle(graph):
    # change format to dict where you can always see the head
    for node in graph.keys():
        for arc in graph[node].keys():
            if arc in graph.keys():
                if node in graph[arc].keys():
                    return [node, arc]

def delete_key(in_dict, key):
    to_convert_dict = deepcopy(in_dict)
    del to_convert_dict[key]
    return to_convert_dict

def remove_cycle(graph, cycle_nodes):  # incomplete
    deleted1 = False
    deleted2 = False
    g = deepcopy(graph)
    for node in g.keys():
        if node == cycle_nodes[0]:
            for arc in g[node].keys():
                if arc == cycle_nodes[1]:
                    g[node] = delete_key(g[node], arc)
                    deleted1 = True
        if node == cycle_nodes[1]:
            for arc in g[node].keys():
                if arc == cycle_nodes[0]:
                    g[node] = delete_key(g[node], arc)
                    deleted2 = True
    if not deleted1:
        print "Couldn't delete first arc."
    if not deleted2:
        print "Couldn't delete second arc."
    return g


def sum_of_arc_feature_vectors(graph, l):
    feat_vec = np.zeros(shape=(l, 1))
    vec = []
    for node in graph.keys():
        for arc in graph[node].keys():
            vec.append(expand_feature_vector(graph[node][arc][1], l))
    for i in range(0, l):
        su = 0
        for vector in vec:
            su += vector[i]
        feat_vec[i] = [su]
    return feat_vec


def structured_perceptron(ins, w, epochs): # training
    # w[-1]=[3.57]
    # print np.vdot(v, w)
    print >> sys.stderr, "Start training ..."
    for epoch in range(1, epochs):
        print >> sys.stderr, "\tEpoch: "+str(epoch)
        total = 0
        correct = 0
        for instance in ins.keys():
            y_gold = ins[instance][1].G  # the correct tree

            g = complete_directed_graph(ins[instance][1].G)  # the complete directed graph

            g_scored = score_arcs(g, w)

            y_predicted = chu_liu_edmonds(g_scored)

            # print y_gold
            # print y_predicted
            """
            if not y == G:
                tmp1 = sumOfArcFeatureVectors(G, len(w))	
                tmp2 = sumOfArcFeatureVectors(y, len(w))	
                w = w+0.5*(tmp1-tmp2)
            else: correct+=1
            """
            total += 1
            if total%500 == 0:
                print >> sys.stderr, "\t\tInstance Nr. "+str(total)
        print total, correct

def highest_incoming_heads(graph):
    # graph2 is the graph with every dependent only have their head with the highest score
    d = {}
    for head in graph:
        for arc in graph[head]:
            if arc in d:
                if graph[head][arc][0] > d[arc][1][0]:
                        d[arc] = [head, [graph[head][arc][0], graph[head][arc][1]]]
            else:
                d[arc] = [head, [graph[head][arc][0], graph[head][arc][1]]]

    graph2 = {}
    for dependent in d:
        if d[dependent][0] in graph2:
            graph2[d[dependent][0]][dependent] = d[dependent][1]
        else:
            graph2[d[dependent][0]] = {dependent : d[dependent][1]}
    return graph2

def chu_liu_edmonds(in_g):  # incomplete

    g = deepcopy(in_g)
    g_a = highest_incoming_heads(g)

    if not cycle(g_a):
        return g_a
    else:

        c = give_cycle(g_a)
        g_c = contract(g_a, c)
        y = chu_liu_edmonds(g_c)
        """
        for d in c:
            for head in g_a:
                for dependent in g_a[head]:
        """
        return g_c

def contract(g_a_in, c): # incomplete

    g_a = deepcopy(g_a_in)
    # remove Cycle
    g_c = remove_cycle(g_a, c)

    # check if exactly to arcs have been removed
    counter = 0
    for key in g_a:
        if len(g_c[key]) != len(g_a[key]):
            if len(g_c[key]) == len(g_a[key])-1:
                counter += 1
    if counter != 2:
        print "Contract function didn't remove exactly two arcs."

    # add tc to represent C
    g_c[c[0]+"-"+c[1]] = {}

    # arcs leaving C
    # for every dependent d: if a node out of C is head of d: add new arc <c, d> with score !?
    new_arcs = {}
    for head in g_c:
        if head in c:
            for dependent in g_c[head]:
                if dependent not in c:
                    if dependent in new_arcs:
                        if new_arcs[dependent] < g_c[head][dependent][0]:
                            new_arcs[dependent] = g_c[head][dependent][0]
                    else:
                        new_arcs[dependent] = g_c[head][dependent][0]
    for dependent in new_arcs:
        g_c[c[0]+"-"+c[1]][dependent] = [new_arcs[dependent], {}]

    score_c = 0 # cycle score s(c)
    for head in g_a:
        if head in c:
            for dependent in g_a[head]:
                if dependent in c:
                    score_c += g_a[head][dependent][0]

    # arcs entering C
    new_arcs = {}
    for head in g_c:
        if head not in c:
            for dependent in g_c[head]:
                if dependent in c:
                    score_h_d = g_c[head][dependent][0] # score of the arc entering c and the dependent
                    score_hd_d = 0 # score of the head of td in c and td
                    for head_2 in g_a:
                        if head_2 in c:
                            if dependent in g_a[head_2]:
                                score_hd_d = g_a[head_2][dependent]
                    if head in new_arcs:
                        if new_arcs[head] < score_h_d + score_c - score_hd_d:
                            new_arcs[head] = score_h_d + score_c - score_hd_d
                    else:
                        new_arcs[head] = score_h_d + score_c - score_hd_d
    for head in new_arcs:
        g_c[head][c[0]+"-"+c[1]] = [new_arcs[head], {}]

    return g_c


def run(args):
    outstream = open(args.outputfile,'w')

    # feat map is a dictionary with every existing feature in the training data as keys,
    # and unique indexes as values. Example: u'hpos,dform:VBD,way': 3781

    start = time.time()
    print >> sys.stderr, "Creating feature map..."

    feat_map = fm(args.inputfile)

    stop = time.time()
    print >> sys.stderr, "\tNumber of features: "+str(len(feat_map))
    print >> sys.stderr, "\tDone, "+str(stop-start)+" sec"

    # instances is a dictionary, containing a index as a key and a list,
    # containing a sentence string and a Instance object.

    start = time.time()
    print >> sys.stderr, "Creating instances..."

    instances = create_instances(args.inputfile, feat_map)

    stop = time.time()
    print >> sys.stderr, "\tDone, "+str(stop-start)+" sec"

    # print all sentences and their feature vector sparse representations:
    """
    for sentence_id in instances.keys():
        print sentence_id+1
        print instances[sentence_id][0]
        print instances[sentence_id][1].G
        #print featvec[sentence_id]
    """
    structured_perceptron(instances, generate_weight_vector(len(feat_map)), 10)

    # print np.vdot(w, a)
    outstream.close()

def write_to_file(token, file_obj):

    print >> file_obj, str(token.id)+"\t"+str(token.form)+"\t"+str(token.lemma)+"\t"+str(token.pos)+"\t"+"_"+"\t"+"_"+"\t"+str(token.head)+"\t"+str(token.rel)+"\t"+"_"+"\t"+"_"


if __name__=='__main__':
    import argparse

    arg_par = argparse.ArgumentParser(description='')

    arg_par.add_argument('-i','--input',dest='inputfile',help='input file',required=True)
    arg_par.add_argument('-o','--output',dest='outputfile',help='output file',required=True)
    arguments = arg_par.parse_args()
    run(arguments)









