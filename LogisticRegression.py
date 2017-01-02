__author__ = 'Lecheng Zheng,Pranav Bahl'

import os
import arff
import yaml
import sys, getopt
import numpy as np
import pandas as pd
from array import array
from scipy.io.arff import loadarff
from sklearn.linear_model import LogisticRegression
import errno

def LogesticRegression(dataFile,outputfolder,C,Penalty,parameters):
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
		"""testpredictions=[]
		trainlabels=[]
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
			testlabels.append(content[len(content)-1])"""
		train_df = pd.read_csv(trainingSet[i])
		train_labels = train_df[label]
		train_features = train_df.drop(label,axis=1)
		test_df = pd.read_csv(testingSet[i])
		test_predictions = pd.DataFrame(test_df[label])
		test_features = test_df.drop(label,axis=1)

		lr = LogisticRegression(penalty=Penalty,C=C)
		lr.fit(train_features,train_labels)
		test_predictions['predictions'] = lr.predict(test_features)
		#testpredictions=np.array(lr.predict(testfeatures)).tolist()
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
	"""parameters['parameter.c'] = C
	parameters['parameter.p'] = Penalty"""
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
	resultDict['algorithm'] = "LogisticRegression"
	yaml.dump(resultDict,open(outputfolder+'/results.yaml','w'))


def main(args):
	dataFile=''
	outputfolder=''
	parameters=dict()
	C=1.0
	penalty='l2'
	try:
		opts,args=getopt.getopt(args,"i:o:c:p:",[])
	except getopt.GetoptError:
		print 'datasplit.py -i <inputfile> -o <outputfolder> -c <regularization> -p <penalty>'
		sys.exit(2)
	for opt,arg in opts:
		if opt=='-i':
			dataFile=arg
		elif opt=='-o':
			outputfolder=arg
		elif opt=='-c':
			C=float(arg)
			parameters['parameter.c']=arg
		elif opt=='-p':
			penalty=args
			parameters['parameter.p']=arg
	LogesticRegression(dataFile,outputfolder,C,penalty,parameters)

if __name__ == "__main__":
   main(sys.argv[1:])
