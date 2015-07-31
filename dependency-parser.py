# !/bin/python
#  -*- coding: utf-8 -*-

import cProfile

import time
import os
import codecs

import cPickle
import gzip

from modules.perceptron import structured_perceptron
from modules.token import sentences
from modules.featmap import fm
from modules.graphs import Graph, write_graph_to_file
from modules.evaluation import evaluate


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

    print "\tCreating feature map..."
    start = time.time()

    feat_map = fm(args.in_file)

    stop = time.time()
    print "\t\tNumber of features: " + str(len(feat_map))
    print "\t\tDone, " + str(stop - start) + " sec"

    print "\tCreating weight vector..."
    start = time.time()

    weight_vector = [0.0 for i in xrange(len(feat_map))]

    stop = time.time()
    print "\t\tLength of weight vector: " + str(len(weight_vector))
    print "\t\tDone, " + str(stop - start) + " sec"

    print "\tCounting sentences..."
    start = time.time()

    sentence_count = 0
    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):
        sentence_count += 1

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

    print "\tStart training, Total Instances: " + str(sentence_count)
    start = time.time()

    if args.decrease_alpha:
        print "\t\tReduce smoothing coefficient activated."

    alpha = 0.5  # smoothing coefficient for the weight adjustments

    for epoch in range(1, int(args.epochs) + 1):

        start2 = time.time()

        print "\t\tEpoch: " + str(epoch) + ", Smoothing coefficient: " + str(alpha)

        total = 0
        correct = 0
        errors = 0

        for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):

            sparse_graph = Graph(sentence, "sparse", feat_map).heads  # gold graph
            complete_sparse_graph = Graph(sentence, "complete-sparse", feat_map, weight_vector).heads  # complete graph

            # call the perceptron
            weight_vector, correct, errors = structured_perceptron(complete_sparse_graph, weight_vector, correct,
                                                                   errors, "train", sparse_graph, alpha)

            total += 1

            # print some information every 500 sentences
            if total % 500 == 0:
                stop2 = time.time()
                print "\t\t\tInstance Nr. " + str(total) + "\tCorrect: " + str(correct) + "\t(" \
                      + str((correct * 100) / total) + "%)\tErrors: " + str(errors) + "\t" + str(stop2-start2) + " sec"
                start2 = time.time()

        # decrease alpha after every epoch if activated
        if args.decrease_alpha:
            alpha /= 2

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

    print "\tSaving the model and the features to file '" + str(args.model) + "'..."
    start = time.time()

    save(args.model, [feat_map, weight_vector])

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"


def test(args):

    # load classifier vectors (model) and feature vector from file:
    print "\tLoading the model and the features from file '" + str(args.model) + "'"
    start = time.time()

    model_list = load(args.model)
    feat_map = model_list[0]
    weight_vector = model_list[1]

    stop = time.time()
    print "\t\t" + str(len(feat_map)) + " features loaded"
    print "\t\tDone, " + str(stop - start) + " sec."

    print "\tCounting sentences..."
    start = time.time()

    sentence_count = 0
    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):
        sentence_count += 1

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

    print "\tStart annotating the test file, Total Instances: " + str(sentence_count)
    start = time.time()

    total = 0
    errors = 0

    for sentence in sentences(codecs.open(args.in_file, encoding='utf-8')):

        # complete graph in full arc representation
        full_graph = Graph(sentence, "complete-full", feat_map, weight_vector).heads

        tmp_errors = errors

        # call the perceptron
        predicted_graph, errors = structured_perceptron(full_graph, weight_vector, 0, errors, "test", None)

        if tmp_errors == errors:  # no error occured during prediction
            write_graph_to_file(predicted_graph, args.out_file)
        else:  # an error occured during prediction
            write_graph_to_file(full_graph, args.out_file, "error")

        total += 1

        # print some information every 500 sentences
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
    arg_par.add_argument('-decrease-alpha', dest='decrease_alpha', action='store_true', help='decrease alpha',
                         default=False)
    arg_par.add_argument('-shuffle-sentences', dest='shuffle_sentences', action='store_true', help='shuffle sentences',
                         default=False)

    arguments = arg_par.parse_args()

    if os.stat(arguments.in_file).st_size == 0:
        print "Input file is empty"

    else:

        if arguments.train:
            print "Running in training mode\n"
            train(arguments)
            # cProfile.run("train(arguments)")

        elif arguments.test:
            print "Running in test mode\n"
            test(arguments)

        elif arguments.evaluate:
            print "Running in evaluation mode\n"
            evaluate(arguments)

    t1 = time.time()
    print "\n\tDone. Total time: " + str(t1 - t0) + " sec.\n"
