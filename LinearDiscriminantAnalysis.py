__author__ = 'Kristopher Kaleb Goering,Pranav_Bahl'

import os
import arff
import yaml
import sys, getopt
import numpy as np
import pandas as pd
from array import array
from scipy.io.arff import loadarff
from sklearn.lda import LDA
import errno

def linearDiscriminantAnalysis(dataFile, outputFolder, solverType, shrinkageValue, numOfComponents, tolerance,parameters):
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

		lda = LDA(solver=solverType, shrinkage=shrinkageValue, n_components=numOfComponents, tol=tolerance)
		lda.fit(train_features, train_labels)
		test_predictions['predictions'] = lda.predict(test_features)
		#testPredictions = np.array(lda.predict(testFeatures)).tolist()
		resultFile = outputFolder + '/result' + str(i + 1) + '.csv'
		"""with open(resultFile,'w') as outfile:
			outfile.write('predictions:\n')
			outfile.write(yaml.dump(testPredictions, default_flow_style=False))
			outfile.write('true_labels:\n')
			outfile.write(yaml.dump(testLabels, default_flow_style=False))"""
		test_predictions.to_csv(resultFile,index=False)
		resultSet.append(resultFile)
	resultDict = dict()
	resultDict['results'] = resultSet
	resultDict['label'] = label
	"""parameters = dict()
	parameters['parameter.s'] = solverType
	parameters['parameter.v'] = shrinkageValue
	parameters['parameter.n'] = numOfComponents
	parameters['parameter.t'] = tolerance"""
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
	resultDict['algorithm'] = "LinearDiscriminantAnalysis"
	yaml.dump(resultDict, open(outputFolder + '/results.yaml', 'w'))

def main(args):
	inputFile = ''
	outputFolder = ''
	parameters=dict()
	solverType = 'svd' #string; default = 'svd', 'lsqr', 'eigen'
	shrinkageValue = None #string or float; 'auto', 0-1, or None; only works with lsqr or eigen solvers
	numOfComponents = None #int; n < n_classes - 1
	tolerance = 0.0001 #float; threshold for rank estim in SVD solver
	try:
		opts,args = getopt.getopt(args, "i:o:s:v:n:t:", [])
	except getopt.GetoptError:
		print 'LinearDiscriminantAnalysis.py -i <inputFile> -o <outputFolder> -s <solverType> -v <shrinkageValue> -n <numOfComponents> -t <tolerance>'
		sys.exit(2)
	for opt,arg in opts:
		if opt == '-i':
			inputFile = arg
		elif opt == '-o':
			outputFolder = arg
		elif opt == '-s':
			solverType = arg
			parameters['parameter.s']=arg
		elif opt == '-v':
			try:
				shrinkageValue = float(arg)
			except:
				shrinkageValue = arg
			parameters['parameter.v']=arg
		elif opt == '-n':
			numOfComponents = int(arg)
			parameters['parameter.n']=arg
		elif opt == '-t':
			tolerance = float(arg)
			parameters['parameter.t']=arg
	if solverType == 'svd':
		shrinkageValue = None
	else:
		tolerance = None
	linearDiscriminantAnalysis(inputFile, outputFolder, solverType, shrinkageValue, numOfComponents, tolerance,parameters)
if __name__ == "__main__":
   main(sys.argv[1:])

###############################################
#Other parameters
#priors : array, optional, shape (n_classes,)
#Class priors.
