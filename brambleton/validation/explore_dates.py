import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
wz_df = pd.read_csv('waze_reports_area_data.csv', 
                    parse_dates=['file_dt', 'datetime'], 
                    infer_datetime_format=True, index_col='file_dt')
rn_df = pd.read_csv('hrsd_rain/MMPS-006_Aug062017_Jun012018.csv', 
                    parse_dates=[0], index_col=0, infer_datetime_format=True)
td_df = pd.read_csv('NOAA_Tide/MSL_Swells.csv', parse_dates=['Date Time'], 
                      index_col=0, infer_datetime_format=True)
wz_dts = np.unique(wz_df.index.date)
wz_dts.sort()
fig, ax = plt.subplots(nrows=2, ncols=3, sharey=True, figsize=(9,6))
axes = ax.ravel()
secondary_yax = []
for i, dt in enumerate(wz_dts):
    date = dt.strftime("%Y-%m-%d")
    rain_color = 'royalblue'
    rn = rn_df[date]
    cur_ax = axes[i]
    cur_ax.bar(rn.index, rn.iloc[:, 0], width=0.01, color=rain_color)
    cur_ax.set_xlim([rn.index[0], rn.index[-1]])
    cur_ax.xaxis.set_major_locator(mdates.HourLocator())
    cur_ax.set_title(date)
    cur_ax.tick_params('y', colors=rain_color)

    tide_color = 'sienna'
    td = td_df[date]
    ax2 = cur_ax.twinx()
    secondary_yax.append(ax2)
    ax2.get_shared_y_axes().join(*secondary_yax)
    ax2.plot(td.index, td.iloc[:, 0], c=tide_color)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    ax2.tick_params('y', colors=tide_color)

    wz = wz_df[date]
    for w in wz.index:
        cur_ax.axvline(x=w, alpha=0.1, linewidth=1, c='red')

plt.figtext(0, 0.5, "Rainfall (in)", rotation='vertical', color=rain_color)
plt.figtext(0.97, 0.5, "Tide (ft above MSL)", rotation='vertical', 
            color=tide_color)
plt.figtext(0.43, 0, "Hour of day", rotation='horizontal')
plt.tight_layout()
fig.subplots_adjust(left=0.1, right=0.9)
fig.delaxes(axes[-1])
plt.savefig('waze_storms_brambleton', dpi=300)
plt.show()

