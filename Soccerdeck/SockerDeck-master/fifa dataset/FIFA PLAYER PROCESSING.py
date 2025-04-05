#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import warnings
warnings.simplefilter(action='ignore', category=Warning)

pd.set_option('display.max_columns', None)
fifa = pd.read_csv('players_22.csv')


# In[3]:


fifa.head()


# In[4]:


fifa.info()


# In[5]:


fifa.info()


# In[6]:


fifa.head()


# In[7]:


fifa.drop(['sofifa_id','player_url','short_name','long_name','potential','wage_eur','dob','club_team_id','club_name','league_name','league_level','club_position','club_jersey_number','club_loaned_from','club_joined','club_contract_valid_until','nationality_id','nationality_name','nation_team_id','nation_position','nation_jersey_number','international_reputation','work_rate','body_type','real_face','release_clause_eur','player_tags','player_traits','player_face_url','club_logo_url','club_flag_url','nation_logo_url','nation_flag_url'],axis=1,inplace=True)
    


# In[8]:


fifa.info()


# In[9]:


fifa


# In[10]:


fifa.isnull().sum()


# In[11]:


fifa.drop(['goalkeeping_speed','ls','st','rs','lw','lf','cf','rf','rw','lam','cam','ram','lm','lcm','rm','rcm','lwb','ldm','cdm','rdm','rwb','lb','lcb','cb','rcb','rb','gk'],axis=1,inplace=True)


# In[12]:


fifa.isnull().sum()


# In[13]:


fifa.drop(['cm','physic'],axis=1,inplace=True)


# In[14]:


fifa.info()


# In[15]:


fifa.isnull().sum()


# In[16]:


value_null=fifa[fifa['value_eur'].isnull()]


# In[17]:


print(value_null)


# In[18]:


fifa.fillna({'value_eur':0},inplace=True)


# In[19]:


fifa.isnull().sum()


# In[22]:


fifa.drop(['pace','passing','dribbling','shooting'],axis=1,inplace=True)


# In[23]:


fifa.isnull().sum()


# In[25]:


fifa.to_csv(r'D:\data.csv')


# In[1]:


fifa.describe()


# In[ ]:




