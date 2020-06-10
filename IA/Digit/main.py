# coding: utf-8
import numpy
import arguments
import ui
import utils

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.datasets import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn import metrics
args = arguments.get_args() # Récupère les arguments donnés au programme
# Instructions exécutées dans le mode 'train_test'
if args.mode == "train_test":
	if args.model=="knn":
		x_train,x_test,y_train,y_test=utils.get_train_data_test_data()
		errors=[]
		for k in range(2,60) : 
		    knn=KNeighborsClassifier(k)
		    errors.append(100*(1-knn.fit(x_train,y_train).score(x_test,y_test)))
		plt.plot(range(2,60),errors,'o-')
		plt.show()
	elif args.model=="kmeans":
		wcss = []
		silhouettes=[]
		for i in range(2,1000):
			km=KMeans(n_clusters=i,init='k-means++', max_iter=300,n_init=10, random_state=0)
			X = pd.DataFrame(load_digits().data)
			x_train,x_test,y_train,y_test=train_test_split(X, load_digits().target, test_size=0.3, random_state=42)
			km.fit(x_train)
			silh = metrics.silhouette_score(x_train, km.labels_)
			silhouettes.append(silh)
		plt.plot(range(2,1000), silhouettes, marker='o')
		plt.title("largeur de silhouette")
		plt.xlabel("Number of clusters")
		plt.ylabel("silhouette")
		plt.show()

# Commandes exécutées dans le mode 'use'
elif args.mode == "use":
	if args.model=="knn":
		x_train,x_test,y_train,y_test=utils.get_train_data_test_data()
		KNN = KNeighborsClassifier(7)
		KNN.fit(x_train, y_train)
		ui.build(KNN,y_test,x_test)
	elif args.model=="naive_bayes" :
		x_train,x_test,y_train,y_test=utils.get_train_data_test_data()
		bnb = BernoulliNB()
		bnb.fit(x_train, y_train)
		ui.build(bnb,y_test,x_test)
	elif args.model=="perceptron" :
		x_train,x_test,y_train,y_test=utils.get_train_data_test_data()
		sc = StandardScaler()
		sc.fit(x_train)
		#ui.build(sc,y_test,x_test)
		x_train_std = sc.transform(x_train)
		x_test_std = sc.transform(x_test)
		ppn = Perceptron(n_iter=40, eta0=0.1, random_state=0)
		ppn.fit(x_train_std, y_train)
		ui.build(ppn,y_test,x_test)
	elif args.model=="regression":
		X = pd.DataFrame(load_digits().data)
		x_train,x_test,y_train,y_test=train_test_split(X, load_digits().target, test_size=0.3, random_state=42)
		model=LogisticRegression(random_state=42)
		model.fit(x_train,y_train)
		ui.build(model,y_test,x_test)
	elif args.model=="kmeans":
		X = pd.DataFrame(load_digits().data)
		x_train,x_test,y_train,y_test=train_test_split(X, load_digits().target, test_size=0.3, random_state=42)
		n_clusters = len(np.unique(x_train))
		clf = KMeans(n_clusters =10, random_state=42)
		print(n_clusters)
		clf.fit(x_train)
		ui.build(clf,y_test,x_test)
	elif args.model=="svm":
		x_train,x_test,y_train,y_test=utils.get_train_data_test_data()
		model = svm.SVC(kernel='linear', decision_function_shape='ovr') 
		model.fit(x_train,y_train)
		ui.build(model,y_test,x_test)


else:
	raise ValueError("Mode invalide")
