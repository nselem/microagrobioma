from biom import load_table

# taxids
# Curtobacterium 2034
# Bifidobacterium 1678
# Clavibacter 1573
# Porphyrobacter 1111
# Achromobacter xylosoxidans 85698
# Brucella 234
# unclassified Achromobacter 2626865
# unclassified Thermomonas 2633315
# Sphingobacteriaceae 84566

table = load_table(f"/mnt/d/data/genomics/solena/solena/biom/8/chile.txt_8.biom")
df = table.to_dataframe().sparse.to_dense()
totalChile = df.sum(axis=0)
curtoChile = df.iloc[list(df.index).index('2034')]
bifidoChile = df.iloc[list(df.index).index('1678')]
claviChile =  df.iloc[list(df.index).index('1573')]

porphyroChile = df.iloc[list(df.index).index('1111')]
achromoChile = df.iloc[list(df.index).index('85698')]
brucellaChile =  df.iloc[list(df.index).index('234')]

unAchromoChile = df.iloc[list(df.index).index('2626865')]
unThermoChile = df.iloc[list(df.index).index('2633315')]
sphingoChile =  df.iloc[list(df.index).index('84566')]


table = load_table(f"/mnt/d/data/genomics/solena/solena/biom/8/maiz.txt_8.biom")
df = table.to_dataframe().sparse.to_dense()
totalMaiz = df.sum(axis=0)
curtoMaiz = df.iloc[list(df.index).index('2034')]
bifidoMaiz = df.iloc[list(df.index).index('1678')]
claviMaiz =  df.iloc[list(df.index).index('1573')]

porphyroMaiz  = df.iloc[list(df.index).index('1111')]
achromoMaiz = df.iloc[list(df.index).index('85698')]
brucellaMaiz =  df.iloc[list(df.index).index('234')]

unAchromoMaiz = df.iloc[list(df.index).index('2626865')]
unThermoMaiz = df.iloc[list(df.index).index('2633315')]
sphingoMaiz =  df.iloc[list(df.index).index('84566')]

table = load_table(f"/mnt/d/data/genomics/solena/solena/biom/8/tomate.txt_8.biom")
df = table.to_dataframe().sparse.to_dense()
totalTomate = df.sum(axis=0)
curtoTomate = df.iloc[list(df.index).index('2034')]
bifidoTomate = df.iloc[list(df.index).index('1678')]
claviTomate =  df.iloc[list(df.index).index('1573')]

porphyroTomate = df.iloc[list(df.index).index('1111')]
achromoTomate = df.iloc[list(df.index).index('85698')]
brucellaTomate =  df.iloc[list(df.index).index('234')]

unAchromoTomate = df.iloc[list(df.index).index('2626865')]
unThermoTomate = df.iloc[list(df.index).index('2633315')]
sphingoTomate =  df.iloc[list(df.index).index('84566')]


print(f"chile - clavi \t{list(claviChile)}")
print(f"chile - curto \t{list(curtoChile)}")
print(f"chile - bifido \t{list(bifidoChile)}")

print(f"chile - porphyro\t{list(porphyroChile)}")
print(f"chile - achromo\t{list(achromoChile)}")
print(f"chile - brucella\t{list(brucellaChile)}")

print(f"chile - unAchromo\t{list(unAchromoChile)}")
print(f"chile - unThermo\t{list(unThermoChile)}")
print(f"chile - sphingo\t{list(sphingoChile)}")

print(f"maiz - clavi \t{list(claviMaiz)}")
print(f"maiz - curto \t{list(curtoMaiz)}")
print(f"maiz - bifido \t{list(bifidoMaiz)}")

print(f"chile - porphyro\t{list(porphyroMaiz)}")
print(f"chile - achromo\t{list(achromoMaiz)}")
print(f"chile - brucella\t{list(brucellaMaiz)}")

print(f"chile - unAchromo\t{list(unAchromoMaiz)}")
print(f"chile - unThermo\t{list(unThermoMaiz)}")
print(f"chile - sphingo\t{list(sphingoMaiz)}")


print(f"tomate - clavi \t{list(claviTomate)}")
print(f"tomate - curto \t{list(curtoTomate)}")
print(f"tomate - bifido \t{list(bifidoTomate)}")

print(f"chile - porphyro\t{list(porphyroTomate)}")
print(f"chile - achromo\t{list(achromoTomate)}")
print(f"chile - brucella\t{list(brucellaTomate)}")

print(f"chile - unAchromo\t{list(unAchromoTomate)}")
print(f"chile - unThermo\t{list(unThermoTomate)}")
print(f"chile - sphingo\t{list(sphingoTomate)}")


porphyroChile = df.iloc[list(df.index).index('1111')]
achromoChile = df.iloc[list(df.index).index('85698')]
brucellaChile =  df.iloc[list(df.index).index('234')]

unAchromoChile = df.iloc[list(df.index).index('2626865')]
unThermoChile = df.iloc[list(df.index).index('2633315')]
sphingoChile =  df.iloc[list(df.index).index('84566')]

