# COMS 6111 Project 3
# Authors
Yousef Elsendiony (ye2194) and Daniel Carpenter Silva (dcs2180)

# Files
Association_Mining.py
Create_Dataset.py
README.txt
example_run.txt
City_Events_by_Month_and_Zip.csv

# Execution Instructions
python3 Association_Mining.py "City_Events_by_Month_and_Zip.csv" 0.05 0.75

# Dependencies

- sudo apt-get update

- sudo apt-get python3-pip

- python3 -m pip install pandas



# Dataset

The aggrergated data set was created by counting the number of events that occurred per month, per zip code in NYC from the following sources... 

##DOB Permit Data
https://data.cityofnewyork.us/Housing-Development/DOB-Permit-Issuance/ipu4-2q9a

##Park Event Location Data
https://data.cityofnewyork.us/City-Government/NYC-Parks-Events-Listing-Event-Locations/cpcm-i88g

##Park Event Date Data
https://data.cityofnewyork.us/City-Government/NYC-Parks-Events-Listing-Event-Listing/fudw-fgrp

##DOB Complaint Data
https://data.cityofnewyork.us/Housing-Development/DOB-Complaints-Received/eabe-havv

##Eviction Data
https://data.cityofnewyork.us/City-Government/Evictions/6z8x-wfk4

##Car Crash data
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

The columns for each type of event were then broken out into 4 seperate binary columns corresponding to a range of event counts each representing approximately a quarter of the population. The final dataset only contains months and zipcodes that exist is all 6 orginal data sources. 

We believe this data set is compelling as it allows us t examine any assoiciations that may exist between the number of park events, evictions, DOB complaints, Cnstruction jobs, and car accidents for a given month and zip code in NYC.

An example of one assiociation that was found seems to suggest that a high number of construction jobs and building complaints corresponds to a higher number of car accidents in a given month + zip code in NYC
[construction_job_count(>135), building_complaint_count(>102)]=>[car_accident_count(>78)] (Conf: 85.2349%, Supp: 5.4181)

# Internal Design
The code scans through the dataset an collects all large itemsets that satifsy the input min support using the apriori algorithm. The for each large itemset the confidence of all possible associations containing one item on the right hand side. Associations that satisfy the input min confidence are then collected and sorted by confidence and the printed to an output.txt file


