__author__ = 'Pranav Bahl'

import os
import arff
import yaml
import sys, getopt
import numpy as np
import pandas as pd
from scipy.io.arff import loadarff
from sklearn.ensemble import RandomForestClassifier
import errno

def randomForest(dataFile,outputfolder,numberOfTrees,depth,criterion,min_samples_split,min_samples_leaf,min_weight_fraction_leaf,max_leaf_nodes,min_impurity_split,warm_start,parameters):
	inputData = yaml.load(open(dataFile))
	trainingSet = inputData['training']
	testingSet = inputData['testing']
	inputFile = inputData['inputFile']
	label = inputData['label']
	resultset = []
	if not os.path.exists(outputfolder):
		try:
			os.makedirs(outputfolder)
		except OSError as exc:
		    if exc.errno != errno.EEXIST:
		        raise exc
		    pass
	for i in range(len(trainingSet)):
		"""trainlabels=[]
		trainfeatures=[]
		traindataset = arff.load(trainingSet[i])
		for row in traindataset:
			content = list(row)
			trainfeatures.append(content[0:len(content)-1])
			trainlabels.append(content[len(content)-1])
		testfeatures=[]
		testlabels=[]
		testdataset = arff.load(testingSet[i])
		for row in testdataset:
			content = list(row)
			testfeatures.append(content[0:len(content)-1])
			testlabels.append(content[len(content)-1])
		"""
		train_df = pd.read_csv(trainingSet[i])
		train_labels = train_df[label]
		train_features = train_df.drop(label,axis=1)
		test_df = pd.read_csv(testingSet[i])
		test_predictions = pd.DataFrame(test_df[label])
		test_features = test_df.drop(label,axis=1)

		rf = RandomForestClassifier(n_estimators=numberOfTrees,max_depth=depth,n_jobs=-1, criterion=criterion, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_leaf_nodes=max_leaf_nodes, warm_start=warm_start)
		rf.fit(train_features,train_labels)
		test_predictions['predictions'] = rf.predict(test_features)
		resultFile = outputfolder+'/result'+str(i+1)+'.csv'
		"""with open(resultFile,'w') as outfile:
			outfile.write('predictions:\n')
			outfile.write(yaml.dump(testpredictions,default_flow_style=False))
			outfile.write('true_labels:\n')
			outfile.write(yaml.dump(testlabels,default_flow_style=False))"""
		test_predictions.to_csv(resultFile,index=False)
		resultset.append(resultFile)
	resultDict = dict()
	#parameters = dict()
	resultDict['results'] = resultset
	resultDict['label'] = label
	"""parameters['parameter.t'] = str(numberOfTrees)
	parameters['parameter.d'] = str(depth)"""
	if not parameters:
		parameters['parameter']='default'
	resultDict['algo_params'] = parameters
	resultDict['split_params'] = inputData['split_params']
	if 'feature_selection_parameters' in inputData:
	        resultDict['feature_selection_parameters'] = inputData['feature_selection_parameters']
	        resultDict['feature_selection_algorithm'] = inputData['feature_selection_algorithm']
	if 'feature_extraction_parameters' in inputData:
	        resultDict['feature_extraction_parameters'] = inputData['feature_extraction_parameters']
	        resultDict['feature_extraction_algorithm'] = inputData['feature_extraction_algorithm']
	if 'preprocessing_params' in inputData:
		resultDict['preprocessing_params'] = inputData['preprocessing_params']
	resultDict['inputFile'] = inputFile
	resultDict['algorithm'] = "RandomForest"
	yaml.dump(resultDict,open(outputfolder+'/results.yaml','w'))


def main(args):
	dataFile=''
	outputfolder=''
	parameters=dict()
	numberOfTrees=10
	depth = None
	criterion = "gini"
	min_samples_split = 2
	min_samples_leaf = 1
	min_weight_fraction_leaf = 0.0
	max_leaf_nodes = None
	min_impurity_split = 0.0000001
	warm_start = False
	try:
		opts,args=getopt.getopt(args,"i:t:o:d:",[])
	except getopt.GetoptError:
		print 'datasplit.py -i <inputfile> -o <outputfolder> -t <numberOfTrees> -d<max_depth_of_trees> -c<criterion> -s<min_samples_split> -l<min_samples_leaf> -m<min_weight_fraction_leaf> -n<max_leaf_nodes> -p<min_impurity_split> -w<warm_start>'
		sys.exit(2)
	for opt,arg in opts:
		if opt=='-i':
			dataFile=arg
		elif opt=='-o':
			outputfolder=arg
		elif opt=='-t':
			numberOfTrees=int(arg)
			parameters['parameter.t']=arg
		elif opt=='-d':
			depth=int(arg)
			parameters['parameter.d']=arg
		elif opt=='-c':
			criterion=arg
			parameters['parameter.c']=arg
		elif opt=='-s':
			try:
				min_samples_split=int(arg)
			except:
				min_samples_split=float(arg)
			parameters['parameter.s']=arg
		elif opt=='-l':
			try:
				min_samples_leaf=int(arg)
			except:
				min_samples_leaf=float(arg)
			parameters['parameter.l']=arg
		elif opt=='-m':
			min_weight_fraction_leaf=float(arg)
			parameters['parameter.m']=arg
		elif opt=='-n':
			if arg != None:
				max_leaf_nodes=int(arg)
			parameters['parameter.n']=arg
		elif opt=='-p':
			min_impurity_split = float(arg)
			parameters['parameter.p']=arg
		elif opt=='-w':
			if arg == 'True':
				warm_start = True
			elif arg=='False':
				warm_start = False
			else:
				raise ValueError
			parameters['parameter.w']=arg
	randomForest(dataFile,outputfolder,numberOfTrees,depth,criterion,min_samples_split,min_samples_leaf,min_weight_fraction_leaf,max_leaf_nodes,min_impurity_split,warm_start,parameters)
if __name__ == "__main__":
   main(sys.argv[1:])
