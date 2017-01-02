__author__ = 'Kristopher Kaleb Goering, Pranav Bahl'

import os
import arff
import yaml
import sys, getopt
import numpy as np
import pandas as pd
from array import array
from scipy.io.arff import loadarff
from sklearn.svm import SVC
import errno

def cSupportVectorClassification(dataFile, outputFolder, c, kernelType, numDegree, numGamma, coef, isShrink, isProb, tolerance, cacheSize, classWeight, isVerbose, maxIter, decisionShape, randomState,parameters):
	inputData = yaml.load(open(dataFile))
	trainingSet = inputData['training']
	testingSet = inputData['testing']
	inputFile = inputData['inputFile']
	label = inputData['label']
	resultSet = []
	if not os.path.exists(outputFolder):
		try:
			os.makedirs(outputFolder)
		except OSError as exc:
		    if exc.errno != errno.EEXIST:
		        raise exc
		    pass
	for i in range(len(trainingSet)):
		"""testPredictions = []
		trainLabels = []
		trainFeatures = []
		trainDataSet = arff.load(trainingSet[i])
		for row in trainDataSet:
			content = list(row)
			trainFeatures.append(content[0:len(content)-1])
			trainLabels.append(content[len(content)-1])
		testFeatures = []
		testLabels = []
		testDataSet = arff.load(testingSet[i])
		for row in testDataSet:
			content = list(row)
			testFeatures.append(content[0:len(content)-1])
			testLabels.append(content[len(content)-1])"""
		train_df = pd.read_csv(trainingSet[i])
		train_labels = train_df[label]
		train_features = train_df.drop(label,axis=1)
		test_df = pd.read_csv(testingSet[i])
		test_predictions = pd.DataFrame(test_df[label])
		test_features = test_df.drop(label,axis=1)

		svm = SVC(C=c, kernel=kernelType, degree=numDegree, gamma=numGamma, coef0=coef, shrinking=isShrink, probability=isProb, tol=tolerance, cache_size=cacheSize, class_weight=classWeight, verbose=isVerbose, max_iter=maxIter, decision_function_shape=decisionShape, random_state=randomState)
		svm.fit(train_features, train_labels)
		test_predictions['predictions'] = svm.predict(test_features)
		#testPredictions = np.array(svm.predict(testFeatures)).tolist()
		resultFile = outputFolder + '/result' + str(i + 1) + '.csv'
		"""with open(resultFile,'w') as outfile:
			outfile.write('predictions:\n')
			outfile.write(yaml.dump(testPredictions, default_flow_style=False))
			outfile.write('true_labels:\n')
			outfile.write(yaml.dump(testLabels, default_flow_style=False))"""
		test_predictions.to_csv(resultFile,index=False)
		resultSet.append(resultFile)
	resultDict = dict()
	#parameters = dict()
	resultDict['results'] = resultSet
	resultDict['label'] = label
	"""parameters['parameter.c'] = str(c)
	parameters['parameter.k'] = str(kernelType)
	parameters['parameter.d'] = str(numDegree)
	parameters['parameter.g'] = str(numGamma)
	parameters['parameter.f'] = str(coef)
	parameters['parameter.s'] = str(isShrink)
	parameters['parameter.p'] = str(isProb)
	parameters['parameter.t'] = str(tolerance)
	parameters['parameter.a'] = str(cacheSize)
	parameters['parameter.w'] = str(classWeight)
	parameters['parameter.v'] = str(isVerbose)
	parameters['parameter.i'] = str(maxIter)
	parameters['parameter.e'] = str(decisionShape)
	parameters['parameter.r'] = str(randomState)"""
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
	resultDict['algorithm'] = "CSupportVectorClassification"
	yaml.dump(resultDict, open(outputFolder + '/results.yaml', 'w'))

def main(args):
	inputFile = ''
	outputFolder = ''
	parameters=dict()
	c = 1.0 #float;
	kernelType = 'rbf' #string; default = 'rbf', 'linear', 'poly', 'sigmoid', 'precomputed', callable; if callable, data must be [n,n]
	numDegree = 3 #int; only for poly, ignored by others
	numGamma = 'auto' #float; for rbf, poly, sigmoid; if auto, 1/n_features
	coef = 0.0 #float; only significant in poly or sigmoid
	isShrink = True #boolean;
	isProb = False #boolean;
	tolerance = 0.001 #float;
	cacheSize = 200 #float; in MB
	classWeight = None # {dict, 'balanced'}
	isVerbose = False #boolean
	maxIter = -1 #int; -1 for no limit
	decisionShape = None #string; 'ovo', 'ovr', or None
	randomState = None #int, RandomState instance or None

	try:
		opts,args = getopt.getopt(args, "i:o:c:k:d:g:f:s:p:t:a:w:v:m:e:r:", [])
	except getopt.GetoptError:
		print 'cSupportVectorClassification.py -i <inputFile> -o <outputFolder> -c <c> -k <kernelType> -d <numDegree> -g <numGamma> -f <coef> -s <isShrink> -p <isProb> -t <tolerance> -a <cacheSize> -w <classWeight> -v <isVerbose> -m <maxIter> -e <decisionFunctionShape> -r <randomState>'
		sys.exit(2)
	for opt,arg in opts:
		if opt == '-i':
			inputFile = arg
		elif opt == '-o':
			outputFolder = arg
		elif opt == '-c':
			c = float(arg)
			parameters['parameter.c']=arg
		elif opt == '-k':
			kernelType = arg
			parameters['parameter.k']=arg
		elif opt == '-d':
			numDegree = int(arg)
			parameters['parameter.d']=arg
		elif opt == '-g':
			try:
				numGamma = float(arg)
			except:
				numGamma = arg
			parameters['parameter.g']=arg
		elif opt == '-f':
			coef = float(arg)
			parameters['parameter.f']=arg
		elif opt == '-s':
			if arg == "True":
				isShrink = True
			elif arg == "False":
				isShrink = False
			else:
				raise ValueError
			parameters['parameter.s']=arg
		elif opt == '-p':
			if arg == "True":
				isProb = True
			elif arg == "False":
				isProb = False
			else:
				raise ValueError
			parameters['parameter.p']=arg
		elif opt == '-t':
			tolerance = float(arg)
			parameters['parameter.t']=arg
		elif opt == '-a':
			cacheSize = float(arg)
			parameters['parameter.a']=arg
		elif opt == '-w':
			classWeight = dict(arg)
			parameters['parameter.w']=arg
		elif opt == '-v':
			if arg == "True":
				isVerbose = True
			elif arg == "False":
				isVerbose = False
			else:
				raise ValueError
			parameters['parameter.v']=arg
		elif opt == '-m':
			maxIter = int(arg)
			parameters['parameter.m']=arg
		elif opt == '-e':
			decisionShape = arg
			parameters['parameter.e']=arg
		elif opt == '-r':
			randomState = int(arg)
			parameters['parameter.r']=arg
	cSupportVectorClassification(inputFile, outputFolder, c, kernelType, numDegree, numGamma, coef, isShrink, isProb, tolerance, cacheSize, classWeight, isVerbose, maxIter, decisionShape, randomState,parameters)
if __name__ == "__main__":
   main(sys.argv[1:])
