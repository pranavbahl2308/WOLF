__author__ = "Pranav Bahl"

from pymongo import MongoClient
import argparse
import csv
import os
import numpy as np
import pandas as pd
from cStringIO import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import errno


class DatabaseResults:

	def __init__(self,args):
		#self.uri = "mongodb://wolfAdmin:wo20lf@db2.acf.ku.edu/wolf"
		self.uri = "mongodb://wolfAdmin:wo20lf@db2.local/wolf"
		self.client = MongoClient(self.uri)
		self.db = self.client.wolf
		self.sd_file_name = args.i
		self.processResult()

	def processResult(self):
		sd_ids=[]
		for sd_id in self.db.SplitData.find({"file":self.sd_file_name},{"_id":1}):
			sd_ids.append(sd_id['_id'])
		results = self.db.Result.aggregate([{'$match':{'sd_id':{'$in':sd_ids}}},{'$group': {'_id' : {'algo_id' : "$algo_id"},'recall' : {'$avg' : "$recall"}, 'precision' : {'$avg' : "$precision"}, 'accuracy' : {'$avg' : "$accuracy"},'f1_score':{'$avg' : "$f1_score"},'mcc':{'$avg' :"$mcc"},'roc_auc':{'$avg' :"$roc_auc"},'std':{'$avg' :"$standard_deviation"} }}])
		with open(str(os.getcwd()+'/Results.xlsx'), 'w') as csvfile:
			fieldnames = ['algo_config', 'precision','recall','accuracy','f1_score','mcc','roc_auc']
			algo_configs = []
			recall = []
			precision = []
			accuracy = []
			f1_score = []
			algo_names = []
			algo_params = []
			mcc = []
			roc_auc = []
			for result in results:
				recall.append(result['recall'])
				precision.append(result['precision'])
				accuracy.append(result['accuracy'])
				f1_score.append(result['f1_score'])
				mcc.append(result['mcc'])
				roc_auc.append(result['roc_auc'])
				algo_param = ""
				algo_name = ""
				for algo_config in self.db.Algorithm.find({"_id":result['_id']['algo_id']}):
					algo_param = algo_config['parameter']
					algo_name = algo_config['executable']
				algo_names.append(algo_name)
				algo_params.append(algo_param)
				algo_configs.append('Algorithm:'+str(algo_name)+" \n "+' parameter:'+str(algo_param))
			recall.append(np.std(recall))
			precision.append(np.std(precision))
			accuracy.append(np.std(accuracy))
			algo_configs.append('std')
			algo_names.append('std')
			algo_params.append('')
			f1_score.append(np.std(f1_score))
			mcc.append(np.std(mcc))
			roc_auc.append(np.std(roc_auc))
			data = pd.DataFrame({'algo_config':algo_configs,'algo_name':algo_names,'algo_param':algo_params,'precision':precision,'recall':recall,'accuracy':accuracy,'f1_score':f1_score,'mcc':mcc,'roc_auc':roc_auc})
			writer = pd.ExcelWriter(str(os.getcwd()+'/Results.xlsx'), engine='xlsxwriter')
			idx = data.groupby(['algo_name'])['roc_auc'].transform(max) == data['roc_auc']
			plot_df = data[idx].drop('algo_config',axis=1).reset_index(drop=True)
			plot_df.to_excel(writer,sheet_name="Results")
			for algo in data['algo_name'].unique():
				if algo != 'std':
					data[data['algo_name'] == algo].drop('algo_config',axis=1).to_excel(writer,sheet_name=algo[:31])
			data[data['roc_auc'] == max(data['roc_auc'])].drop('algo_config',axis=1).to_excel(writer,sheet_name="Best_configuration")
			cols = [col for col in data.columns if col not in ['algo_config']]
			workbook  = writer.book
			worksheet = writer.sheets['Results']
			observations = len(data)
			count = 0
			for i in plot_df.columns:
				if i not in ['algo_config','algo_name','algo_param']:
					imgdata = StringIO()
					fig,ax = plt.subplots()
					plot_df[plot_df['algo_name'] != 'std'][i].plot.bar(ax=ax)
					ax.set_xticklabels(plot_df[plot_df['algo_name'] != 'std'].index,rotation = 0)
					ax.set_xlabel(i)
					ax.set_ylabel("score")
					fig.savefig(imgdata)
					worksheet.insert_image(observations+5+(35*count),1,"",{'image_data':imgdata})
					count += 1
			"""for i in range(observations-1):
				imgdata = StringIO()
				fig,ax = plt.subplots(figsize=(7,3))
				data[i:i+1][cols].plot.bar(ax=ax)
				ax.set_xticklabels(data[i:i+1]['algo_config'],rotation = 0)
				fig.savefig(imgdata)
				worksheet.insert_image(observations+3+(15*i),1,"",{'image_data':imgdata})"""
			writer.save()
			writer.close()

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', help='Splitdata filename')
	args = parser.parse_args()

	dbRes = DatabaseResults(args)
