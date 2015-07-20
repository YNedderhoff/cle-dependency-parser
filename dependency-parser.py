# !/bin/python
#  -*- coding: utf-8 -*-

import time
import os
import codecs

import cPickle
import gzip

from modules.perceptron import structured_perceptron
from modules.token import sentences
from modules.featmap import fm, add_feat_vec, reverse_feat_map
from modules.scoring import score
from modules.graphs import DepTree, FullGraph, SparseGraph

def create_weight_vector(l):
    # returns a list of length len(l) filled with 0.0
    w = []
    for i in range(l):
        w.append(0.0)
    return w


def load(file_name):
    # load the model (weight vectors) from a file:
    stream = gzip.open(file_name, "rb")
    model = cPickle.load(stream)
    stream.close()
    return model


def save(file_name, model):
    # save the model (weight vectors) to a file:
    stream = gzip.open(file_name, "wb")
    cPickle.dump(model, stream)
    stream.close()


def train(args):

    start = time.time()
    print "\tCreating feature map..."

    # feat map is a dictionary with every existing feature in the training data as keys,
    # and unique indexes as values. Example: u'hpos,dform:VBD,way': 3781
    feat_map = fm(args.in_file)
    rev_feat_map = reverse_feat_map(feat_map)
    stop = time.time()
    print "\t\tNumber of features: " + str(len(feat_map))
    print "\t\tDone, " + str(stop - start) + " sec"

    start = time.time()
    print "\tCreating weight vector..."

    weight_vector = create_weight_vector(len(feat_map))

    stop = time.time()
    print "\t\tNumber of features: " + str(len(feat_map))
    print "\t\tDone, " + str(stop - start) + " sec"

    start = time.time()
    print "\tCreating sparse representation of every sentence..."

    sparse_graphs = {}

    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):

        dep_tree = DepTree(sentence).nodes
        full_graph = FullGraph(dep_tree).heads
        sparse_graph = SparseGraph(dep_tree).heads

        # Check if full_graph and sparse_graph ids match at every point
        for full_head in full_graph:
            for full_arc in full_graph[full_head]:
                counter = 0
                for sparse_arc in sparse_graph[full_head]:
                    if full_arc.dependent == sparse_arc.dependent:
                        counter += 1
                if counter != 1:
                    print "Error: The full and sparse graph representations do not match."

        # add feature vec to every graph
        sparse_graph = add_feat_vec(full_graph, sparse_graph, feat_map)

        # check if every feature vector is filled with the correct number of features.

        for head in sparse_graph:
            for arc in sparse_graph[head]:
                if not arc.feat_vec:
                    print "Error: Feature vector is empty."
                elif len(arc.feat_vec) != 6 and arc.head != 0:
                    print "Length of arc feature vector is wrong."
                    print arc.feat_vec
                elif len(arc.feat_vec) != 2 and arc.head == 0:
                    print "Length of arc feature vector is wrong (__ROOT__ arc)."
                    print arc.feat_vec

        sparse_graphs[len(sparse_graphs)] = sparse_graph
    stop = time.time()
    print "\t\tNumber of sentences: " + str(len(sparse_graphs))
    print "\t\tDone, " + str(stop - start) + " sec"

    start = time.time()
    print "\tStart training..."

    for epoch in range(1, int(args.epochs) + 1):
        print "\t\tEpoch: " + str(epoch)
        total = 0

        for graph_id in sparse_graphs:
            weight_vector = structured_perceptron(sparse_graphs[graph_id], feat_map, rev_feat_map, weight_vector, "train")
            total += 1
            if total % 500 == 0:
                print "\t\t\tInstance Nr. " + str(total)
    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

    """
    start = time.time()
    print "\tSaving the model and the features to file '" +str(args.model) + "'..."

    save(args.model, [feat_map, w])

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"
    """

def test(args):
    """
    # load classifier vectors (model) and feature vector from file:
    print "\tLoading the model and the features from file '" + str(args.model) + "'"
    start = time.time()

    model_list = load(args.model)
    feat_map = model_list[0]
    w = model_list[1]

    stop = time.time()
    print "\t\t" + str(len(feat_map)) + " features loaded"
    print "\t\tDone, " + str(stop - start) + " sec."

    start = time.time()
    print "\tAnnotate file '" + args.in_file + "'..."

    structured_perceptron(args, feat_map, w)

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"
    """

def write_to_file(token, file_obj):
    print >> file_obj, str(token.id) + "\t" + str(token.form) + "\t" + str(token.lemma) + "\t" + str(
        token.pos) + "\t" + "_" + "\t" + "_" + "\t" + str(token.head) + "\t" + str(token.rel) + "\t" + "_" + "\t" + "_"


if __name__ == '__main__':

    t0 = time.time()

    import argparse

    arg_par = argparse.ArgumentParser(description='')

    mode = arg_par.add_mutually_exclusive_group(required=True)
    mode.add_argument('-train', dest='train', action='store_true', help='run in training mode')
    mode.add_argument('-test', dest='test', action='store_true', help='run in test mode')
    mode.add_argument('-ev', dest='evaluate', action='store_true', help='run in evaluation mode')
    mode.add_argument('-tag', dest='tag', action='store_true', help='run in tagging mode')

    arg_par.add_argument('-i', '--input', dest='in_file', help='input file', required=True)
    arg_par.add_argument('-m', '--model', dest='model', help='model', default='model')
    arg_par.add_argument('-o', '--output', dest='out_file', help='output file', default='predicted.col')
    arg_par.add_argument('-e', '--epochs', dest='epochs', help='epochs', default='10')

    arguments = arg_par.parse_args()

    if os.stat(arguments.in_file).st_size == 0:
        print "Input file is empty"
    else:
        if arguments.train:
            print "Running in training mode\n"
            train(arguments)
            #cle(arguments)

        elif arguments.test:
            print "Running in test mode\n"
            test(arguments)

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
    t1 = time.time()
    print "\n\tDone. Total time: " + str(t1 - t0) + "sec.\n"
    """
    test_tree = {
        "0_Root": {
            "1_John": [9.0, {}],
            "2_saw": [10.0, {}],
            "3_Mary": [9.0, {}]
        },
        "1_John": {
            "2_saw": [20.0, {}],
            "3_Mary": [11.0, {}]
        },
        "2_saw": {
            "1_John": [30.0, {}],
            "3_Mary": [30.0, {}]
        },
        "3_Mary": {
            "1_John": [11.0, {}],
            "2_saw": [0.0, {}]
        }
    }

    test_tree2 = {
        "0_Root": {
            "1_John": [5.0, {}],
            "2_saw": [10.0, {}],
            "3_Mary": [15.0, {}]
        },
        "1_John": {
            "2_saw": [25.0, {}],
            "3_Mary": [25.0, {}]
        },
        "2_saw": {
            "1_John": [20.0, {}],
            "3_Mary": [15.0, {}]
        },
        "3_Mary": {
            "1_John": [10.0, {}],
            "2_saw": [30.0, {}]
        }
    }
    predicted = chu_liu_edmonds(test_tree2)
    print predicted


    # run_tests()
    # run(arguments)
    """
