import requests
from pprint import pformat
import pandas as pd

station_id = "43t"
param = "PM25,PM10,O3,CO,NO2,SO2,WS,TEMP,RH,WD"

data_type = "hr"
start_date = "2023-01-01"
end_date = "2024-03-01"
start_time = "00"
end_time = "23"

url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
response = requests.get(url)
response_json = response.json()
# print(pformat(response_json))

pd_from_dict = pd.DataFrame.from_dict(response_json["stations"][0]["data"])
print(pformat(pd_from_dict))

# df = pd.DataFrame(pd_from_dict)
# column_null = ['PM25','CO','NO2','TEMP','RH']
# df1 = df[column_null] = df[column_null].fillna(df[column_null].mean().round(2))
# df1.insert(0, 'DATETIMEDATA', df['DATETIMEDATA'])
# condition = (df1[column_null] == 0).sum(axis=1) > 1
# df1.drop(df1[condition].index, inplace=True)
# df1["NO2"].replace(0, df1["NO2"].mean().round(2))
# df1.to_csv('HKT_clean.csv', index=True)

# df1[['Date', 'Time']] = df1['DATETIMEDATA'].str.split(' ', expand=True)
# df3 = df1.drop('DATETIMEDATA', axis=1)
# df3 = df1.groupby(['Date']).mean().round(2)
# df3.to_csv('mean_value_nai.csv', index=True)

df_train = pd.read_csv("HKT_clean.csv")
# Set data for predict next day
for i in range(len(df_train) - 1):
    df_train.loc[i, 'DAY1'] = df_train.loc[i+1, 'PM25']
df_train.loc[len(df_train) - 1, 'DAY1'] = float('nan')

# Set data for predict next 2 day
for i in range(len(df_train) - 2):
    df_train.loc[i, 'DAY2'] = df_train.loc[i+2, 'PM25']
df_train.loc[len(df_train) - 2, 'DAY2'] = float('nan')

# Set data for predict next 3 day
for i in range(len(df_train) - 3):
    df_train.loc[i, 'DAY3'] = df_train.loc[i+3, 'PM25']
df_train.loc[len(df_train) - 3, 'DAY3'] = float('nan')

print(df_train)