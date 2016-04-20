__author__ = 'Pranav Bahl'

import yaml
import sys, getopt
import argparse
import itertools
from pymongo import MongoClient

class WolfJob:

	def __init__(self, args):
		self.client = MongoClient()
		self.db = self.client.WOLF
		self.iter=0
		self.jobs = []
		self.inputfile=args.i
		self.datasplitDir = []
		self.algoResultDir = []
		self.createJobs()

	def createJobs(self):	
		datasplit = yaml.load(open(self.inputfile))['datasplit']
		self.generateCommand(datasplit,'datasplit')
		
		algorithm = yaml.load(open(self.inputfile))['algorithm']
		self.generateCommand(algorithm,'algorithm')
		
		metricCalculation = yaml.load(open(self.inputfile))['metric_calculation']
		self.generateCommand(metricCalculation,'metric_calculation')

		self.writeJobScript()

	def generateCommand(self,component,function):
		splitcmd = 'python ' + component['executable'] + ' -i '
		paramset = dict()
		filesCount = 1
		if (function != 'metric_calculation'):
			list_of_lists = list(map(lambda x: self.getOptionsList(x), component['parameters']))
			option_strings = [list(tup) for tup in itertools.product(*list_of_lists)]
			for option in option_strings:
				params = ''
				for row in option:
					params += ' ' + row[0] + ' '+str(row[1])
					if(function == 'datasplit'):
						if (row[0] not in paramset):
							paramset[row[0]] = set()
						paramset[row[0]].add(row[1])
				if (function == 'datasplit'):
					self.insertSplitParams(params,component['data_file'])
					datasplitFolder = component['output_folder']+'/iter'+str(option_strings.index(option)+1)
					self.datasplitDir.append(datasplitFolder)
					self.jobs.append(splitcmd + component['data_file'] + ' -o ' + ' ' + datasplitFolder  + params)
					self.iter = self.iter + 1
				elif(function == 'algorithm') :
					self.insertAlgoParams(params,component['executable'])
					for i in self.datasplitDir:
						resultFolder = i +'/result'+ str(option_strings.index(option)+1)
						self.algoResultDir.append(resultFolder)
						self.jobs.append(splitcmd + i +'/splitdatafiles.yaml' + ' -o ' + ' ' + resultFolder + params)
			if (function == 'datasplit'):
				for x in paramset:
					filesCount *= max(paramset[x])
				self.insertFiles(filesCount)
		elif(function == 'metric_calculation'):
			for i in self.algoResultDir:
				self.jobs.append(splitcmd + i + '/results.yaml' + ' -o ' + i )
		else:
			print "Wrong input"
		
	def insertSplitParams(self,params,dataFile):
		param = params.replace('-','').split()
		if(0 == self.db.SplitData.find({"file":dataFile,"parameter": {param[0]:param[1],param[2]:param[3]}}).count()):
			objId = int(self.db.seqs.find_and_modify(query={ 'collection' : 'splitdata' },update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True).get('id'))
			self.db.SplitData.insert({"_id":objId,"file":dataFile,"parameter": {param[0]:param[1],param[2]:param[3]}})

	def insertFiles(self,filesCount):
		for count in range(filesCount):
			if(0 == self.db.Files.find({"_id":count+1}).count()):
				print count
				self.db.Files.insert_one({"_id":count+1,"train_file":'train_'+str(count+1)+'.arff',"test_file":'test_'+str(count+1)+'.arff'})

	def insertAlgoParams(self,params,component):
		executable = component[0:component.find('.')]
		param = params.replace('-','').split()
		if(0 == self.db.Algorithm.find({"executable":executable,"parameter": {param[0]:param[1],param[2]:param[3]}}).count()):
			algo_id = int(self.db.seqs.find_and_modify(query={ 'collection' : 'algorithm' },update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True).get('id'))
			self.db.Algorithm.insert({"_id":algo_id,"executable":executable,"parameter": {param[0]:param[1],param[2]:param[3]}})


	def getOptionsList(self,row):

        	if row[0] == 'single':
        	    return [(row[1], row[2])]

        	elif row[0] == 'collection':
			if row[1] == 'list':
				return list(map(lambda opt: (row[2], opt), row[3])) 
			else:
				return list((row[2],a)for a in range(row[3][0],row[3][1],row[3][2] if len(row[3])==3 else 1))

	def writeJobScript(self):
		jobscript = open('submit.sh','w')
		for i in self.jobs:
		        jobscript.write(i+"\n")
		jobscript.close()

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', help='WOLF job configuration file')
	args = parser.parse_args()

	wolf = WolfJob(args)
