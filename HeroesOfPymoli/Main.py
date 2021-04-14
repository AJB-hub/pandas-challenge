#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

purchase_data.tail(5)


# ### Player Count

# Display the total number of players
# 

# In[2]:


# Pass the unique elements in "SN" series to len to get number of elements
uniquePlayers = len(pd.unique(purchase_data["SN"]))

print(f'{uniquePlayers} players.')


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


#pass the unique elements in "item id" to len for a count of unique elements
uniqueItems = len(pd.unique(purchase_data['Item ID']))

# pass mean method to price series
averagePrice = purchase_data['Price'].mean()

# number of elements/rows in the dataframe
totalPurchases = len(purchase_data['Price'])

# sum of price data from dataframe
totalRevenue = purchase_data['Price'].sum()

# construct a dataframe that takes the above calculations and makes them readable
summary_df = pd.DataFrame(
    {
        'Unique Items': uniqueItems,
        'Average Price': averagePrice,
        'Total Purchases': totalPurchases,
        'Total Revenue': totalRevenue
    },
    index=range(0,1)
)

# format the column data to be more readable
format_mapping = {"Average Price": "${:,.2f}","Total Revenue": "${:,.2f}"}

summary_df.style.format(format_mapping)


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


# Construct 3 new dataframes based on the possible gender options
male_df = purchase_data[purchase_data["Gender"]=="Male"]

female_df = purchase_data[purchase_data["Gender"]=="Female"]

other_df = purchase_data[(purchase_data["Gender"]!="Female")&(purchase_data["Gender"]!="Male")]


# In[5]:


# Define a function that calculates a percent of purchases for the item passed
def percent(count):
    percent = round(100 * (count / int(totalPurchases)),2)
    return percent


# In[6]:


# DataFrame with percentages and count of each gender option
genderDemo = pd.DataFrame(
    {
        "Percentage": [
            percent(len(male_df)),
            percent(len(female_df)),
            percent(len(other_df))
        ],
        "Count": [
            len(male_df),
            len(female_df),
            len(other_df)
        ]
    }, index = ["Male","Female","Other"]
)

genderDemo["Percentage"] = genderDemo["Percentage"].map("{:,.2f}%".format)
genderDemo


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[7]:


# Dataframe with price data from each gender dataframe
genderSummary = pd.DataFrame(
    {
        "Purchase Count": [ #how many purchases per gender option
            len(female_df),
            len(male_df),
            len(other_df)
                          ],
        "Average Purchase": [ 
            female_df["Price"].mean(),
            male_df["Price"].mean(),
            other_df["Price"].mean()
                            ],
        "Total Purchase Value": [
            female_df["Price"].sum(),
            male_df["Price"].sum(),
            other_df["Price"].sum()
                                ],
        "Average Purchase Total per Person": [ #for each person, find out how much they spent, then find the average for everyone
            female_df.groupby(["SN"])["Price"].sum().mean(),
            male_df.groupby(["SN"])["Price"].sum().mean(),
            other_df.groupby(["SN"])["Price"].sum().mean()
        ]
        
    }, index=['female','male','other'] 
)                               


# In[8]:


# Formatting to prettify 
genderSummary['Average Purchase'] = genderSummary['Average Purchase'].map("${:,.2f}".format)
genderSummary['Average Purchase Total per Person'] = genderSummary['Average Purchase Total per Person'].map("${:,.2f}".format)
genderSummary['Total Purchase Value'] = genderSummary['Total Purchase Value'].map("${:,.2f}".format)
genderSummary
              


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[9]:


# Creates the bin based on the dataframe series and chosen bin size
def binConstructor(dataframe, series, bins=4):
    minSeries = dataframe[series].min() -1
    maxSeries = dataframe[series].max() +1
    dataRange = maxSeries - minSeries
    output = [minSeries]
    for i in range(1,bins+1):
        point = i*(dataRange/bins) + minSeries
        output.append(point)
        
    return output

   
binAge = binConstructor(purchase_data,"Age",8)


# In[10]:


# Appends a bin column to the dataframe 
age_df = purchase_data
age_df["Bin"] = pd.cut(age_df["Age"],binAge) 
binned_df = age_df.groupby(age_df["Bin"])


# In[11]:


# Count the number of purchases in each age bin
player_count = age_df["Bin"].value_counts()

# dataframe to display count and percent of purchases in each bin
demo_final = pd.DataFrame(
    {
        "Player Count": player_count,
        "Percentage": 100 * player_count / player_count.sum(),
    }
)


# In[12]:


# Format to percent
demo_final["Percentage"] = demo_final["Percentage"].map("{:,.2f}%".format)
demo_final


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[13]:


# creates a new dataframe with data grouped by age demographic
purchases_df = pd.DataFrame(
    {
        "Purchase Count": age_df["Bin"].value_counts(),
        "Average Purchase Price":binned_df["Price"].mean(),
        "Total Purchase Value":binned_df["Price"].sum(),
        "Average Purchase Total":binned_df["Price"].sum() / age_df["Bin"].value_counts()
    },
    index = pd.unique(age_df["Bin"])
)


# In[14]:


# Dataframe formatting
format_mapping = {
    "Average Purchase Price": "${:,.2f}",
    "Total Purchase Value": "${:,.2f}",
    "Average Purchase Total":"${:,.2f}"
}
purchases_df.style.format(format_mapping)


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[15]:


# Remove the bin column as it is not needed anymore
purchase_data = purchase_data.drop(columns="Bin")


# In[16]:


# create a dataframe which shows purchase count, avg price, and total price by SN
topSpender_df = pd.DataFrame(
    {
        "Purchase Count": purchase_data["SN"].value_counts(),
        "Average Purchase Price": purchase_data.groupby("SN")["Price"].mean(),
        "Total Purchase Value": purchase_data.groupby("SN")["Price"].sum()
    }
)


# In[17]:


# Formatting and sorting dataframe
format_mapping = {
    "Average Purchase Price": "${:,.2f}",
    "Total Purchase Value": "${:,.2f}"
}
topSpender_df.sort_values(by="Total Purchase Value",ascending=False).head(5).style.format(format_mapping)


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, average item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[ ]:


# Reduce the size of df to what is needed
item_id = purchase_data[["Item ID","Item Name","Price"]]
# group by id and name
item_group = item_id.groupby(["Item ID","Item Name"])

itemCount = item_id.groupby("Item ID")["Item Name"].value_counts()
itemPrice = item_group["Price"].mean()
itemTotal = itemCount * itemPrice


# In[150]:


# Construct dataframe
popular_df = pd.DataFrame(
    {
        "Purchase Count": itemCount,
        "Item Price": itemPrice,
        "Total Purchase Value": itemTotal 
    }
)


# In[153]:


# Formatting and sorting of df
format_mapping = {
    "Item Price": "${:,.2f}",
    "Total Purchase Value": "${:,.2f}"
}

popular_df.sort_values("Purchase Count",ascending=False).head(5).style.format(format_mapping)


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[158]:


popular_df.sort_values("Total Purchase Value",ascending=False).head(5).style.format(format_mapping)

