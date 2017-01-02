__author__ = 'Kristopher Kaleb Goering'

import os
import arff
import yaml
import sys, getopt
import numpy as np
import pandas as pd
from array import array
from scipy.io.arff import loadarff
from sklearn.qda import QDA
import errno

def quadraticDiscriminantAnalysis(dataFile, outputFolder, regParam,parameters):
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

		qda = QDA(reg_param=regParam)
		qda.fit(train_features, train_labels)
		test_predictions['predictions'] = qda.predict(test_features)
		#testPredictions = np.array(qda.predict(testFeatures)).tolist()
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
	#parameters['parameter.p'] = regParam
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
	resultDict['algorithm'] = "QuadraticDiscriminantAnalysis"
	yaml.dump(resultDict, open(outputFolder + '/results.yaml', 'w'))

def main(args):
	inputFile = ''
	outputFolder = ''
	parameters=dict()
	regParam = 0.0 #float; regularizes the covariance estimate as [(1-reg_param)*Sigma + reg_param*np.eye(n_features)]
	try:
		opts,args = getopt.getopt(args, "i:o:p:", [])
	except getopt.GetoptError:
		print 'QuadraticDiscriminantAnalysis.py -i <inputFile> -o <outputFolder> -p <regParam>'
		sys.exit(2)
	for opt,arg in opts:
		if opt == '-i':
			inputFile = arg
		elif opt == '-o':
			outputFolder = arg
		elif opt == '-p':
			regParam = float(arg)
			parameters['parameter.p']=arg
	quadraticDiscriminantAnalysis(inputFile, outputFolder, regParam,parameters)
if __name__ == "__main__":
   main(sys.argv[1:])

###############################################
#Other parameters
#priors : array, optional, shape (n_classes,)
#Class priors.
