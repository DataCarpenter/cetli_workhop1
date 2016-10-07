# -*- coding: utf-8 -*-
# <nbformat>4</nbformat>

# <codecell>

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
%matplotlib inline
test=pd.read_csv('Test.csv')
train=pd.read_csv('Train.csv')

# <markdowncell>

# So, lets  create a baseline submission file, concentratino on the format, rather than the actual machine learning. 

# <markdowncell>

# First, we collect the rownames of the soon-to-be submission file

# <codecell>

rownames= test['objectId'].tolist()

# <markdowncell>

# Then, makin sure we use unicode everywhere...

# <codecell>

def create_unicode(text):
    return text.decode('utf-8')
train['product_uni']= train['product'].apply(create_unicode)

product_names_uni=train['product_uni'].value_counts().index.tolist()
type(product_names_uni[0])

# <markdowncell>

# Lets use our recently aquired knowledge on datetime to filter the training dataset. In this example, we want to create our submission based on training data onll form the months after may. 

# <codecell>

import datetime
def convert_time(date_string):
    return  datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

train['datetime']=train['createdAt'].apply(convert_time)
train['month']= train['datetime'].apply(lambda x: x.month)

# <markdowncell>

# What is the distribution of the newly creates month column?

# <codecell>

train.month.value_counts()

# <markdowncell>

# Doing the actual filtering:

# <codecell>

filtered_train=train.loc[train.month >6]
filtered_train.head(5)

# <markdowncell>

# What are the frequencies in the filtered column?

# <codecell>

filtered_train['product_uni'].value_counts()

# <markdowncell>

# lets plot the distribution of  these frequency numbers, just because we can.

# <codecell>

freq_counts=filtered_train['product_uni'].value_counts()
plt.hist(freq_counts, bins=50)
plt.show()

# <markdowncell>

# In the sample submission in every row we want to "predict" this distribution. In other words:for every product we want to predict simply its frequency. First we need an empty dataframe with the rigth  rownames and column names.  

# <codecell>

submission= pd.DataFrame(0,index=rownames, columns=product_names_uni)

# <markdowncell>

# Ce now create a list of number which will represent our prediction for every line. Note, that not every product are represented in the frequency list, (because of the filtering ) for those, we can insert an "average" number, say 15.  

# <codecell>

numbers=[]
for prod in product_names_uni:
    if prod in freq_counts.index:
        numbers.extend([freq_counts[prod]])
    else:
        numbers.extend([15])
        

# <markdowncell>

# now pushing this number list inte every row of our submission dataframe.

# <codecell>

for obj_id in rownames:
    submission.loc[obj_id] = numbers

# <codecell>

submission.head(5)

# <codecell>

some minor adjustment to have a properly formed csv

# <codecell>

submission_to_export= submission.reset_index().rename(columns={'index': 'objectId'})
submission_to_export.to_csv('workshop_submission.csv', encoding=('utf-8'), index=False)

# <markdowncell>

# Dont forget the 'utf-8'encoding! 

# <codecell>


