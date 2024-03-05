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
df = pd.DataFrame(pd_from_dict)
column_null = ['PM25','CO','NO2','TEMP','RH','WD']
df1 = df[column_null] = df[column_null].fillna(df[column_null].mean().round(2))
df1.insert(0, 'DATETIMEDATA', df['DATETIMEDATA'])
condition = (df1[column_null] == 0).sum(axis=1) > 1
df1.drop(df1[condition].index, inplace=True)
df1["NO2"].replace(0, df1["NO2"].mean().round(2))

print(pformat(df1))
df1.to_csv('Test1.csv', index=True)

#pd_from_dict.to_csv(f"air4thai_{station_id}_{start_date}_{end_date}.csv")
