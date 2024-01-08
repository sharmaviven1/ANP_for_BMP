# -*- coding: utf-8 -*-
"""ANP for Agri BMPs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14hPMy8Y2ohlBuINfM2bbWfKLrWe7SC5C

# Import packages
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""# Load Data"""

# specify path to the file here
path = '/content/BNPs table.xlsx'
data = pd.read_excel('/content/BNPs table.xlsx')

# check the format of the data
data.head()

"""# ANP connection efficiencies, populating Supermatrix

$$ \begin{equation*}
S_{il} = \begin{cases}
   \frac{{\sum^M_{j=1}} c^{k=1}_{ij}}{{\sum^M_{j=1}} c^{k=2}_{ij}} ∀
    \text{ } i=l\\      
   \frac{{\sum^M_{j=1}} c^{k=1}_{ij}+{\sum^M_{j=1}} c^{k=1}_{lj}}{{\sum^M_{j=1}} c^{k=2}_{ij}+{\sum^M_{j=1}} c^{k=2}_{lj}} ∀ \text{ } i \neq l
\end{cases}

\end{equation*} $$
"""

# Number of alternatives (BNPs) are read using data.shape[0]
SupMat = np.zeros((data.shape[0],data.shape[0]))
for row in range(data.shape[0]):  # iternating over rows
  for col in range(data.shape[1]+1):  # iterating over cols
   # using the formula from the paper to calculate network efficiencies
   if row==col:
    SupMat[row,col] = data.NitrateLoadReduction[row]/data.Cost[row]
   else:
    SupMat[row,col] = (data.NitrateLoadReduction[row]+data.NitrateLoadReduction[col])/(data.Cost[row]+data.Cost[col])

print(SupMat)

"""# Row normalized supermatrix

$$ \hat{S} = S \phi SJ $$
where $\phi$ is elementwise division and $J$ is all ones matrix.
"""

J =  np.ones_like(SupMat)
np.matmul(SupMat,J)

NormSupMat = np.divide(SupMat,np.matmul(SupMat,J))
print(NormSupMat)

"""# Stabilizing the Supermatrix to compute LimitMatrix"""

LimMat = np.linalg.matrix_power(NormSupMat,200)
print(LimMat)

"""# Saving efficiencies in the datafile"""

data.insert(data.shape[1],"Eff", LimMat[0,:], True)

"""# Selecting best $n$ BMPs"""

n = int(input('Enter value of n:'))

df1 = data.sort_values(by=['Eff'],ascending=False)

df1.BMP[0:n]

"""# Selecting 2nd best $n$ BMPs"""

df2 = df1.reset_index(drop=True)

df2.Eff[n-1] = 0

df2 = df2.sort_values(by=['Eff'],ascending=False)
df2.BMP[0:n]

"""# Selecting 3rd best $n$ BMPs"""

df3 = df1.reset_index(drop=True)
df3

df3.Eff[n-2] = 0
df3 = df3.sort_values(by=['Eff'],ascending=False)
df3.BMP[0:n]