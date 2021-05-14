# -*- coding: utf-8 -*-
"""Project_ProbStats_C.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zgNhZfjS7AqIrvJGFkJOV1Di1jzMKu4w

**Question C:** Inference the equality of distributions in the two states (distribution of daily #cases and daily #deaths) for the last three months of 2020 (Oct, Nov, Dec) of your dataset using **K-S test and Permutation test**. For the K-S test, use both 1-sample and 2-sample tests. For the 1-sample test, try Poisson, Geometric, and Binomial. To obtain parameters of these distributions to check against in 1-sample KS, use MME on the Oct-Dec 2020 data of the first state in your dataset to obtain parameters of the distribution, and then check whether the Oct-Dec 2020 data for the second state in your dataset has the distribution with the obtained MME parameters. For the permutation test, use 1000 permutations. Use a threshold of 0.05 for both K-S test and Permutation test.
"""

import pandas as pd
import numpy as np
from scipy.stats import poisson
from scipy.stats import geom
from scipy.stats import binom

# Commented out IPython magic to ensure Python compatibility.
# %cd D:\StonyBrook\Study\Prob&Stats CSE544\Project

# from google.colab import drive
# drive.mount('/content/gdrive')

# %cd /content/gdrive/My Drive/Prob_stats_proj

data = pd.read_csv('7.csv')

## converting date column to datetime data type ##
data['Date'] = pd.to_datetime(data['Date'])

"""Below printed is the data that is obtained from the CSV file for the states IA and ID.

"""

data

def get_eCDF(X):
    n = len(X)
    Srt = sorted(X)
    delta = .1
    X = []
    Y = [0]
    for i in range(0,n):
        X = X + [Srt[i]]
        Y = Y + [Y[len(Y)-1]+(1/n)]
    Y = Y + [1]
        
    return X,Y


def KS_Test_1_sample(X1,Y1, CDF_function, parameter):
    tot_max = -1
        
    Table = np.zeros((len(X1),4))
    for i in range(len(Table)):
        Table[i,0] = Y1[i]
        Table[i,1] = Y1[i+1]
        F_x = CDF_function(parameter, X1[i])
        Table[i,2] = abs(Table[i,0] - F_x)
        Table[i,3] = abs(Table[i,1] - F_x)
        cmax = max(Table[i,2], Table[i,3])
        if cmax > tot_max:
            tot_max = cmax
        
        
    return tot_max
    

def KS_test_2_sample(X1,Y1, X2,Y2):
    Table = np.zeros((len(X1),6))
    tot_max = -1
    for i in range(len(Table)):
        Table[i,0] = Y1[i]
        Table[i,1] = Y1[i+1]
        index1 = [idx for idx, val in enumerate(X2) if val >= X1[i]]
        index2 = [idx for idx, val in enumerate(X2) if val < X1[i]]
        if index1 == []:
            Table[i,3] = 1
        else :    
            Table[i,3] = Y2[index1[0]]
        if index2 == []:
            Table[i,2] = 0
        else:
            Table[i,2] = Y2[index2[-1]]
        #print(index1, index2)
        
        #Table[i,3] = Y2[index1[0]]
        Table[i,4] = abs( Table[i,0] - Table[i,2])
        Table[i,5] = abs(Table[i,1] - Table[i,3])
        cmax = max(Table[i,4], Table[i,5])
        if cmax > tot_max:
            tot_max = cmax
            x1_max = X1[i]
            y1_max = Table[i,0]
            y2_max = Table[i,2]
    
    return tot_max

def get_Ti(n_perm, data, n1):
    T = []
    for i in range(n_perm):
        permute = np.random.permutation(len(data))
        D1 = data[permute[:n1]]
        D2 = data[permute[n1:]]
        T.append(abs(np.mean(D1) - np.mean(D2)))
    
    return np.array(T)

def get_p_value(T,T_obs):
    count = np.sum(T > T_obs)
    p_val = count/len(T)
    return p_val

"""We filter the data to obtain the data only in the date range '2020-10-01', '2020-12-31'."""

###### Getting Oct- Dec 2020 data ######
start_date, end_date = '2020-10-01', '2020-12-31'
condition = (data['Date'] >= start_date) & (data['Date'] <= end_date)
oct_dec_data = data.loc[condition]

################## 1- sample KS test ####################

"""# 1- Sample KS test

##Tests for IA confirmed cases with ID confirmed cases
"""

###### Tests for IA confirmed cases with ID confirmed cases ######

handle = 'IA confirmed'
test_handle = 'ID confirmed'

# Obtaining eCDF for test_handle
test_handle_data = oct_dec_data[test_handle]

test_X, test_Y = get_eCDF(test_handle_data)

"""###Poisson distribution :"""

# Assuming Poisson distribution 

def MME_Poisson(X):
    estimate = np.mean(X)
    return estimate

def CDF_Poisson(lambda_, x):
    prob = poisson.cdf(x, lambda_)
    return prob

CDF_dist = CDF_Poisson

# Obtaining MME for IA confirmed cases 
print('####### Poisson Distribution ########')
lambda_ = MME_Poisson(oct_dec_data[handle])
print(' Poisson parameter lambda : ', lambda_)

# KS-test to be performed on test_handle
KS_value = KS_Test_1_sample(test_X, test_Y, CDF_dist, lambda_ )

print(' KS statistic : ', KS_value)

# Critical threshold is 0.05

# Reject Null hypothesis

"""**Result of 1 sample ks test for poisson distribution:**

Null hypothesis (H0) : Distribution of confirmed cases in the period equals poisson distribution.

Alternate hypothesis (H1) : Distribution of confirmed cases in the period is not poisson distribution.

Procedure: We have obtained the lambda parameter for poisson distribution by using MME on the IA state's data which is the mean of the distribution. Then calculated the maximum differences between all the points in the cdf. The critical value of 0.05 is used as mentioned in the question. 

As the KS value obtained is 0.808 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

###Geometric distribution :
"""

# Assuming Geometric distribution 

def MME_Geometric(X):
    sample_mean = np.mean(X)
    estimate = 1/sample_mean
    
    return estimate

def CDF_Geometric(p,x):
    prob = geom.cdf(x, p)
    return prob

print('####### Geometric Distribution ########')
p = MME_Geometric(oct_dec_data[handle])
CDF_dist = CDF_Geometric

print(' Geometric parameter : ', p)

KS_value = KS_Test_1_sample(test_X, test_Y, CDF_dist, p )

print(' KS statistic : ', KS_value)

# Critical threshold is 0.05

# Reject Null hypothesis

"""**Result of 1 sample ks test for geometric distribution:**

Null hypothesis (H0) : Distribution of confirmed cases in the period equals geometric distribution.

Alternate hypothesis (H1) : Distribution of confirmed cases in the period is not geometric distribution.

Procedure: We have obtained the geometric parameter for geometric distribution by using MME on the IA state's data which is the (1/mean of the distribution). Then calculated the maximum differences between all the points in the cdf. The critical value of 0.05 is used as mentioned in the question. 

As the KS value obtained is 0.271 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

###Binomial distribution :
"""

# Assuming Binomial distribution


def MME_Binomial(X):
    mean = np.mean(X)
    var = np.var(X)
    estimate_p = 1 - (var/mean)
    estimate_n = mean/estimate_p
    
    #print(mean,var)
    
    return estimate_p,estimate_n

def CDF_Binomial(params,x):
    prob = binom.cdf(x, params[0], params[1])
    return prob
    
print('####### Binomial Distribution ########')
n,p = MME_Binomial(oct_dec_data[handle])
CDF_dist = CDF_Binomial

print(' Binomial parameters(n,p) : ', n,p)

KS_value = KS_Test_1_sample(test_X, test_Y, CDF_dist, [n,p] )

print(' KS statistic : ', KS_value)

# Critical threshold is 0.05

# Reject Null hypothesis

"""Result of 1 sample ks test for binomial distribution:

Null hypothesis (H0) : Distribution of confirmed cases in the period equals binomial distribution.

Alternate hypothesis (H1) : Distribution of confirmed cases in the period is not binomial distribution.

Procedure: We have obtained the binomial parameter using the formula in the def MME_Binomial and IA state data. Then calculated the maximum differences between all the points in the cdf. The critical value of 0.05 is used as mentioned in the question.

As the KS value obtained is 0.989 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

##Tests for IA death cases with ID death cases
"""

###### Tests for IA death cases with ID death cases ######

handle = 'IA deaths'
test_handle = 'ID deaths'

test_handle_data = oct_dec_data[test_handle]

test_X, test_Y = get_eCDF(test_handle_data)

"""###Poisson distribution :"""

# Assuming Poisson distribution 
CDF_dist = CDF_Poisson

print('####### Poisson Distribution ########')
lambda_ = MME_Poisson(oct_dec_data[handle])
print(' Poisson parameter lambda : ', lambda_)

KS_value = KS_Test_1_sample(test_X, test_Y, CDF_dist, lambda_ )

print(' KS statistic : ', KS_value)

# Critical threshold is 0.05

# Reject Null hypothesis

"""**Result of 1 sample ks test for poisson distribution:**

Null hypothesis (H0) : Distribution of deaths in the period equals poisson distribution.

Alternate hypothesis (H1) : Distribution of deaths in the period is not poisson distribution.

Procedure: We have obtained the lambda parameter for poisson distribution by using MME on the IA deaths data which is the mean of the distribution. Then calculated the maximum differences between all the points in the cdf. The critical value of 0.05 is used as mentioned in the question. 

As the KS value obtained is 0.748 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

###Geometric distribution
"""

# Assuming Geometric distribution 

print('####### Geometric Distribution ########')
p = MME_Geometric(oct_dec_data[handle])
CDF_dist = CDF_Geometric

print(' Geometric parameter : ', p)

KS_value = KS_Test_1_sample(test_X, test_Y, CDF_dist, p )

print(' KS statistic : ', KS_value)

# Critical threshold is 0.05

# Reject Null hypothesis

"""Result of 1 sample ks test for geometric distribution:

Null hypothesis (H0) : Distribution of deaths in the period equals geometric distribution.

Alternate hypothesis (H1) : Distribution of deaths in the period is not geometric distribution.

Procedure: We have obtained the geometric parameter for geometric distribution by using MME on the IA deaths data which is the (1/mean of the distribution). Then calculated the maximum differences between all the points in the cdf. The critical value of 0.05 is used as mentioned in the question.

As the KS value obtained is 0.373 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

###Binomial distribution:
"""

# Assuming Binomial distribution
print('####### Binomial Distribution ########')
n,p = MME_Binomial(oct_dec_data[handle])
CDF_dist = CDF_Binomial

print(' Binomial parameters(n,p) : ', n,p)

KS_value = KS_Test_1_sample(test_X, test_Y, CDF_dist, [n,p] )

print(' KS statistic : ', KS_value)

# Critical threshold is 0.05

# Reject Null hypothesis

"""Result of 1 sample ks test for binomial distribution:

Null hypothesis (H0) : Distribution of deaths in the period equals binomial distribution.

Alternate hypothesis (H1) : Distribution of deaths in the period is not binomial distribution.

Procedure: We have obtained the binomial parameter using the formula in the def MME_Binomial using IA deaths data. Then calculated the maximum differences between all the points in the cdf. The critical value of 0.05 is used as mentioned in the question.

As the KS value obtained is 1.0 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

# KS 2-sample Test

##Tests for IA confirmed cases with ID confirmed cases
"""

###### Tests for IA confirmed cases with ID confirmed cases ######

handle = 'IA confirmed'
test_handle = 'ID confirmed'

# Obtaining eCDF for handles
handle_data = oct_dec_data[handle]

test_handle_data = oct_dec_data[test_handle]

X1, Y1 = get_eCDF(handle_data)
X2, Y2 = get_eCDF(test_handle_data)


KS_value = KS_test_2_sample(X1,Y1, X2,Y2)

print(' KS statistic : ', KS_value)

# Reject Null Hypothesis

"""Result of 2 sample ks test for IA confirmed and ID confirmed

Null hypothesis (H0) : Distribution of confirmed cases in the IA state equals Distribution of confirmed cases in the ID state

Alternate hypothesis (H1) : Distribution of confirmed cases in the IA state not equals Distribution of confirmed cases in the ID state

Procedure: Generate the cdf for both the distributions(both states). Then we apply the KS 2 sample test to get the maximum difference between the distributions. The critical value of 0.05 is used as mentioned in the question.

As the KS value obtained is 0.2808 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

##Tests for IA death cases with ID death cases
"""

###### Tests for IA death cases with ID death cases ######

handle = 'IA deaths'
test_handle = 'ID deaths'

# Obtaining eCDF for handles
handle_data = oct_dec_data[handle]

test_handle_data = oct_dec_data[test_handle]

X1, Y1 = get_eCDF(handle_data)
X2, Y2 = get_eCDF(test_handle_data)


KS_value = KS_test_2_sample(X1,Y1, X2,Y2)

print(' KS statistic : ', KS_value)

# Reject Null Hypothesis

"""Result of 2 sample ks test for IA deaths and ID deaths

Null hypothesis (H0) : Distribution of deaths in the IA state equals Distribution of deaths in the ID state

Alternate hypothesis (H1) : Distribution of deaths in the IA state not equals Distribution of deaths in the ID state

Procedure: Generate the cdf for both the distributions(both states). Then we apply the KS 2 sample test to get the maximum difference between the distributions. The critical value of 0.05 is used as mentioned in the question.

As the KS value obtained is 0.236 and c = 0.05. As KS value is greater than critical value, we reject the null hypothesis.

Is KS test applicable?
There are no assumptions under KS test. Hence the test is applicable.

# Permutation test

##Test for IA confirmed cases with ID confirmed cases
"""

###### Test for IA confirmed cases with ID confirmed cases ######

handle = 'IA confirmed'
test_handle = 'ID confirmed'

# Obtaining eCDF for handles
handle_data = oct_dec_data[handle]

test_handle_data = oct_dec_data[test_handle]

T_obs = np.abs(np.mean(handle_data) - np.mean(test_handle_data))

print(" T_observed is : " ,T_obs)

total_data = np.concatenate((np.array(handle_data) , np.array(test_handle_data)))

T_i = get_Ti(1000, total_data, len(handle_data))

p = get_p_value(T_i, T_obs)

print(' p statistic : ', p)

# Reject Null Hypothesis

"""Result of Permutation test for IA confirmed and ID confirmed

Null hypothesis (H0) : Distribution of confirmed cases in the IA state equals Distribution of confirmed cases in the ID state

Alternate hypothesis (H1) : Distribution of confirmed cases in the IA state not equals Distribution of confirmed cases in the ID state

Procedure: 
Find T_obs value by using:  
T_obs = | mean(IA confirmed) - mean(ID_confirmed) | 
Then we concatenate all the confirmed cases counts from both train and test sets. And then create 1000 permutations from the set and calculate the p-value for each of the permutation generated by using the same formula mentioned above for the permuted two partitions.
Then we count the number of permutations that resulted in a p value greater than T_obs. P-value is calculated by divind count obtained by 1000.
If the p-value is less than or equal to c. Then we reject the null hypothesis. 

Result: As the obtained p-value is 0 which is lower than the given threshold of 0.05. We reject the null hypothesis.

Is Permutation test applicable?
There are no assumptions under Permutation test. Hence the test is applicable.

##Test for IA death cases with ID death cases
"""

###### Test for IA death cases with ID death cases ######


handle = 'IA deaths'
test_handle = 'ID deaths'

# Obtaining eCDF for handles
handle_data = oct_dec_data[handle]

test_handle_data = oct_dec_data[test_handle]

T_obs = np.abs(np.mean(handle_data) - np.mean(test_handle_data))

print(" T_observed is : " ,T_obs)


total_data = np.concatenate((np.array(handle_data) , np.array(test_handle_data)))

T_i = get_Ti(1000, total_data, len(handle_data))

p = get_p_value(T_i, T_obs)

print(' p statistic : ', p)

# Reject Null Hypothesis

"""Result of Permutation test for IA deaths and ID deaths

Null hypothesis (H0) : Distribution of deaths in the IA state equals Distribution of deaths in the ID state

Alternate hypothesis (H1) : Distribution of deaths in the IA state not equals Distribution of deaths in the ID state

Procedure: Find T_obs value by using:
T_obs = | mean(IA confirmed) - mean(ID_confirmed) | Then we concatenate all the deaths counts from both train and test sets. And then create 1000 permutations from the set and calculate the p-value for each of the permutation generated by using the same formula mentioned above for the permuted two partitions. Then we count the number of permutations that resulted in a p value greater than T_obs. P-value is calculated by divind count obtained by 1000. If the p-value is less than or equal to c. Then we reject the null hypothesis.

Result: As the obtained p-value is 0 which is lower than the given threshold of 0.05. We reject the null hypothesis.

Is Permutation test applicable?
There are no assumptions under Permutation test. Hence the test is applicable.
"""