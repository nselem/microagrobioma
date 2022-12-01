from operator import index
import pandas as pd
import numpy as np
import statisticsFunctions
from biom import load_table

taxonomicDistances = dict()
orderedTaxonomies = 'species|genus|family|order|class|phylum|kingdom|superkingdom|root'
level = 0
for taxonomy in orderedTaxonomies.split('|'):
    taxonomicDistances[taxonomy] = level
    level += 1

def CalculatePhylogeneticDistanceTaxons(dataI,dataJ):
    if (dataI["rank"] is np.nan) or (dataJ["rank"] is np.nan):
        return "root"
    traceI = dataI["traceTaxId"]
    traceJ = dataJ["traceTaxId"]
    levelsI = traceI.split('|')
    currentLevel = 0
    for l in levelsI:
        if l in traceJ:
            break
        currentLevel += 1
    ranksI = dataI["traceRank"].split('|')
# go to the next rank on the list (meant to skip "no rank")
    while ranksI[currentLevel] not in taxonomicDistances.keys():
        currentLevel +=1
    return ranksI[currentLevel]
    

def CalculatePhylogeneticDistanceMatrix (phylogenyFileName, outFileName):
    data = pd.read_csv(phylogenyFileName)
    distRank = pd.DataFrame(0, columns=data["taxid"], index = data["taxid"])
    distNumber = pd.DataFrame(0, columns=data["taxid"], index = data["taxid"])

    for i in range(len(data)):
        if i%50 == 0:
            print(f"progress:\t{i}")
        dataI = data.iloc[i]
        taxonI = dataI["taxid"]
        
        for j in range(len(data)):
            dataJ = data.iloc[j]
            taxonJ = dataJ["taxid"]
            rank = CalculatePhylogeneticDistanceTaxons(dataI,dataJ)
            distRank.at[ taxonI, taxonJ ] = rank
            if i != j:
                distNumber.at[ taxonI, taxonJ ] = taxonomicDistances[ rank ]
            else:
                distNumber.at[ taxonI, taxonJ ] = 0
    distRank.to_csv(outFileName+'_rank.csv')
    distNumber.to_csv(outFileName+'_number.csv')



path = "/mnt/d/data/genomics/solena/solena/tda"

table = load_table(f"/mnt/d/data/genomics/unam/agromicrobioma/biom/chile_nivel_{8}.biom")
outName = f"chile_nivel_{8}"

# https://biom-format.org/documentation/table_objects.html
numTaxons = int(table.shape[0])
numSamples = int(table.shape[1])

rawData = table.to_dataframe().sparse.to_dense()
statisticsFunctions.ReBoot(rawData)
clavibacterTaxon = '1573'

statisticsFunctions.CalculateCorrelationTaxon(rawData, clavibacterTaxon, f"{path}/correlations_clavibacter_chile_genus.csv")




path = "/mnt/d/data/genomics/solena/solena/tda"

phylogenyFileName = f"{path}/taxids_phylogeny.csv"
outFileName = f"{path}/phylogenetic_distances_all"
CalculatePhylogeneticDistanceMatrix(phylogenyFileName, outFileName)