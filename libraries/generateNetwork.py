import math
from biom import load_table
from scipy.spatial import distance
from scipy import stats
import pandas as pd
import numpy as np
import datetime
from joblib import Parallel, delayed
from libraries import statisticsFunctions
import os
import sys


np.random.seed(1000)

def generate( biomFileName, outputFileName):
    table = load_table(biomFileName)
    # numTaxons = int(table.shape[0])
    # numSamples = int(table.shape[1])
    rawData = table.to_dataframe().sparse.to_dense()
    statisticsFunctions.ReBoot(rawData)
    network = statisticsFunctions.CalculateMetricsParallel(rawData)
    statisticsFunctions.printNetwork(network,f"networks/{outputFileName}_raw_network.csv")
    statisticsFunctions.printNetworkGephi(network,list(rawData.index),f"networks/{outputFileName}_network")

# statisticsFunctions.PermutationTest(rawData, network, numPermutations = numPermutations, reBoot = True)
# statisticsFunctions.PermutationTest(rawData, network, bootstrap=True, numPermutations = numPermutations, reBoot = True)
