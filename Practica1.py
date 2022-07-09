"""
Created on Tue Apr 16 15:00:54 2019
@author: david
EXEMPLE CLASSIFICADOR MUTUAL KNN AMB LES DADES IRIS (per un nou exemple)
"""

# Carreguem les llibreries que necessitem
import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd  
import networkx as nx
from sklearn import preprocessing
# Assignem noms de columnes
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']

# Llegim les dades de la url a un dataframe de pandas i el mostrem
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
dataset = pd.read_csv(url, names=names)  
dataset.head()

# Separem les característiques (columnes x) de les classes (columna y) Per x agafem només 2 columnes  
X = dataset.iloc[:, 0:2].values  
y = dataset.iloc[:, 4].values  
print(X)
print(y)
X.shape
y.shape

#traiem duplicats
dup=np.unique(X,return_index=True,axis=0)
X=X[dup[1],:]
y=y[dup[1]]
X.shape
y.shape



#Seleccionem a l'atzar les files que suposem classificades i retenim la resta que considerem no classificades
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
X_train.shape
num_objectes_train=X_train.shape[0]
num_objectes_test=X_test.shape[0]
print(num_objectes_train)
print(num_objectes_test)

#Dibuixem els nostres exemples amb diferents colors segons la classificació
colors = {'Iris-versicolor':'red', 'Iris-virginica':'blue', 'Iris-setosa':'green'}
cols = [colors[i] for i in y_train]
plt.scatter(X_train[:,0],X_train[:,1] , c=cols, s=100)
plt.xlabel("Longitud sèpal")
plt.ylabel("Ample sèpal")
for i, txt in enumerate(range(num_objectes_train)):
    plt.annotate(txt, (X_train[i,0],X_train[i,1]))

# COMENCEM LA CLASSIFICACIÓ D'UN NOU EXEMPLE (EL PRIMER del conjunt de test)


#Afegim el punt a classificar
X_clas = np.append(X_train, X_test[0:1,:],axis=0)

#Tornem a fer el gràfic amb aquest punt en color groc
colors = {'Iris-versicolor':'red', 'Iris-virginica':'blue', 'Iris-setosa':'green'}
cols = [colors[i] for i in y_train]
plt.scatter(X_train[:,0],X_train[:,1] , c=cols, s=50)
plt.scatter(X_test[0,0],X_test[0,1], c='yellow',s=200)
plt.xlabel("Longitud sèpal")
plt.ylabel("Ample sèpal")
for i, txt in enumerate(range(num_objectes_train+1)):
    plt.annotate(txt, (X_clas[i,0],X_clas[i,1]))

# Estandaritzem les 2 variables del X_clas
X_clas=preprocessing.scale(X_clas)


## AQUI COMENÇA LA SOLUCIÓ DE LA PRÀCTICA
# Fem la matriu de distàncies
dist=np.zeros(shape=(num_objectes_train+1,num_objectes_train+1), dtype=float)
for i in range(num_objectes_train+1):
    for j in range(num_objectes_train+1):
            dist[i,j]=np.sqrt(np.sum((X_clas[i,:]-X_clas[j,:])**2))

# Passem la matriu de distàncies a similaritats 1/dist
sim=1/(dist+1)
# grafiquem el graf (complet) amb la matriu d'adjacècncia com les similaritats
G1=nx.from_numpy_matrix(sim)
nx.draw_networkx(G1)

#Determinem els índex dels k més propers
K=4 # ull k ha de ser inferior al nombre de punts -1, és clar
#Ordenem les files amb les distàncies de menys a més sense agafar la primera (que és 0)
dist_sort=dist.argsort(axis=1)[:,1:(K+1)]
# Creem la matriu d'adjacències amb mutual
adj=np.zeros(shape=(num_objectes_train+1,num_objectes_train+1), dtype=float)
for i in range(num_objectes_train+1):
   for j in range(K):
       if i in dist_sort[dist_sort[i,j],:]:
           adj[i,dist_sort[i,j]]=1

# Dibuixem el graf amb les adjacències
G2=nx.from_numpy_matrix(adj)
nx.draw_networkx(G2)

# Assignar la classe al nou exemple
# Agafem de l'última fila (l'exemple que volem classificar) totes les columnes menys la última
# i ho convertim en bool (perquè seran indexos per mirar les classes dels exemples coneguts)
index_clas=adj[-1,:-1].astype(bool)

#Mirem quines són les classes dels que estan relacionats amb la nova observació
#Fixem-nos com ho classificarà
y_train[index_clas]


if True in index_clas:
    u, c = np.unique(y_train[index_clas], return_counts=True)
    y_class=u[c.argmax()]
else:
    y_class='Unclassified'

# Mirem si ho ha fet bé
y_class
y_class==y_test[0]
