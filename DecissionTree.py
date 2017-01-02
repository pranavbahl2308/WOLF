__author__ = 'Lecheng Zheng,Pranav Bahl'

import os
import arff
import yaml
import sys, getopt
import numpy as np
import pandas as pd
from array import array
from scipy.io.arff import loadarff
from sklearn import trees
import errno

def DecissionTree(dataFile,outputfolder,criterion,max_features,max_depth,min_samples_split,min_samples_leaf,min_weight_fraction_leaf,max_leaf_nodes,presort,parameters):
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

        dt = tree.DecisionTreeClassifier(criterion=criterion,max_features=max_features,max_depth=max_depth,min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf,min_weight_fraction_leaf=min_weight_fraction_leaf,max_leaf_nodes=max_leaf_nodes,presort=presort,class_weight='balanced')
        dt.fit(train_features,train_labels)
        test_predictions['predictions'] = dt.predict(test_features)
        #testpredictions=np.array(dt.predict(testfeatures)).tolist()
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
    """parameters['parameter.c'] = criterion
    parameters['parameter.f'] = max_features
    parameters['parameter.d'] = max_depth
    parameters['parameter.s'] = min_samples_split
    parameters['parameter.l'] = min_samples_leaf
    parameters['parameter.w'] = min_weight_fraction_leaf
    parameters['parameter.n'] = max_leaf_nodes
    parameters['parameter.p'] = presort"""
    if not parameters:
        parameters['parameter']='default'
    resultDict['algo_params'] = parameters
    resultDict['inputFile'] = inputFile
    resultDict['algorithm'] = "DecissionTree"
    resultDict['split_params'] = inputData['split_params']
    if 'feature_selection_parameters' in inputData:
        resultDict['feature_selection_parameters'] = inputData['feature_selection_parameters']
        resultDict['feature_selection_algorithm'] = inputData['feature_selection_algorithm']
    if 'feature_extraction_parameters' in inputData:
        resultDict['feature_extraction_parameters'] = inputData['feature_extraction_parameters']
        resultDict['feature_extraction_algorithm'] = inputData['feature_extraction_algorithm']
    if 'preprocessing_params' in inputData:
		resultDict['preprocessing_params'] = inputData['preprocessing_params']
    yaml.dump(resultDict,open(outputfolder+'/results.yaml','w'))


def main(args):
    dataFile=''
    outputfolder=''
    parameters=dict()
    criterion = 'gini'
    max_features = 'auto'
    max_depth = None
    min_samples_split=2
    min_samples_leaf=1
    min_weight_fraction_leaf=0.
    max_leaf_nodes=None
    presort=False
    try:
        opts,args=getopt.getopt(args,"i:o:c:f:",[])
    except getopt.GetoptError:
        print 'datasplit.py -i <inputfile> -o <outputfolder> -c <criterion> -f <max_features> -d <max_depth> -s <min_samples_split> -l <min_samples_leaf> -w <min_weight_fraction_leaf> -n <max_leaf_nodes> -p <presort>'
        print 'option for criterion: gini or entropy'
        print 'option for max_features: auto, sqrt, log2'
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-i':
            dataFile=arg
        elif opt=='-o':
            outputfolder=arg
        elif opt=='-c':
            criterion=arg
            parameters['parameter.c']=arg
        elif opt=='-f':
            if arg != None:
                try:
                    max_features=int(arg)
                except:
                    try:
                        max_features=float(arg)
                    except:
                        max_features = arg
            parameters['parameter.f']=arg
        elif opt=='-d':
            if arg != None:
                max_depth=int(arg)
            parameters['parameter.d']=arg
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
        elif opt=='-w':
            min_weight_fraction_leaf=float(arg)
            parameters['parameter.w']=arg
        elif opt=='-n':
            if arg != None:
                max_leaf_nodes=int(arg)
            parameters['parameter.n']=arg
        elif opt=='-p':
            if arg == 'True':
                presort = True
            elif arg == 'False':
                presort = False
            else:
            	raise ValueError
    		parameters['parameter.p']=arg
    DecissionTree(dataFile,outputfolder,criterion,max_features,max_depth,min_samples_split,min_samples_leaf,min_weight_fraction_leaf,max_leaf_nodes,presort,parameters)
if __name__ == "__main__":
   main(sys.argv[1:])
