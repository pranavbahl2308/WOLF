__author__ = 'Pranav Bahl'

import os
import arff
import yaml
import random, math
import sys, getopt
import numpy as np
from array import array
from scipy.io.arff import loadarff

def splitdata(inputfile,outputfolder,folds,iterations):
	seed = 1234
	filename=inputfile[0:inputfile.find('.')]
	trainingset = []
	testingset = []
	data_files = dict()
	data=[]
	dataset = arff.load(inputfile)
	for row in dataset:
		data.append(list(row))
	random.seed=seed
	random.shuffle(data)
	len_part=int(math.ceil(len(data)/float(folds)))
	dataset1 = loadarff(open(inputfile,'r'))
	attribute_names = dataset1[1]._attrnames
	count = 0
	for x in range (0,iterations):
		train={}
		test={}
		for i in range(folds):
			count = count+1
			testfile ='test_'+str(count)+'.arff'
			trainfile='train_'+str(count)+'.arff'
			trainingset.append(outputfolder+"/"+trainfile)
			testingset.append(outputfolder+"/"+testfile)
			random.shuffle(data)
		        test[i]  = data[i*len_part:i*len_part+len_part]
			if not os.path.isdir(outputfolder):
				os.makedirs(outputfolder)
			arff.dump(outputfolder+'/'+testfile,test[i],relation="cpu",names=attribute_names)
			train[i] = [j for j in data if j not in test[i]]
			arff.dump(outputfolder+'/'+trainfile,train[i],relation="cpu",names=attribute_names)
	data_files['training'] = trainingset
	data_files['testing'] = testingset
	data_files['k'] = folds
	data_files['r'] = iterations
	data_files['inputFile'] = inputfile
	yaml.dump(data_files,open(outputfolder+'/splitdatafiles.yaml','w'))
	
def main(args):
	inputfile=''
	outputfolder=''
	folds=0
	seed=0
	try:
		opts,args=getopt.getopt(args,"i:o:k:r:",[])
	except getopt.GetoptError:
		print 'datasplit.py -i <inputfile> -o <outputfile> -k <folds> -s <seedvalue>'
		sys.exit(2)
	for opt,arg in opts:
		if opt=='-i':
			inputfile=arg
		elif opt=='-o':
			outputfolder=arg
		elif opt=='-k':
			folds=int(arg)
		elif opt=='-r':
			iterations=int(arg)
	splitdata(inputfile,outputfolder,folds,iterations)
if __name__ == "__main__":
   main(sys.argv[1:])
