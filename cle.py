#!/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import time
import numpy as np

class Token(object):
	"""
	Represents one token 
	(a non-empty line in CoNLL09 format).
	"""
	def __init__( self, line ):
		entries = line.split('\t')
		self.id = entries[0]
		self.form = entries[1]
		self.lemma = entries[2]
		self.pos = entries[3]
		self.head = entries[6]
		self.rel = entries[7].rstrip()

def sentences( filestream ):
	"""
	Generator that returns sentences as lists of Token objects.
	Reads CoNLL09 format.
	"""
	sentence = []
	for line in filestream:
		line = line.rstrip()
		if line:
			sentence.append(Token(line))
		elif sentence:
			yield sentence
			sentence = []
	if sentence:
		yield sentence

class Node:
	def __init__(self, token):
		#A node object contains a Token object (the head) and a list of other 	
		#Token objects (the dependants).
		self.nodeToken = token
		self.edges = []
	def addEdge(self, node):
		self.edges.append(node)

class DepTree:
	def __init__(self, sentence):
		#This is a dictionary of node Objects.
		self.nodes = {}
		self.nodes[0] = Node(Token("0\tRoot\t__NULL__\t__NULL__\t__NULL__\t__NULL__\t__NULL_\t__NULL__\t__NULL__\t__NULL__"))
		for tid, token in enumerate(sentence):
			self.nodes[tid+1] = Node(token)
		for tid, token1 in enumerate(sentence):
			if int(token1.head) == 0:
				self.nodes[0].addEdge(token1)
			for token2 in sentence:
				if token2.head == token1.id:
					self.nodes[tid+1].addEdge(token2)

class Instance:
	def __init__(self, sentence, featmap):
		#An instance object is a graph, represented as a dictionary.
		#This example {node1:{node2:[s, f]}} is a graph with two nodes
		#and one arc from node1 to node 2, with the score s and the feature vector f.
		T = DepTree(sentence)
		self.G = {}
		for n in T.nodes.keys():
			self.G[T.nodes[n].nodeToken.form] = {}
			if not T.nodes[n].edges == []:
				for e in T.nodes[n].edges:
					f = ArcfeatureVector(T.nodes[n].nodeToken, e, featmap)
					self.G[T.nodes[n].nodeToken.form][e.form] = [0.0, f]
		
					
def ArcfeatureVector (h, d, featmap):
	#returns a feature vector in sparse representation, given the feature map, a head and a dependant
	featv = {}
	featv[featmap["hform:"+h.form]] = 1
	featv[featmap["hpos:"+h.pos]] = 1
	featv[featmap["dform:"+d.form]] = 1
	featv[featmap["dpos:"+d.pos]] = 1
	featv[featmap["hform,dpos:"+h.form+","+d.pos]] = 1
	featv[featmap["hpos,dform:"+h.pos+","+d.form]] = 1
	return featv

def CompleteDirectedGraph (ins):
	#converts directed Graph into a complete directed Graph. The new arcs have the score 0.0 and 
	#a feature vector consisting of zeroes.
	a = {}
	for v in ins.keys():
		a[v] = {}
		for v2 in ins.keys():
			if not v2 == v:
				if v2 in ins[v].keys():
					a[v][v2] = ins[v][v2]
				if not v2 in ins[v].keys():
					a[v][v2] = [0.0, {}]
	return a


def fm (infile):
	#takes a file in conll09 format, returns a feature map
	featmap={} #featmap as dictionary {feature:index}
	index=0 #index in featmap
	start = time.time()
	print >> sys.stderr, "Creating featuremap..."
	for sentence in sentences(codecs.open(infile,encoding='utf-8')):
		local_features=[]
		for token1 in sentence:
			if int(token1.head) == 0:
				#at this point ROOT is the head and token1 is the dependent
				local_features.append("hform:Root")
				local_features.append("hpos:__NULL__")
				local_features.append("dform:"+token1.form)
				local_features.append("dpos:"+token1.pos)
				local_features.append("hform,dpos:"+"Root"+","+token1.pos)
				local_features.append("hpos,dform:"+"__NULL__"+","+token1.form)
		for token1 in sentence:	
			for token2 in sentence:
				if token2.head == token1.id:
					#at this point, token1 is the head, and token2 the dependent
					local_features.append("hform:"+token1.form)
					local_features.append("hpos:"+token1.pos)
					local_features.append("dform:"+token2.form)
					local_features.append("dpos:"+token2.pos)
					local_features.append("hform,dpos:"+token1.form+","+token2.pos)
					local_features.append("hpos,dform:"+token1.pos+","+token2.form)
		for feature in local_features:
			start3=time.time()
			if not feature in featmap:
				featmap[feature]=index
				index+=1
	stop = time.time()
	print >> sys.stderr, "\tNumber of features: "+str(len(featmap))
	print >> sys.stderr, "\tDone, "+str(stop-start)+" sec"
	return featmap
					
def createInstances (infile, featmap):
	#creates a dictionary with numbers as keys and Instances in the Format (sentence, Instance object)
	#as values
	start = time.time()
	ins = {}
	print >> sys.stderr, "Creating instances..."
	scount=0
	for sentence in sentences(codecs.open(infile,encoding='utf-8')):
		s = ""
		for token in sentence:
			s+=token.form+" "
		ins[scount] = [s.rstrip(), Instance(sentence, featmap)]
		scount+=1
	stop = time.time()
	print >> sys.stderr, "\tDone, "+str(stop-start)+" sec"
	return ins

def expandFeatureVector(sparseRep, featcount):
	#convert sparse representation of feature vector to full feature vector
	featvec = np.zeros(shape=(featcount,1))
	for f_index in sparseRep.keys():
		featvec[f_index] = [sparseRep[f_index]]
	return featvec

def generateWeightVector(l):
	#returns lx1 vector, filled with zeroes
	#w = np.ones(shape=(l,1))
	w = np.zeros(shape=(l,1))
	return w
	

def scoreArcs(graph, w): # f= feature vector, w = weight vector
	#the score function for Arcs, the dot product of weight vector and feature vector
	for node in graph.keys():
		for arc in graph[node].keys():
			graph[node][arc][0] = np.vdot(w, expandFeatureVector(graph[node][arc][1], len(w)))

def cycle(graph):
	for node in graph.keys():
		for arc in graph[node].keys():
			if node in graph[arc].keys():
				return True
			else: return False
def giveCycle(graph):
	for node in graph.keys():
		for arc in graph[node].keys():
			if node in graph[arc].keys():
				return [node, arc]

def removeCycle(graph, cycle): #incomplete
	pass

def sumOfArcFeatureVectors(graph, l):
	featvec = np.zeros(shape=(l,1))
	vec = []
	for node in graph.keys():
		for arc in graph[node].keys():
			vec.append(expandFeatureVector(graph[node][arc][1], l))
	for i in range(0, l):
		su = 0
		for vector in vec:
			su += vector[i]
		featvec[i] = [su]
	return featvec
			

def StructuredPerceptron(ins, w, epochs): #training
	#w[-1]=[3.57]
	#print np.vdot(v, w)
	print >> sys.stderr, "Start training ..."
	for epoch in range(1, epochs):
		print >> sys.stderr, "\tEpoch: "+str(epoch)
		total = 0
		correct = 0
		for instance in ins.keys():
			G = ins[instance][1].G # the correct tree
			F = CompleteDirectedGraph(ins[instance][1].G) # the complete directed graph
			scoreArcs(F, w)
			y = ChuLiuEdmonds(F, w)
			
			if not y == G:
				tmp1 = sumOfArcFeatureVectors(G, len(w))	
				tmp2 = sumOfArcFeatureVectors(y, len(w))	
				w = w+0.5*(tmp1-tmp2)
			else: correct+=1
			total+=1
			if total%500 == 0:
				print >> sys.stderr, "\t\tInstance Nr. "+str(total)
		print total, correct

def ChuLiuEdmonds(F, w): #incomplete
	if cycle(F) == False:
		return F
	else:
		C = giveCycle(F)
		FC = Contract(F,C,w)
		return FC

def Contract(F, C, w): #incomplete
	FC = removeCycle(F, C)
	return FC


def run(args):
	outstream = open(args.outputfile,'w')

	#featmap is a dictionary with every existing feature in the training data as keys,
	#and unique indexes as values. Example: u'hpos,dform:VBD,way': 3781
	featmap=fm(args.inputfile)

	#instances is a dictionary, containing a index as a key and a list,
	#containing a sentence string and a Instance object.
	instances=createInstances(args.inputfile, featmap)

	#print all sentences and their feature vector sparse representations:
	"""
	for sentence_id in instances.keys():
		print sentence_id+1
		print instances[sentence_id][0]
		print featvec[sentence_id]
	"""
	StructuredPerceptron(instances, generateWeightVector(len(featmap)), 10)
	
	#print np.vdot(w, a)
	outstream.close()

def write_to_file( token, fileobj  ):

	print >> fileobj, str(token.id)+"\t"+str(token.form)+"\t"+str(token.lemma)+"\t"+str(token.pos)+"\t"+"_"+"\t"+"_"+"\t"+str(token.head)+"\t"+str(token.rel)+"\t"+"_"+"\t"+"_"		


if __name__=='__main__':
	import argparse

	argpar = argparse.ArgumentParser(description='Creates a file in different POS taggers format for a given file in CoNLL09 format')

	argpar.add_argument('-i','--input',dest='inputfile',help='input file',required=True)
	argpar.add_argument('-o','--output',dest='outputfile',help='output file',required=True)
	argse = argpar.parse_args()
	run(argse)
	








