import graphFunctions
import math
from biom import load_table
from scipy.spatial import distance
from scipy import stats
import pandas as pd
import numpy as np
import datetime
from joblib import Parallel, delayed
import statisticsFunctions
import os
import sys

path = '/mnt/d/data/genomics/solena/solena/'

if not os.path.exists(os.path.join(path,'networks')):
    os.mkdir(os.path.join(path,'networks'))
np.random.seed(1)
start = datetime.datetime.now()
numPermutations = 100
numBootstraps   = 100

# load condition list
conditionsIn = open(os.path.join(path,'conditionsList.txt'),'r')
conditions=conditionsIn.read().splitlines()
conditionsIn.close()

# iterate over network levels and then conditions
for level in range(2,32):
    print("--------------------")
    print("--------------------")
    print(f"------ level ------ {level}")
    print("--------------------")
# create folder for each level
    localPath = os.path.join(path,'networks',str(level))
    if not os.path.exists(localPath):
        os.mkdir(os.path.join(localPath))

    for condition in conditions:
        print(f"------ condition ------ {condition}")
        table = load_table(os.path.join(path,'biom',str(level),f"{condition}_{level}.biom"))
        outName = os.path.join(localPath, f"{condition}_{level}".replace('.txt',''))

# https://biom-format.org/documentation/table_objects.html
        numTaxons = int(table.shape[0])
        numSamples = int(table.shape[1])

        rawData = table.to_dataframe().sparse.to_dense()
        statisticsFunctions.ReBoot(rawData)
        network =list()

        network = statisticsFunctions.CalculateMetricsParallel(rawData)
        statisticsFunctions.printNetwork(network,os.path.join(localPath, f"{outName}_raw_network.csv"))
        statisticsFunctions.printNetworkGephi(network,list(rawData.index), os.path.join(localPath, f"{outName}_network"))
        graphFunctions.AppendNamesToNodes(os.path.join(localPath, f"{outName}_network_nodes.csv"), os.path.join(path,'taxonNames.csv'))