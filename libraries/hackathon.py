
import pandas as pd
from sklearn.decomposition import PCA

path = 'data/EMP.5k.csv'
df = pd.read_csv(path)

pca = PCA(n_components=500)
principalComponents = pca.fit_transform(df)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])


