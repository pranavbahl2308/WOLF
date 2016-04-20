__author__ = 'Pranav Bahl'

from sklearn.metrics import roc_auc_score,recall_score, precision_score, f1_score, accuracy_score, confusion_matrix
import yaml
import os
import yaml
import sys, getopt
from pymongo import MongoClient

def metricCalculation(inputfile,outfile):
	client = MongoClient()
	db = client.WOLF
	resultsfile = yaml.load(open(inputfile))['results']
	#dataFile = yaml.load(open(inputfile))['inputFile']
	#k = 
	#test = "file:"++",parameter:{k:"+str(yaml.load(open(inputfile))['k'])+",r:"+str(yaml.load(open(inputfile))['r'])
	#print test
	sd_id=0
	algo_id = 0
	print yaml.load(open(inputfile))['algorithm']
	print str(yaml.load(open(inputfile))['t'])
	print str(yaml.load(open(inputfile))['d'])
	for s in  db.SplitData.find({"file":yaml.load(open(inputfile))['inputFile'],"parameter": {"k":str(yaml.load(open(inputfile))['k']),"r":str(yaml.load(open(inputfile))['r'])}},{"_id":1}):
		sd_id = s['_id']
	for r in db.Algorithm.find({"executable":yaml.load(open(inputfile))['algorithm'],"parameter": {"d":str(yaml.load(open(inputfile))['d']),"t":str(yaml.load(open(inputfile))['t'])}},{"_id":1}):
		algo_id = r['_id']
	for r,i in zip(resultsfile,range(len(resultsfile))):
		predictions=yaml.load(open(r,'r'))['predictions']
		true_labels=yaml.load(open(r,'r'))['true_labels']
		accuracy=float(accuracy_score(true_labels,predictions))
		precision = float(precision_score(true_labels,predictions))
		recall = float(recall_score(true_labels,predictions))
		f1_Score = float(f1_score(true_labels,predictions))
		try:
			roc_auc = float(roc_auc_score(true_labels,predictions))
		except ValueError:
			roc_auc = 0.0
		#conf_mat = confusion_matrix(true_labels, predictions)
		objId = int(db.seqs.find_and_modify(query={ 'collection' : 'result' },update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True).get('id'))
		db.Result.insert({"_id":objId,"sd_id":sd_id,"file_id":i+1,"algo_id":algo_id,"accuracy":accuracy,"precision":precision,"recall":recall,"f1_score":f1_Score,"roc_auc":roc_auc})
		metric_calc = dict()
		metric_calc['accuracy'] = accuracy
		metric_calc['precision'] = precision
		metric_calc['recall'] = recall
		metric_calc['f1_Score'] = f1_Score
		metric_calc['roc_auc'] = roc_auc
		yaml.dump(metric_calc,open(outfile+'/metric'+str(i+1)+'.yaml','w'))


def main(args):
	inputfile=''
	outputfolder=''
	numberOfTrees=0
	try:
		opts,args=getopt.getopt(args,"i:t:o:k:",[])
	except getopt.GetoptError:
		print 'MetricCollection.py -i <inputfile> -o <outputfolder>'
		sys.exit(2)
	for opt,arg in opts:
		if opt=='-i':
			inputfile=arg
		elif opt=='-o':
			outputfolder=arg
	metricCalculation(inputfile,outputfolder)

if __name__ == "__main__":
   main(sys.argv[1:])
