#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import numpy as np
from sklearn import linear_model


# In[28]:


df=pd.read_csv('data.csv')


# In[29]:


df.head()


# In[30]:


import math
mean_eurval=math.floor(df.value_eur.median())
mean_eurval


# In[31]:


df.value_eur=df.value_eur.replace(0,mean_eurval)


# In[32]:


df


# In[42]:


df.drop(['ID','age','height_cm','weight_kg','player_positions','weak_foot','skill_moves'],axis=1,inplace=True)
print(df.columns.values)


# In[43]:


inputs = df.drop('value_eur',axis='columns')

df
# In[ ]:





# In[44]:


target = df['value_eur']


# In[45]:


target


# In[46]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(inputs,target,test_size=0.2) 


# In[48]:


X_train


# In[49]:


from sklearn.linear_model import LinearRegression
clf = LinearRegression()
clf.fit(X_train, y_train)


# In[54]:


clf.score(X_train,y_train)


# In[51]:


from sklearn import tree
model = tree.DecisionTreeClassifier()


# In[53]:


model.fit(X_train, y_train)


# In[57]:


model.score(X_test, y_test)


# In[58]:


model.predict(X_test)


# In[62]:


model.predict([[65,51,73,66,59,68,64,67,68,46,65,76,73,73,64,77,70,90,84,66,66,51,25,72,56,73,67,26,24,44,10,11,9,8,9]])


# In[63]:


inputsPer = df.drop('overall',axis='columns')


# In[65]:


targetPer = df['overall']


# In[66]:


X_train, X_test, y_train, y_test = train_test_split(inputsPer,targetPer,test_size=0.2) 


# In[68]:


X_train


# In[69]:


clf.fit(X_train, y_train)


# In[70]:


clf.score(X_test,y_test)


# In[80]:


clf.predict([[40000,85,95,71,91,88,96,93,88,93,85,91,94,90,78,93,95,86,68,71,66,69,71,93,44,40,77,46,20,24,35,14,6,11,8]])


# In[ ]:




