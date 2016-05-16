#!/usr/bin/python3
import theano
import sys,pprint
import operator
import numpy as np
from sklearn.cluster import KMeans
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
from gensim.models import LsiModel, LogEntropyModel
from gensim.similarities import Similarity
import pickle
from  collections import defaultdict

#Input : Background corpus, Actual Corpus
def tokenizer(string):
    return string.split(' ')

def createcorpus(bg_corpus,output_dictionary,output_serialize):
	# Generating a training/background corpus from your own source of documents
	#saving dictionary and corpus in Matrix method form
	print("Creating corpus and dictionary")
	background_corpus = TextCorpus(input=bg_corpus)
	background_corpus.dictionary.save(output_dictionary)
	MmCorpus.serialize(output_serialize,background_corpus)  
	return background_corpus,background_corpus.dictionary


def model_construction(corpus_in,dictionary_in):
	# Revive a corpus
	# Load a dictionary
	# Log Entropy weights frequencies of all document features in the corpus
	# The tokenizer used to create the Background corpus
	# Creates LSI transformation model, LogEnt transformation model from log entropy corpus representation. 
	# Can persist transformation models, too.
	logent_transformation = LogEntropyModel(corpus_in,id2word=dictionary_in)
	tokenize_func = tokenizer  
	lsi_transformation = LsiModel(corpus=logent_transformation[corpus_in], id2word=dictionary_in)
	#logent_transformation.save("logent.model")
	#lsi_transformation.save("lsi.model")
	return lsi_transformation,logent_transformation

def finding_similarity(input_file,dictionary,lsi_transformation,logent_transformation):
	# This index corpus consists of what you want to compare future queries against
	# A corpus can be anything, as long as iterating over it produces a representation of the corpus documents as vectors.
	reader = open(input_file)
	index_documents = reader.readlines()
	tokenize_func=tokenizer
	corpus_actual = (dictionary.doc2bow(tokenize_func(document.strip())) for document in index_documents)
	index = Similarity(corpus=lsi_transformation[logent_transformation[corpus_actual]], output_prefix="shard",num_features=200)
	return index

def main():
	writer=open("final_clusters.p","w")
	output_dictionary ="bg_dict.dict"
	output_serialize = "bg_corpus.mm"
	print "Creating corpus"
	corpus,dictionary =createcorpus(sys.argv[1],output_dictionary,output_serialize)
	pprint.pprint(corpus) 
	print "Creating model"
	lsi,logent = model_construction(corpus,dictionary)
	print "Finding Similarity"
	c_index=finding_similarity(sys.argv[2],dictionary,lsi,logent)
	sim_matrix=[]
	#print len(c_index)
	#print c_index
	print "Creating Similarity Matrix"
	for s,i in zip(c_index,range(len(c_index))):
		temp=[]
		for a in s:
			temp.append(a)
		sim_matrix.append(temp)
	print len(np.array(sim_matrix))
	print "Starting Clustering"	
	est= KMeans(n_clusters=100)			
	est.fit(np.array(sim_matrix))
	labels=est.labels_
	print "Clustering Ends"
	clusters=defaultdict(list)
	for k,lab in zip(range(len(est.labels_)),est.labels_) :
		clusters[lab].append(k) 
		print k,lab 
	for clust in clusters:
  		pickle.dump(clusters[clust],writer)
  	writer.close()	
main()