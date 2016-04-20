__author__ = 'Pranav Bahl'

import os
import arff
import yaml
import sys, getopt
import numpy as np
from array import array
from scipy.io.arff import loadarff
from sklearn.ensemble import RandomForestClassifier

def randomForest(datafile,outputfolder,numberOfTrees,depth):
	trainingset = yaml.load(open(datafile))['training']
	testingset = yaml.load(open(datafile))['testing']
	k = yaml.load(open(datafile))['k']
	r = yaml.load(open(datafile))['r']
	inputFile = yaml.load(open(datafile))['inputFile']
	resultset = []
	if not os.path.isdir(outputfolder):
				os.makedirs(outputfolder)	
	for i in range(len(trainingset)):
		testpredictions=[]
		trainlabels=[]
		trainfeatures=[]
		traindataset = arff.load(trainingset[i])
		for row in traindataset:
			content = list(row)
			trainfeatures.append(content[0:len(content)-1])
			trainlabels.append(content[len(content)-1])
		testfeatures=[]
		testlabels=[]
		testdataset = arff.load(testingset[i])
		for row in testdataset:
			content = list(row)
			testfeatures.append(content[0:len(content)-1])
			testlabels.append(content[len(content)-1])
		rf = RandomForestClassifier(n_estimators=numberOfTrees,max_depth=depth,n_jobs=-1)
		rf.fit(trainfeatures,trainlabels)
		testpredictions=np.array(rf.predict(testfeatures)).tolist()
		resultfile = outputfolder+'/result'+str(i+1)+'.yaml'
		with open(resultfile,'w') as outfile:
			outfile.write('predictions:\n')
			outfile.write(yaml.dump(testpredictions,default_flow_style=False))
			outfile.write('true_labels:\n')
			outfile.write(yaml.dump(testlabels,default_flow_style=False))
		resultset.append(resultfile)
	resultdict = dict()
	resultdict['results'] = resultset
	resultdict['k'] = k
	resultdict['r'] = r
	resultdict['t'] = numberOfTrees
	resultdict['d'] = depth
	resultdict['inputFile'] = inputFile
	resultdict['algorithm'] = "RandomForest"
	yaml.dump(resultdict,open(outputfolder+'/results.yaml','w'))
	

def main(args):
	datafile=''
	outputfolder=''
	numberOfTrees=0
	try:
		opts,args=getopt.getopt(args,"i:t:o:d:",[])
	except getopt.GetoptError:
		print 'datasplit.py -i <inputfile> -o <outputfolder> -k <numberOfTrees>'
		sys.exit(2)
	for opt,arg in opts:
		if opt=='-i':
			datafile=arg
		elif opt=='-o':
			outputfolder=arg
		elif opt=='-t':
			numberOfTrees=int(arg)
		elif opt=='-d':
			depth=int(arg)
	randomForest(datafile,outputfolder,numberOfTrees,depth)
if __name__ == "__main__":
   main(sys.argv[1:])
