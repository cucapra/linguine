import matplotlib.patches as mpatches
import scipy.stats
import json
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os.path

FILE_NAME = 'data/run.json'
if len(sys.argv) > 1:
    FILE_NAME = sys.argv[1]
FILE_NAME = os.path.normpath(FILE_NAME)
data = json.load(open(FILE_NAME))
df1 = pd.DataFrame(data)
df = pd.DataFrame([(d, *(tup[1:])) for tup in df1.itertuples()
                   for d in tup.fpsData])
df.columns = ['frame'] + list(df1.columns)
bench_names = list(set(list(df['bench_name'])))
for bench in bench_names:
    data_raw = df.loc[(df['shader'] == 'raw') & (
        df['bench_name'] == bench)]['frame']
    data_default = df.loc[(df['shader'] ==
                           'default') & (df['bench_name'] == bench)]['frame']
    data_raw, data_default = list(data_raw), list(data_default)
    diff = []
    for i in range(len(data_raw)):
        diff.append(data_raw[i] - data_default[i])

    print(bench)
    print(f"Means \n GLSL: {np.mean(data_raw)} Gator: {np.mean(data_default)}")
    print(f" Ttest : {scipy.stats.ttest_ind(data_raw, data_default).pvalue}")
    print(f" Wilcox: {scipy.stats.wilcoxon(data_raw, data_default).pvalue}")
    print(f" diff  : mean {np.mean(diff):.2f}, std {np.std(diff):.2f} "
          f" stderr {scipy.stats.sem(diff):.2f}")
    low = -.1
    upp = .1
    pv1 = scipy.stats.ttest_1samp(diff, low).pvalue
    pv2 = scipy.stats.ttest_1samp(diff, upp).pvalue
    print(f" TOST  : {max(pv1,pv2) / 2.:.2f} (pv1={pv1:.2f}, pv2={pv2:.2f})")
    print('---------')

# PLOT_TYPE = "bar"
# if PLOT_TYPE == "violin":
#     fig, ax = plt.subplots()
#     sns.violinplot(
#         ax=ax, data=df.loc[df['shader'] == 'default'], x="frame", y="bench_name", color='red')
#     sns.violinplot(
#         ax=ax, data=df.loc[df['shader'] == 'raw'], x="frame", y="bench_name", color='blue')
#     plt.setp(ax.collections, alpha=.3)
#     red_patch = mpatches.Patch(color='red', label='default')
#     blue_patch = mpatches.Patch(color='blue', label='raw')

#     plt.legend(handles=[blue_patch, red_patch])
#     plt.show()
# elif PLOT_TYPE == "bar":
#     fig, ax = plt.subplots()
#     g = sns.barplot(x="bench_name", y="frame",
#                     data=df, hue="shader", ci="sd", ax=ax, hue_order=["default", "raw"])
#     L = ax.legend()
#     L.get_texts()[0].set_text('Lathe')
#     L.get_texts()[1].set_text('GLSL')
#     plt.xlabel('Shader')
#     plt.ylabel('fps')

#     plt.show()
