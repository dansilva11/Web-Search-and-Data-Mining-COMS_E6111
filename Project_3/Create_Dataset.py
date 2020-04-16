import pandas as pd

# dob_perm_df = pd.read_csv(r"DOB_Permit_Issuance.csv")[['Job Start Date','Zip Code']].dropna()
# dob_perm_df['Job Start Date'] = dob_perm_df['Job Start Date'].str[:10]
# dob_perm_df = dob_perm_df[dob_perm_df["Job Start Date"].str[-4:].astype(int)< 2021]
# dob_perm_df = dob_perm_df[dob_perm_df["Job Start Date"].str[-4:].astype(int)> 1920]
# dob_perm_df['month_year'] = pd.to_datetime(dob_perm_df['Job Start Date']).dt.to_period('M')
# dob_perm_df = dob_perm_df.groupby(['month_year','Zip Code']).agg('count').reset_index().rename(columns={"Job Start Date": "dob_job_count", 'Zip Code':'zip'})[['month_year','zip','dob_job_count']]
# dob_perm_df.to_csv("DOB_Permit_processed.csv")

dob_perm_df = pd.read_csv(r"DOB_Permit_processed.csv")
dob_perm_df.drop(columns=['Unnamed: 0'], inplace=True)

# crash_df = pd.read_csv(r"Motor_Vehicle_Collisions_-_Crashes.csv")[['CRASH DATE','ZIP CODE']]
# crash_df['month_year'] = pd.to_datetime(crash_df['CRASH DATE']).dt.to_period('M')
# crash_df = crash_df.groupby(['month_year','ZIP CODE']).agg('count').reset_index().rename(columns={"CRASH DATE": "crash_count", 'ZIP CODE':'zip'})[['month_year','zip','crash_count']]
# crash_df.to_csv("Crashes_processed.csv")
#
crash_df = pd.read_csv(r"Crashes_processed.csv")
crash_df.drop(columns=['Unnamed: 0'], inplace=True)

# dob_comp_df = pd.read_csv(r"DOB_Complaints_Received.csv")[['Date Entered','ZIP Code']]
# dob_comp_df['month_year'] = pd.to_datetime(dob_comp_df['Date Entered']).dt.to_period('M')
# dob_comp_df = dob_comp_df.groupby(['month_year','ZIP Code']).agg('count').reset_index().rename(columns={"Date Entered": "dob_complaint_count", 'ZIP Code':'zip'})[['month_year','zip','dob_complaint_count']]
# dob_comp_df.to_csv("DOB_Complaints_processed.csv")

dob_comp_df = pd.read_csv(r"DOB_Complaints_processed.csv")
dob_comp_df.drop(columns=['Unnamed: 0'], inplace=True)

# evictions_df = pd.read_csv(r"Evictions.csv")[['EXECUTED_DATE','EVICTION_ZIP']]
# evictions_df['month_year'] = pd.to_datetime(evictions_df['EXECUTED_DATE']).dt.to_period('M')
# evictions_df = evictions_df.groupby(['month_year','EVICTION_ZIP']).agg('count').reset_index().rename(columns={"EXECUTED_DATE": "eviction_count", 'EVICTION_ZIP':'zip'})[['month_year','zip','eviction_count']]
# evictions_df.to_csv("Evictions_processed.csv")
#
evictions_df = pd.read_csv(r"Evictions_processed.csv")
evictions_df.drop(columns=['Unnamed: 0'], inplace=True)

# df1 = pd.read_csv(r"NYC_Parks_Events_Listing___Event_Listing.csv")
# df2 = pd.read_csv(r"NYC_Parks_Events_Listing___Event_Locations.csv")
#
# event_df = df1.merge(df2,on='event_id')[['event_id','date','zip']].dropna()
# event_df['month_year'] = pd.to_datetime(event_df['date']).dt.to_period('M')
# park_event_df = event_df.groupby(['month_year','zip']).agg('count').reset_index().rename(columns={"event_id": "park_event_count"})[['month_year','zip','park_event_count']]
# park_event_df.to_csv("Park_Events_processed.csv")

park_event_df = pd.read_csv(r"Park_Events_processed.csv")
park_event_df.drop(columns=['Unnamed: 0'], inplace=True)

park_event_df.dropna(inplace=True)
dob_comp_df.dropna(inplace=True)
evictions_df.dropna(inplace=True)

dob_perm_df.dropna(inplace=True)

park_event_df['zip'] = park_event_df['zip'].astype(int)
dob_comp_df = dob_comp_df[dob_comp_df['zip'].str.isdigit()]

dob_comp_df['zip'] = dob_comp_df['zip'].astype(int)

evictions_df['zip'] = evictions_df['zip'].astype(int)

# crash_df['zip'] = crash_df['zip'].astype(float)
crash_df['zip'] = pd.to_numeric(crash_df['zip'],errors='coerce')
crash_df.dropna(inplace=True)
crash_df['zip'] = crash_df['zip'].astype(int)

dob_perm_df['zip'] = dob_perm_df['zip'].astype(int)

out_df = park_event_df.merge(evictions_df, on=['month_year','zip'], how='inner')
out_df = out_df.merge(dob_comp_df, on=['month_year','zip'], how='inner')
out_df = out_df.merge(dob_perm_df, on=['month_year','zip'], how='inner')
out_df = out_df.merge(crash_df, on=['month_year','zip'], how='inner')
out_df.rename(columns={"crash_count":"car_accident_count","dob_job_count":"construction_job_count",
                       "dob_complaint_count":"building_complaint_count","park_event_count":"park_n_rec_event_count"}, inplace=True)
for col in out_df.columns:
    if col in ['month_year','zip']:
        continue

    # print(col)
    out_df[col] = out_df[col].astype(int)
    if col == 'park_n_rec_event_count':
        interval =  int(out_df[col].max()/50)
    else:
        interval =  int(out_df[col].max()/10)



    for x in range(1,4):
        if x==1:
            low = interval*(x-1)
        else:
            low = interval * (x - 1) + 1
        high = interval*x
        out_df[col+"("+str(low)+"-"+str(high)+")"]=((out_df[col]>=low)&(out_df[col]<=high)).astype(int)
    out_df[col + "(>" + str(high) + ")"] = (out_df[col] > high).astype(int)
    out_df.drop(columns=[col], inplace=True)
out_df.to_csv("City_Events_by_Month_and_Zip.csv", index=False)

