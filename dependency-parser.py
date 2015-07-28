# !/bin/python
#  -*- coding: utf-8 -*-

import time
import os
import codecs
import random

import cPickle
import gzip

from copy import deepcopy

from modules.perceptron import structured_perceptron
from modules.token import sentences
from modules.featmap import fm, add_feat_vec_to_sparse_graph, add_feat_vec_to_full_graph, reverse_feat_map
from modules.graphs import CompleteFullGraph, FullGraph, SparseGraph, write_graph_to_file
from modules.evaluation import evaluate

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
    print "\tCreating sparse graph representation of every sentence..."

    sparse_graphs = {}

    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):

        full_graph = FullGraph(sentence).heads
        sparse_graph = SparseGraph(sentence).heads

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
        sparse_graph = add_feat_vec_to_sparse_graph(full_graph, sparse_graph, feat_map)

        # check if every feature vector is filled with the correct number of features.

        for head in sparse_graph:
            for arc in sparse_graph[head]:
                if arc.feat_vec:
                    if arc.head == 0:
                        if len(arc.feat_vec) != 10:
                            print "Length of arc feature vector is wrong."
                            print arc.feat_vec
                    else:
                        if len(arc.feat_vec) != 20:
                            print "Length of arc feature vector is wrong."
                            print arc.feat_vec
                else:
                    print "Error: Feature vector is empty."

        sparse_graphs[len(sparse_graphs)] = sparse_graph

    stop = time.time()
    print "\t\tNumber of sentences: " + str(len(sparse_graphs))
    print "\t\tDone, " + str(stop - start) + " sec"

    start = time.time()
    print "\tStart training, Total Instances: " + str(len(sparse_graphs))

    if args.decrease_alpha:
        print "\t\tReduce smoothing coefficient activated."

    alpha = 0.5  # smoothing coefficient for the weight adjustments
    graph_ids = sparse_graphs.keys()  # list of dict keys, needed when shuffeling tokens after every epoch

    for epoch in range(1, int(args.epochs) + 1):

        print "\t\tEpoch: " + str(epoch) + ", Smoothing coefficient: " + str(alpha)

        total = 0
        correct = 0
        errors = 0

        for graph_id in graph_ids:
            weight_vector, correct, errors = structured_perceptron(deepcopy(sparse_graphs[graph_id]), feat_map, rev_feat_map, weight_vector, correct, errors, "train", alpha)
            total += 1
            if total % 500 == 0:
                print "\t\t\tInstance Nr. " + str(total) + "\tCorrect: " + str(correct) + "\t(" \
                    + str((correct*100)/total) + "%)\tErrors: " + str(errors)
                # print "\t\t\tCurrent weight vector:"
                # print "\t\t\t" + str(weight_vector)

        if args.decrease_alpha:  # decrease alpha after every epoch
            alpha /= 2

        if args.shuffle_sentences:  # shuffle sentences after every epoch
            random.shuffle(graph_ids)

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

    start = time.time()
    print "\tSaving the model and the features to file '" + str(args.model) + "'..."

    save(args.model, [feat_map, weight_vector])

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

def test(args):

    # load classifier vectors (model) and feature vector from file:
    print "\tLoading the model and the features from file '" + str(args.model) + "'"
    start = time.time()

    model_list = load(args.model)
    feat_map = model_list[0]
    rev_feat_map = reverse_feat_map(feat_map)
    weight_vector = model_list[1]

    stop = time.time()
    print "\t\t" + str(len(feat_map)) + " features loaded"
    print "\t\tDone, " + str(stop - start) + " sec."
    start = time.time()
    sentence_count = 0
    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):
        sentence_count += 1

    print "\tStart annotating the test file, Total Instances: " + str(sentence_count)

    total = 0
    errors = 0

    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):

        # create complete, directed graph representation of sentence
        full_graph = CompleteFullGraph(sentence).heads

        # add feature vec
        full_graph = add_feat_vec_to_full_graph(full_graph, feat_map)

        tmp_errors = errors

        predicted_graph, errors = structured_perceptron(deepcopy(full_graph), feat_map, rev_feat_map, weight_vector, 0, errors, "test")

        if tmp_errors == errors:  # no error occured during prediction
            write_graph_to_file(predicted_graph, args.out_file)
        else:  # a error occured during prediction
            write_graph_to_file(full_graph, args.out_file, "error")

        total += 1
        if total % 500 == 0:
            print "\t\tInstance Nr. " + str(total) + "\tErrors: " + str(errors)
            # print "\t\t\tCurrent weight vector:"
            # print "\t\t\t" + str(weight_vector)
    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

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
    arg_par.add_argument('-g', '--gold', dest='gold', help='gold', default='gold.conll06')
    arg_par.add_argument('-o', '--output', dest='out_file', help='output file', default='predicted.conll06')
    arg_par.add_argument('-e', '--epochs', dest='epochs', help='epochs', default='10')
    arg_par.add_argument('-decrease-alpha', dest='decrease_alpha', action='store_true', help='decrease alpha', default=False)
    arg_par.add_argument('-shuffle-sentences', dest='shuffle_sentences', action='store_true', help='shuffle sentences', default=False)

    arguments = arg_par.parse_args()

    if os.stat(arguments.in_file).st_size == 0:
        print "Input file is empty"
    else:
        if arguments.train:
            print "Running in training mode\n"
            train(arguments)

        elif arguments.test:
            print "Running in test mode\n"
            test(arguments)

        elif arguments.evaluate:
            print "Running in evaluation mode\n"
            evaluate(arguments)
        """
        elif arguments.tag:
            print "Running in tag mode\n"
            t.tag(arguments.in_file, arguments.model, arguments.output_file)

        """

    t1 = time.time()
    print "\n\tDone. Total time: " + str(t1 - t0) + "sec.\n"
