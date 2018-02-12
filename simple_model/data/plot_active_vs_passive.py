import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

# activate latex text rendering
rc('text', usetex=True)

df = pd.read_csv("dumb_vs_smart.csv", index_col=0, skiprows=1, names=[r"DS Node Depth (ft)-\textit{Active}", 
    r"DS Node Depth (ft)-\textit{Passive}", r"DS Node Flooding (cfs)-\textit{Passive}"])
df.reset_index(inplace=True)
df.set_index(df.index/12., inplace=True)
font_size = 12
ax = df.plot(fontsize=font_size, lw=3, legend=False)
lines = ax.lines
passive_color = "0.55"
lines[1].set_color(passive_color)
lines[2].set_color(passive_color)
lines[2].set_linestyle("--")
lgd = ax.legend(loc='lower left', bbox_to_anchor=(0, 1), ncol=1, fontsize=font_size)
ax.set_xlabel("Time elapsed (hr)", fontsize=font_size)
fig = plt.gcf()
fig.savefig("dumb_vs_smart",  bbox_inches="tight")

plt.show()