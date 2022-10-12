#!/usr/bin/env python
# coding: utf-8

# ## Libraries Used

# - First we need to install the library that will help us use SQL dialect on a pandas data frame - pandasql

# In[2]:


#!pip install pandasql


# In[3]:


import pandas as pd
from pandasql import sqldf


# ## Loading the data

# In[9]:


path = 'https://raw.githubusercontent.com/doronk28/SQL-flights/main/airlines.csv'
airlines = pd.read_csv(path)

airlines.info()


# In[18]:


path = 'https://raw.githubusercontent.com/doronk28/SQL-flights/main/airports.csv'
airports = pd.read_csv(path)

airports.info()


# In[24]:


path = 'https://raw.githubusercontent.com/doronk28/SQL-flights/main/flights.csv'
flights = pd.read_csv(path)

flights.info()


# In[15]:


path = 'https://raw.githubusercontent.com/doronk28/SQL-flights/main/models.csv'
models = pd.read_csv(path)

models.info()


# In[154]:


path = 'https://raw.githubusercontent.com/doronk28/SQL-flights/main/passengers.csv'
passengers = pd.read_csv(path)

passengers.info()


# In[155]:


path = 'https://raw.githubusercontent.com/doronk28/SQL-flights/main/planes.csv'
planes = pd.read_csv(path)

planes.info()


# ### Show all records in the airlines table

# In[156]:


query = """
SELECT 
    *
FROM 
    airlines
        """
sqldf(query)


# In[157]:


airlines


# In[158]:


airports


# In[159]:


flights


# ### Show the amount of flights per airline that went out of LAX (please show the full name of the airline)

# In[160]:


query = """
SELECT 
    airline, count(airline) count_al
FROM 
    flights 
WHERE origin_airport = 'LAX'
GROUP BY
    1
        """
sqldf(query)


# In[161]:


flights.query("ORIGIN_AIRPORT == 'LAX'").groupby('AIRLINE').size()


# In[162]:


#code to join tables on pandas
###airline_flight = airlines.merge(flights, left_on='AL_ID', right_on = 'AIRLINE')


# In[163]:


###airline_flight.head()


# In[ ]:





# ### For each day, show the average delay in departure per airline

# In[164]:


query = """
SELECT 
    Day, AVG(departure_delay)
FROM 
    flights
GROUP BY
    1
        """
sqldf(query)


# In[165]:


flights.groupby('DAY').agg({'DEPARTURE_DELAY':'mean'})


# ### What is the share of each cancellation reason for flights started on the first week of May 2015?

# In[ ]:





# In[166]:


flights.query('YEAR == 2015 and MONTH == 5 and 1<= DAY <=7').groupby('CANCELLATION_REASON').size()


# In[167]:


#or
flights[(flights['YEAR'] == 2015) & (flights['MONTH'] == 5) & (flights['DAY'].between(1,7))].groupby('CANCELLATION_REASON').size()


# ### Rank the cities by amount of flights (not canceled) in descending order (first rank with the most flights)

# In[168]:


query = """
SELECT 
    a.city, COUNT(*)
FROM 
    airports a
JOIN 
    flights f
ON a.AP_ID = f.origin_airport
WHERE 
    f.cancelled = 0
GROUP BY 1
ORDER BY 2 DESC
        """
sqldf(query)


# In[169]:


joined_df = airports.merge(flights, left_on='AP_ID', right_on='ORIGIN_AIRPORT')


# In[170]:


filt = joined_df['CANCELLED'] == 0
joined_df = joined_df[filt]


# In[171]:


joined_df.groupby('CITY').size().sort_values(ascending=False)


# ### Rank the cities by amount of flights that were not canceled in descending order and show the 3rd city
# Bonus: show the top 10 cities without the first 2

# In[172]:


query = """
SELECT 
    a.city, COUNT(*)
FROM 
    airports a
JOIN 
    flights f
ON a.AP_ID = f.origin_airport
WHERE 
    f.cancelled = 0
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1
offset 2

        """
sqldf(query)


# In[173]:


## Bonus: show the top 10 cities without the first 2


# In[174]:


query = """
SELECT 
    a.city, COUNT(*)
FROM 
    airports a
JOIN 
    flights f
ON a.AP_ID = f.origin_airport
WHERE 
    f.cancelled = 0
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
offset 2

        """
sqldf(query)


# In[175]:


df = joined_df.groupby('CITY').agg({'AIRPORT': 'count'}).sort_values(by='AIRPORT', ascending=False)
df.iloc[2:12]


# ## Write a Python function for the following!

# ### Show all the records for passengers older then X

# In[176]:


def passengers_above(age):
    return passengers.query('AGE > @age')


# In[177]:


passengers_above(70)


# ### Show gender distribution for passengers older then X

# In[178]:


def get_gender_dist(age):
    df = passengers_above(age)
    return df['GENDER'].value_counts()


# In[179]:


get_gender_dist(70)


# In[ ]:




