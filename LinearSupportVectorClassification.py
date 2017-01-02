__author__ = 'Kristopher Kaleb Goering, Pranav Bahl'

import os
import arff
import yaml
import sys, getopt
import numpy as np
import pandas as pd
from array import array
from scipy.io.arff import loadarff
from sklearn.svm import LinearSVC
import errno

def linearSupportVectorClassification(dataFile, outputFolder, c, lossType, penaltyType, isDual, tolerance, multiClass, isFit, interceptScaling, classWeight, isVerbose, maxIter, randomState,parameters):
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

		svm = LinearSVC(C=c, loss=lossType,  penalty=penaltyType, dual=isDual, tol=tolerance, multi_class=multiClass, fit_intercept=isFit, intercept_scaling=interceptScaling, class_weight=classWeight, verbose=isVerbose, max_iter=maxIter, random_state=randomState)
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
	"""parameters['parameter.c'] = c
	parameters['parameter.l'] = lossType
	parameters['parameter.p'] = penaltyType
	parameters['parameter.d'] = isDual
	parameters['parameter.t'] = tolerance
	parameters['parameter.m'] = multiClass
	parameters['parameter.f'] = isFit
	parameters['parameter.s'] = interceptScaling
	parameters['parameter.w'] = classWeight
	parameters['parameter.v'] = isVerbose
	parameters['parameter.i'] = maxIter
	parameters['parameter.r'] = randomState"""
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
	resultDict['algorithm'] = "LinearSupportVectorClassification"
	yaml.dump(resultDict, open(outputFolder + '/results.yaml', 'w'))

def main(args):
	inputFile = ''
	outputFolder = ''
	parameters=dict()
	c = 1.0 #float;
	lossType = 'squared_hinge' #string; default = 'squared_hinge', 'hinge' is default for SVC class
	penaltyType = 'l2' #string; default = 'l2', 'l1'
	isDual = True #boolean
	tolerance = 0.001 #float;
	multiClass = 'ovr' #string; default = 'ovr', 'crammer_singer'
	isFit = True #boolean;
	interceptScaling = 1 #float;
	classWeight = None # {dict, 'balanced'}
	isVerbose = 0 #int;
	maxIter = 1000 #int; -1 for no limit
	randomState = None #int, RandomState instance or None

	try:
		opts,args = getopt.getopt(args, "i:o:c:l:p:d:t:m:f:s:w:v:x:r:", [])
	except getopt.GetoptError:
		print 'LinearSupportVectorClassification.py -i <inputFile> -o <outputFolder> -c <c> -l <lossType> -p <penaltyType> -d <isDual> -t <tolerance> -m <multiClass> -f <isFit> -s <interceptScaling> -w <classWeight> -v <isVerbose> - <maxIter> -r <randomState>'
		sys.exit(2)
	for opt,arg in opts:
		if opt == '-i':
			inputFile = arg
		elif opt == '-o':
			outputFolder = arg
		elif opt == '-c':
			c = float(arg)
			parameters['parameter.c']=arg
		elif opt == '-l':
			lossType = arg
			parameters['parameter.l']=arg
		elif opt == '-p':
			penaltyType = arg
			parameters['parameter.p']=arg
		elif opt == '-d':
			if arg == "True":
				isDual = True
			elif arg == "False":
				isDual = False
			else:
				raise ValueError
			parameters['parameter.d']=arg
		elif opt == '-t':
			tolerance = float(arg)
			parameters['parameter.t']=arg
		elif opt == '-m':
			multiClass = arg
			parameters['parameter.m']=arg
		elif opt == '-f':
			if arg == "True":
				isFit = True
			elif arg == "False":
				isFit = False
			else:
				raise ValueError
			parameters['parameter.f']=arg
		elif opt == '-s':
			interceptScaling = float(arg)
			parameters['parameter.s']=arg
		elif opt == '-w':
			classWeight = dict(arg)
			parameters['parameter.w']=arg
		elif opt == '-v':
			isVerbose = int(arg)
			parameters['parameter.v']=arg
		elif opt == '-x':
			maxIter = int(arg)
			parameters['parameter.x']=arg
		elif opt == '-r':
			if arg != None:
				randomState = int(arg)
			parameters['parameter.r']=arg
	linearSupportVectorClassification(inputFile, outputFolder, c, lossType, penaltyType, isDual, tolerance, multiClass, isFit, interceptScaling, classWeight, isVerbose, maxIter, randomState,parameters)
if __name__ == "__main__":
   main(sys.argv[1:])
