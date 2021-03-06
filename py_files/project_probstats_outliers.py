# -*- coding: utf-8 -*-
"""Project_ProbStats_Outliers.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lTbMyZI9SpBc1y-Vx-x16Yret9EnqSrA

# Outlier Analysis:
"""

import pandas as pd
import numpy as np
from scipy.stats import gamma
import matplotlib.pyplot as  plt

# Commented out IPython magic to ensure Python compatibility.
# from google.colab import drive
# drive.mount('/content/gdrive')

# %cd /content/gdrive/My Drive/Prob_stats_proj

# %cd D:\StonyBrook\Study\Prob&Stats CSE544\Project

"""##Data Preprocessing"""

data = pd.read_csv('7.csv')

## converting date column to datetime data type ##
data['Date'] = pd.to_datetime(data['Date'])

"""###Data snapshot
Following df view gives a snapshot of the columns in our data and the values in each of them
"""

data

"""###Data features
Following list displays the list of features in our dataset
"""

data.info()

"""##Detecting outliers with Tukey's rule
Using Tukey's rule, we detected outliers and found the number of outliers for each feature

Negative value found at 2020-12-25 for ID state. 

Outliers - 
-  IA confirmed - 38
- IA deaths - 35
- ID confirmed - 28
- ID deaths - 37

But when removing the outliers, most of the original data was getting deleted. So instead we used the original data to perform the asked inferences.
"""

def IQR(X):
    X = sorted(X)
    n = len(X)
    Q1 = X[np.int(np.ceil(n/4))]
    Q3 = X[np.int(np.ceil(3*n/4))]
    
    return Q3-Q1, Q1, Q3   

def outliers(X, handle, a, b):
    if( a < 0): a=0
        
    condition = (X[handle] < a) | (X[handle] > b)
    outlier = X.loc[condition]
    
    return outlier

"""#### Data plot
The following scatter plot represent the data for each of the features and identifies the outliers in yellow
"""

handle = 'ID deaths'

iqr, q1,q3 = IQR(data[handle])
threshold_min = q1 - 1.5 * iqr
threshold_max = q3 + 1.5 * iqr


outlier_data = outliers(data, handle, threshold_min, threshold_max)

plt.scatter(data['Date'], data[handle])
plt.scatter(outlier_data['Date'], outlier_data[handle])
plt.show()
print(len(outlier_data))

handle = 'IA deaths'

iqr, q1,q3 = IQR(data[handle])
threshold_min = q1 - 1.5 * iqr
threshold_max = q3 + 1.5 * iqr


outlier_data = outliers(data, handle, threshold_min, threshold_max)

plt.scatter(data['Date'], data[handle])
plt.scatter(outlier_data['Date'], outlier_data[handle])
plt.show()
print(len(outlier_data))

handle = 'ID confirmed'

iqr, q1,q3 = IQR(data[handle])
threshold_min = q1 - 1.5 * iqr
threshold_max = q3 + 1.5 * iqr


outlier_data = outliers(data, handle, threshold_min, threshold_max)

plt.scatter(data['Date'], data[handle])
plt.scatter(outlier_data['Date'], outlier_data[handle])
plt.show()
print(len(outlier_data))

handle = 'IA confirmed'

iqr, q1,q3 = IQR(data[handle])
threshold_min = q1 - 1.5 * iqr
threshold_max = q3 + 1.5 * iqr


outlier_data = outliers(data, handle, threshold_min, threshold_max)

plt.scatter(data['Date'], data[handle])
plt.scatter(outlier_data['Date'], outlier_data[handle])
plt.show()
print(len(outlier_data))

handle = 'ID confirmed'

iqr, q1,q3 = IQR(data[handle])
threshold_min = q1 - 1.5 * iqr
threshold_max = q3 + 1.5 * iqr


outlier_data = outliers(data, handle, threshold_min, threshold_max)

plt.scatter(data['Date'], data[handle])
plt.scatter(outlier_data['Date'], outlier_data[handle])
plt.show()
print(len(outlier_data))