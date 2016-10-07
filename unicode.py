# -*- coding: utf-8 -*-
# <nbformat>4</nbformat>

# <markdowncell>

# ### Resources
# - http://joelonsoftware.com/articles/Unicode.html 
# - https://www.youtube.com/watch?v=MijmeoH9LT4
# - https://www.youtube.com/watch?v=sgHbC6udIqc

# <codecell>

import pandas as pd
train=pd.read_csv('Train.csv')
sample=pd.read_csv('sample_submission.csv', encoding='utf-8', index_col= 'objectId')

# <markdowncell>

# What lives inside the train datasets 'product' column?

# <codecell>

one_product=train['product'][0]
print one_product
type(one_product)

# <markdowncell>

# What if we try to decode it? 

# <codecell>

one_product.decode('utf-8')

# <markdowncell>

# Althoug the notebook output is a bit crusty, the utf-8 decosed unicode test-representation is the was to go. Here the "print" function wil help the reader, and the 'type' shows, that the variable is unicode.

# <codecell>

unicode_one_product= one_product.decode('utf-8')
print unicode_one_product
print type(unicode_one_product)

# <codecell>

one_product == unicode_one_product

# <markdowncell>

# They look similar, but because the different type, the equalit returns "False". it would be better to throw, an error.

# <codecell>

unicode_one_product.decode('utf-8')

# <markdowncell>

# This erro shows us the main concerne to keep in mind: Python 2.7 tries to implicitly (secterly)  encode everything into ASCII.  'sys.getdefaultencoding()' shows us why

# <codecell>

import sys
sys.getdefaultencoding()

# <codecell>

simple_string='alma'
u_string=u'alma'
print type(simple_string)
print type(u_string)
simple_string == u_string

# <markdowncell>

# altohug they have a differen type 'alma' ans u'alma' happens to be equal. This is considered as a FEATURE by the Py 2.7 developers, but if you happen to have only-unicode chars in your text, it becomes a BUG. 

# <codecell>

all_train_products= train['product'].value_counts().index.tolist()
type(all_train_products[0])


# <markdowncell>

# Lets check out our other source file, the sample submission. It contains unicode characters. 

# <codecell>

all_sample_products= sample.columns.tolist()
type(all_sample_products[0])

# <markdowncell>

# Try to compare the two lists: how many are different?

# <codecell>

len([x for x in all_sample_products if not x in all_train_products])

# <markdowncell>

# 142 products which are missing?  Try it again with proper types. (unicode)

# <codecell>

all_train_producst_unicode= [x.decode('utf-8') for x in all_train_products]
len([x for x in all_sample_products if not x in all_train_producst_unicode])

# <markdowncell>

# Thats better! now we should create a new columns with unicode values in the train table.  

# <codecell>

def create_unicode(text):
    return text.decode('utf-8')

train['product_uni']= train['product'].apply(create_unicode)

# <markdowncell>

# which equals to

# <codecell>

train['product_uni']= train['product'].apply(lambda x: x.decode('utf-8'))

# <codecell>

train['product_uni']
