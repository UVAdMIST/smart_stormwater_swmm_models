import pandas as pd
import csv
import sys

def format_output_ts(df, name, date):
    dt_df = df[date]
    dt_df = dt_df.iloc[:, [0]]
    dt_df.columns=[name]
    dt_df['dt'] = dt_df.index.strftime("%m/%d/%Y")
    dt_df['time'] = dt_df.index.strftime("%H:%M:%S")
    dt_df[['dt', 'time', name]].to_csv('{}_{}.csv'.format(name, date), 
                                       sep=' ', index=False, header=False)

date = sys.argv[1]

wz_df = pd.read_csv('waze_reports_area_data.csv', 
                    parse_dates=['file_dt', 'datetime'], 
                    infer_datetime_format=True, index_col='file_dt')
rn_df = pd.read_csv('hrsd_rain/MMPS-006_Aug062017_Jun012018.csv', 
                    parse_dates=[0], index_col=0, infer_datetime_format=True)
td_df = pd.read_csv('NOAA_Tide/MSL_Swells.csv', parse_dates=['Date Time'], 
                      index_col=0, infer_datetime_format=True)


t = format_output_ts(rn_df, 'rain', date)
format_output_ts(td_df, 'tide', date)


