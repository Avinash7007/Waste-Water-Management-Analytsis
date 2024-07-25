#!/usr/bin/env python
# coding: utf-8

# # Importing the necessary libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# In[2]:


# igonre the warning

import os 
import warnings
warnings.filterwarnings('ignore')


# # Read the data from csv

# In[3]:


Sources_df =pd.read_csv(r"D:\2-Project\9-Waterproject\Source.csv")
Sources_df


# In[4]:


Trtplant_df= pd.read_csv(r"D:\2-Project\9-Waterproject\Treatment Plant.csv")
Trtplant_df


# In[5]:


WstWtrtrt_df = pd.read_csv(r"D:\2-Project\9-Waterproject\WasteWaterTreatmentFact.csv")
WstWtrtrt_df


# In[6]:


Sources_df.info()


# In[7]:


Trtplant_df.info()


# In[8]:


WstWtrtrt_df.info()


# # Data cleaning and Transfarmation Activities

# In[9]:


# checking the null values and duplicate row


# In[10]:


Sources_df.isnull().sum()


# In[11]:


Trtplant_df.isnull().sum()


# In[12]:


WstWtrtrt_df.isnull().sum()


# In[13]:


# check duplicates values


# In[14]:


Sources_df.duplicated().sum()


# In[15]:


Trtplant_df.duplicated().sum()


# In[16]:


WstWtrtrt_df.duplicated().sum()


# In[17]:


# change the data types


# In[18]:


Sources_df.dtypes


# In[19]:


Trtplant_df.dtypes


# In[20]:


WstWtrtrt_df.dtypes


# In[21]:


WstWtrtrt_df['Date'] = pd.to_datetime(WstWtrtrt_df['Date'], format='mixed', dayfirst=True)


# In[22]:


WstWtrtrt_df.dtypes


# In[23]:


# Deriving new column day name

WstWtrtrt_df['Day Name']=WstWtrtrt_df['Date'].dt.day_name()


# In[24]:


WstWtrtrt_df


# In[25]:


WstWtrtrt_df['Day Name']


# In[26]:


WstWtrtrt_df.info()


# In[27]:


# clean capacity column data
Trtplant_df['Capacity']


# In[28]:


Trtplant_df['Capacity'].str.split(' ').str.get(0).astype('int')


# In[29]:


Trtplant_df['Capacity_new'] = Trtplant_df['Capacity'].str.split(' ').str.get(0).astype('int')


# In[30]:


Trtplant_df.info()


# In[31]:


Trtplant_df['Capacity_new']


# # Data Modeling

# In[32]:


# Establin g new realtionship between sources_df and trtplant_df ,Trtfact_df

WstWtrtrt_Sources_df = pd.merge(WstWtrtrt_df,Sources_df,on ='SourceID',how='left')


# In[33]:


WstWtrtrt_Sources_df


# In[34]:


# Establish new relationship between trtplant_df & wstwtrt_df

WstWtrtrt_TrtPlant_df= pd.merge(WstWtrtrt_Sources_df,Trtplant_df,on='PlantID',how='left')


# In[35]:


WstWtrtrt_TrtPlant_df


# # Data Visualization

# In[36]:


# Plant that is treating maximum and minimum volumne of waste water
WstWtrtrt_TrtPlant_df


# In[37]:


WstWtrtrt_TrtPlant_df_grouped = WstWtrtrt_TrtPlant_df.groupby('name',as_index = False)['Volume of Water Treated'].sum()


# In[38]:


WstWtrtrt_TrtPlant_df_grouped


# In[39]:


# plot total volume of waste water treated by different treatment plants 

fig =px.bar(WstWtrtrt_TrtPlant_df_grouped.sort_values(by='Volume of Water Treated',ascending=False),template='plotly_dark',x='name', y='Volume of Water Treated',color= 'name',text='Volume of Water Treated')
fig.update_layout(xaxis_title='Treatment Plant Name',yaxis_title = 'Volume of Waste Water Treated(million galon)',title=dict(text='Total Volume of waste Water Treated by Different Treatment Plants',x=0.5),width=1000)


# In[40]:


# KPI 2 : % Contribution of waste water from different Sources

WstWtrtrt_Sources_df


# In[41]:


WstWtrtrt_Sources_grouped_df=WstWtrtrt_Sources_df.groupby('Source Name',as_index=False)['Volume of Water Treated'].sum()


# In[42]:


WstWtrtrt_Sources_grouped_df


# In[43]:


fig=px.pie(WstWtrtrt_Sources_grouped_df,names='Source Name',values='Volume of Water Treated',template='plotly_dark',hole=0.5)
fig.update_layout(width=500,title=dict(text='% Contribution of waste water from different Sources',x=0.5))
fig.show()


# In[44]:


# KPI 3 : Identify Highly utilized Treatment Plant
# Summation on Volume of Waste Water on the basis of Plant name and Date
WstWtrtrt_TrtPlant_grp_vol_df=WstWtrtrt_TrtPlant_df.groupby(['name','Date'],as_index=False)['Volume of Water Treated'].sum().sort_values(by=['name','Date'])


# In[45]:


# Taking mean of capacity_new column on the basis of Plant name and Date
WstWtrtrt_TrtPlant_grp_cap_df=WstWtrtrt_TrtPlant_df.groupby(['name','Date'],as_index=False)['Capacity_new'].mean().sort_values(by=['name','Date'])


# In[46]:


# Identifying Utilization of Treatment Plants on Daily basis 
WstWtrtrt_TrtPlant_grp_cap_df['Utilization']=WstWtrtrt_TrtPlant_grp_vol_df['Volume of Water Treated']/WstWtrtrt_TrtPlant_grp_cap_df['Capacity_new'] * 100


# In[47]:


# Rounding data to 2 places
WstWtrtrt_TrtPlant_grp_cap_df['Utilization']=WstWtrtrt_TrtPlant_grp_cap_df['Utilization'].round(2)


# In[48]:


# Identifying average utilization of treatment plant
Avg_utilization_df=WstWtrtrt_TrtPlant_grp_cap_df.groupby('name',as_index=False)['Utilization'].mean().round(2)


# In[49]:


# Plotting Utilization of Different Treatment Plants  
fig=px.bar(Avg_utilization_df.sort_values(by='Utilization'),x='Utilization',y='name',template='plotly_dark',color='Utilization',text='Utilization')
fig.update_layout(title=dict(text='Utilization of Treatment Plants',x=0.5),width=1000)
fig.show()


# In[50]:


# KPI 4  Identifying Highly Efficient treatment plant

WstWtrtrt_TrtPlant_df


# In[51]:


succesful_Treated_df=WstWtrtrt_TrtPlant_df[WstWtrtrt_TrtPlant_df['Result']=='Pass'].groupby('name',as_index=False)['Volume of Water Treated'].sum().sort_values(by='name')
succesful_Treated_df


# In[52]:


WstWtrtrt_TrtPlant_df_grouped = WstWtrtrt_TrtPlant_df_grouped.sort_values(by='name')
WstWtrtrt_TrtPlant_df_grouped


# In[53]:


succesful_Treated_df['Volume of Water Treated']/WstWtrtrt_TrtPlant_df_grouped['Volume of Water Treated']


# In[54]:


succesful_Treated_df['Efficiency']=succesful_Treated_df['Volume of Water Treated']/WstWtrtrt_TrtPlant_df_grouped['Volume of Water Treated']*100


# In[55]:


succesful_Treated_df['Efficiency']=succesful_Treated_df['Efficiency'].round(2)
succesful_Treated_df


# In[56]:


# Ploting effieciency of treatment plant

fig = px.bar(succesful_Treated_df.sort_values(by='Efficiency'),x='Efficiency',y='name',template='plotly_dark',color='Efficiency',text='Efficiency')
fig.update_layout(width=1000,title=dict(text='Efficiency of treatment plant' ,x=0.5))


# In[57]:


# KPI 5 : Identify Day Wise Activity of Treatment Plant
WstWtrtrt_TrtPlant_df


# In[58]:


Dayname_wise_activty = WstWtrtrt_TrtPlant_df.groupby(['name','Day Name'],as_index = False)['Volume of Water Treated'].sum()


# In[59]:


Dayname_wise_activty


# In[60]:


fig = px.line(Dayname_wise_activty,x='name',y='Volume of Water Treated',color = 'Day Name',template='plotly_dark')
fig.update_layout(width=900,title=dict(text='Day wise Activity of Treatment Plant',x = 0.5))

