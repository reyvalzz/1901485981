# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 01:29:52 2019
@author: ASUS
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

df = pd.read_csv("Book4100100CSV.csv", sep=";")
Independent = df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]].values
Dependent = df.iloc[:, 19].values

Independent_train, Independent_test, Dependent_train, Dependent_test = train_test_split(Independent, Dependent, test_size = 0.5, random_state = 1)
scaleIndependent = StandardScaler()
Independent_train = scaleIndependent.fit_transform(Independent_train)
Independent_test = scaleIndependent.transform(Independent_test)

clsfierGaussian = GaussianNB()
clsfierGaussian.fit(Independent_train, Dependent_train)
Dependent_pred = clsfierGaussian.predict(Independent_test)

vectoraccuracy = cross_val_score(estimator=clsfierGaussian,X=Independent_train,y=Dependent_train,cv=10)
mean = vectoraccuracy.mean()
deviasi = vectoraccuracy.std()

confusionmatrix = confusion_matrix(Dependent_test, Dependent_pred)
clsreport = classification_report(Dependent_test, Dependent_pred)

print('------ Di bawah ini adalah Confusion Matrix -----')
print(confusionmatrix)
print('-------------------------------------------------\n')
print('------ Di bawah ini adalah Classification Report -----')
print(clsreport)
print('-------------------------------------------------')
print("mean of accuracy: ", mean)
print('-------------------------------------------------')
print("deviasi: ", deviasi)