#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[48]:


import pandas as pd


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[49]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values="Unknown")
df.head(5)


# In[50]:


df.columns = [c.replace(' ', '_') for c in df.columns]
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
# 
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*

# In[51]:


df.shape

# 81,937 rows


# In[52]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[ ]:


# The rows are answers to NYC dog liscence application questions 


# In[ ]:


# Animal Gender = M or F
# Vaccinated = Yes or No


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[ ]:


# 1. What percentage of dogs are vaccinated in NYC?
# 2. What percentage of dogs spayed or neutered in NYC?
# 3. What are the most dog friendly neighborhoods in NYC?
# 4. What is the most common breed in NYC?


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[53]:


df.Primary_Breed.value_counts().head(10)


# In[54]:


df.Primary_Breed.value_counts().head(10).plot()


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[55]:


df.Primary_Breed.value_counts().head(10).sort_values().plot(kind='barh')


# ## What are the most popular dog names?

# In[56]:


df.Animal_Name.value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[66]:


df[df.Animal_Name == 'Anthony'].Animal_Name.value_counts().sort_values(ascending=True)


# In[65]:


df[df.Animal_Name == 'Max'].Animal_Name.value_counts().sort_values(ascending=True)


# In[64]:


df[df.Animal_Name == 'Maxwell'].Animal_Name.value_counts().sort_values(ascending=True)


# ## What percentage of dogs are guard dogs?

# In[78]:


(df.Guard_or_Trained.value_counts(normalize=True) * 100).round(2)


# ## What are the actual numbers?

# In[79]:


df.Guard_or_Trained.value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[83]:


df.Guard_or_Trained.value_counts(dropna=False)


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[ ]:





# ## What are the top dog breeds for guard dogs? 

# In[86]:


df[df.Guard_or_Trained == 'Yes'].Primary_Breed.value_counts().sort_values(ascending=False)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[88]:


df['year'] = df['Animal_Birth'].apply(lambda birth: birth.year)
df.head()


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[89]:


df['age'] = 2022 - df['year'] 
df.head()


# In[92]:


df.age.mean().round(1)


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[134]:


join = pd.read_csv("zipcodes-neighborhoods.csv", na_values="unknown")
join.head()


# In[131]:


merged = df.merge(join, left_on='Owner_Zip_Code', right_on='zip')
merged.head(2)


# In[161]:


merged.neighborhood.value_counts(dropna=False)


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[132]:


merged[merged.neighborhood.str.contains("Bronx", na=False)].Animal_Name.value_counts()


# In[133]:


merged[merged.neighborhood.str.contains("Brooklyn", na=False)].Animal_Name.value_counts(dropna=False)


# In[123]:


merged[merged.neighborhood.str.contains("Upper East Side", na=False)].Animal_Name.value_counts()


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[152]:


merged.groupby(by='neighborhood').Primary_Breed.value_counts().sort_values(ascending=False)


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[ ]:





# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[158]:


df[(df.Animal_Dominant_Color == 'Black') | (df.Animal_Dominant_Color == 'Brown') | (df.Animal_Dominant_Color == 'grey')].Primary_Breed.value_counts()


# In[ ]:





# ## How many dogs are in each borough? Plot it in a graph.

# In[162]:


merged.borough.value_counts(dropna=False)


# In[165]:


merged.borough.value_counts(dropna=False).sort_values().plot(kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[234]:


pop = pd.read_csv("boro_population.csv")
pop


# In[272]:


boro_dogs = pd.DataFrame(merged.borough.value_counts(dropna=False))
boro_dogs

boro_dogs['index_column'] = boro_dogs.index

boro_dogs


# In[274]:


pop_merged = pop.merge(boro_dogs, left_on='borough', right_on='index_column')

pop_merged


# In[278]:


pop_merged['dogs_per_capita'] = (pop_merged['population']/pop_merged['borough_y']).round(2)

pop_merged


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.
