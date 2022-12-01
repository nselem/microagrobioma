import os

#path = '/mnt/d/documents/OneDrive/trabajo/genomica/unam/nelly/agromicrobioma/solena/maiz/'
path = '/mnt/d/data/genomics/solena/solena/kraken_braken/'
maxLevel = 32
# process all files in a folder
taxonNames = dict()
taxonFile = open(f"{path}taxonNames.csv",'w')

for filename in os.listdir(path):
    if "report" not in filename:
        continue    
    outs = []
    for level in range(maxLevel):
        if not os.path.exists(os.path.join(path,'agglomerated',str(level))):
            os.makedirs(os.path.join(path,'agglomerated',str(level)))
        out = open(os.path.join(path,'agglomerated',str(level),filename),'w')
        outs.append(out)
# skip non kraken report files

    f = open(os.path.join(path,filename),'r')
# skip first line for unclassified counts
    f.readline()
    for line in f:
    # sample line
    #  7.08	4246958	726	R	1	root
    #  0      1      2  3   4   5
    # 0. Percentage of reads covered by the clade rooted at this taxon
    # 1. Number of reads covered by the clade rooted at this taxon
    # 2. Number of reads assigned directly to this taxon
    # 3. Taxonomy rank code
    # 4. NCBI taxonomy ID
    # 5. Name
        fields = line.split('\t')
    
    # add taxon name and id pair to known list
        if fields[4] not in taxonNames.keys():
            taxonNames[fields[4]] = fields[5].strip()

    # trim extra characters from taxonomy rank code. kraken-biom will only parse entries with codes in ["D", "P", "C", "O", "F", "G", "S", "SS"]
        fields[3] = fields[3][0]
        taxonomy = fields[-1]
        level = 0
    # check number of spaces to calculate taxonomy level
        for l in taxonomy:
            if l == ' ':
                level += .5
            else:
                break
#        if level > len(outs)-1:
#            if not os.path.exists(os.path.join(path,'agglomerated',str(level))):
#                os.makedirs(os.path.join(path,'agglomerated',str(level)))
#            out = open(os.path.join(path,'agglomerated',str(level),filename),'w')
#            outs.append(out)
    # if taxon is in a terminal branch, print it on every next level
        if fields[2] == fields[1]:
            for l in range(int(level),maxLevel):
                #outs[l].write(line)
                outs[l].write(fields[0])
                for i in range(1,len(fields)):
                    outs[l].write('\t'+fields[i])
                
        else:
            fields[2] = fields[1]
        # change number of reads assigned to the taxon for the number assigned to the whole clade
            outs[int(level)].write(fields[0])
            for i in range(1,len(fields)):
                outs[int(level)].write('\t'+fields[i])
    for out in outs:
        out.close()

for t,n in taxonNames.items():
    taxonFile.write(f"{t},{n}\n")

taxonFile.close()