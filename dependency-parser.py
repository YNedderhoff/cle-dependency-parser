# !/bin/python
#  -*- coding: utf-8 -*-

import time
import os

import cPickle
import gzip

from modules.perceptron import structured_perceptron
from modules.featmap import fm


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

    stop = time.time()
    print "\t\tNumber of features: " + str(len(feat_map))
    print "\t\tDone, " + str(stop - start) + " sec"

    start = time.time()
    print "\tRunning the perceptron on '" + args.in_file + "' ..."

    w = structured_perceptron(arguments, feat_map, create_weight_vector(len(feat_map)))

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

    start = time.time()
    print "\tSaving the model and the features to file '" +str(args.model) + "'..."

    save(args.model, [feat_map, w])

    stop = time.time()
    print "\t\tDone, " + str(stop - start) + " sec"

def test(args):
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

    # run_tests()
    # run(arguments)
