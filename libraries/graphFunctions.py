def AppendNamesToNodes(nodesFileName, taxonsFileName):
# load taxon id - names dictionary    
    inTaxons = open(taxonsFileName,'r')
    taxonNames = dict()
    for line in inTaxons:
        fields = line.replace('\n','').split(',')
        taxonNames[fields[0]]=fields[1]
# load nodes data into buffer
    inNodes = open(nodesFileName,'r')
    nodes = list()
    header = inNodes.readline().replace('\n','')
    for line in inNodes:
        nodes.append(line.replace('\n',''))
    inNodes.close()
# overwrite file appending the taxon name
    out = open(nodesFileName,'w')
    out.write(f"{header},taxonName\n")
    for node in nodes:
        # node format
        # Id	Label
        taxonId = node.split(',')[1]
        out.write(f"{node},{taxonNames[taxonId]}\n")
    out.close()

#for level in range(10,11):
 #   AppendNamesToNodes(f"/mnt/d/documents/OneDrive/trabajo/codigos/unam/nelly/agromicrobioma/networks/maiz_nivel_{level}_network_nodes.csv","/mnt/d/documents/OneDrive/trabajo/genomica/unam/nelly/agromicrobioma/solena/maiz/taxonNames.csv")
