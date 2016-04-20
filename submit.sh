python Splitingdata.py -i cpu.arff -o  output/iter1 -k 3 -r 10
python Splitingdata.py -i cpu.arff -o  output/iter2 -k 3 -r 15
python Splitingdata.py -i cpu.arff -o  output/iter3 -k 3 -r 20
python Splitingdata.py -i cpu.arff -o  output/iter4 -k 5 -r 10
python Splitingdata.py -i cpu.arff -o  output/iter5 -k 5 -r 15
python Splitingdata.py -i cpu.arff -o  output/iter6 -k 5 -r 20
python RandomForest.py -i output/iter1/splitdatafiles.yaml -o  output/iter1/result1 -d 2 -t 100
python RandomForest.py -i output/iter2/splitdatafiles.yaml -o  output/iter2/result1 -d 2 -t 100
python RandomForest.py -i output/iter3/splitdatafiles.yaml -o  output/iter3/result1 -d 2 -t 100
python RandomForest.py -i output/iter4/splitdatafiles.yaml -o  output/iter4/result1 -d 2 -t 100
python RandomForest.py -i output/iter5/splitdatafiles.yaml -o  output/iter5/result1 -d 2 -t 100
python RandomForest.py -i output/iter6/splitdatafiles.yaml -o  output/iter6/result1 -d 2 -t 100
python RandomForest.py -i output/iter1/splitdatafiles.yaml -o  output/iter1/result2 -d 2 -t 150
python RandomForest.py -i output/iter2/splitdatafiles.yaml -o  output/iter2/result2 -d 2 -t 150
python RandomForest.py -i output/iter3/splitdatafiles.yaml -o  output/iter3/result2 -d 2 -t 150
python RandomForest.py -i output/iter4/splitdatafiles.yaml -o  output/iter4/result2 -d 2 -t 150
python RandomForest.py -i output/iter5/splitdatafiles.yaml -o  output/iter5/result2 -d 2 -t 150
python RandomForest.py -i output/iter6/splitdatafiles.yaml -o  output/iter6/result2 -d 2 -t 150
python RandomForest.py -i output/iter1/splitdatafiles.yaml -o  output/iter1/result3 -d 4 -t 100
python RandomForest.py -i output/iter2/splitdatafiles.yaml -o  output/iter2/result3 -d 4 -t 100
python RandomForest.py -i output/iter3/splitdatafiles.yaml -o  output/iter3/result3 -d 4 -t 100
python RandomForest.py -i output/iter4/splitdatafiles.yaml -o  output/iter4/result3 -d 4 -t 100
python RandomForest.py -i output/iter5/splitdatafiles.yaml -o  output/iter5/result3 -d 4 -t 100
python RandomForest.py -i output/iter6/splitdatafiles.yaml -o  output/iter6/result3 -d 4 -t 100
python RandomForest.py -i output/iter1/splitdatafiles.yaml -o  output/iter1/result4 -d 4 -t 150
python RandomForest.py -i output/iter2/splitdatafiles.yaml -o  output/iter2/result4 -d 4 -t 150
python RandomForest.py -i output/iter3/splitdatafiles.yaml -o  output/iter3/result4 -d 4 -t 150
python RandomForest.py -i output/iter4/splitdatafiles.yaml -o  output/iter4/result4 -d 4 -t 150
python RandomForest.py -i output/iter5/splitdatafiles.yaml -o  output/iter5/result4 -d 4 -t 150
python RandomForest.py -i output/iter6/splitdatafiles.yaml -o  output/iter6/result4 -d 4 -t 150
python MetricCollection.py -i output/iter1/result1/results.yaml -o output/iter1/result1
python MetricCollection.py -i output/iter2/result1/results.yaml -o output/iter2/result1
python MetricCollection.py -i output/iter3/result1/results.yaml -o output/iter3/result1
python MetricCollection.py -i output/iter4/result1/results.yaml -o output/iter4/result1
python MetricCollection.py -i output/iter5/result1/results.yaml -o output/iter5/result1
python MetricCollection.py -i output/iter6/result1/results.yaml -o output/iter6/result1
python MetricCollection.py -i output/iter1/result2/results.yaml -o output/iter1/result2
python MetricCollection.py -i output/iter2/result2/results.yaml -o output/iter2/result2
python MetricCollection.py -i output/iter3/result2/results.yaml -o output/iter3/result2
python MetricCollection.py -i output/iter4/result2/results.yaml -o output/iter4/result2
python MetricCollection.py -i output/iter5/result2/results.yaml -o output/iter5/result2
python MetricCollection.py -i output/iter6/result2/results.yaml -o output/iter6/result2
python MetricCollection.py -i output/iter1/result3/results.yaml -o output/iter1/result3
python MetricCollection.py -i output/iter2/result3/results.yaml -o output/iter2/result3
python MetricCollection.py -i output/iter3/result3/results.yaml -o output/iter3/result3
python MetricCollection.py -i output/iter4/result3/results.yaml -o output/iter4/result3
python MetricCollection.py -i output/iter5/result3/results.yaml -o output/iter5/result3
python MetricCollection.py -i output/iter6/result3/results.yaml -o output/iter6/result3
python MetricCollection.py -i output/iter1/result4/results.yaml -o output/iter1/result4
python MetricCollection.py -i output/iter2/result4/results.yaml -o output/iter2/result4
python MetricCollection.py -i output/iter3/result4/results.yaml -o output/iter3/result4
python MetricCollection.py -i output/iter4/result4/results.yaml -o output/iter4/result4
python MetricCollection.py -i output/iter5/result4/results.yaml -o output/iter5/result4
python MetricCollection.py -i output/iter6/result4/results.yaml -o output/iter6/result4
