#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%%
def binaly(data, threshold, b):
    data_bin = np.where(data < threshold, 0, data)
    data_bin = np.where(threshold <= data, 1, data_bin)
    data_bin = np.convolve(data_bin, b, mode = 'same')
    data_bin = np.where(0.01 <= data_bin, 1, data_bin)
    data_bin = data_bin.astype(dtype = 'int')
    return data_bin
#%%
def extract_df(data, sampling_rate, col_name, col_st, threshold = 0.3, n_conv = 500):
    sampling_time = 1 / sampling_rate
    col_name = col_name.split(',')

    df = data.copy()
    df = df.drop(
        columns = [
            '#EndHeader',
            '日時(μs)'
        ]
    )
    df = df.set_axis(
        labels = col_name,
        axis = 'columns'
    )

    n_data = len(df)
    n_conv = int(n_data / n_conv)
    b = np.ones(n_conv)/n_conv
    data_st = df.loc[:, col_st].values
    data_calc = data_st.copy()
    data_calc = abs(data_calc)
    threshold *= max(data_calc)

    data_bin_R = np.flip(data_calc)
    data_bin_L = binaly(data_calc, threshold, b)
    data_bin_R = binaly(data_bin_R, threshold, b)

    id_ex_L = np.diff(data_bin_L)
    id_ex_L = np.where(id_ex_L == 1)[0]
    id_ex_R = np.diff(data_bin_R)
    id_ex_R = np.where(id_ex_R == 1)[0]
    id_ex_R = n_data - id_ex_R
    id_ex_R = np.flip(id_ex_R)
    dfs_ex = []
    for i in range(len(id_ex_L)):
        df_ex = df.iloc[
            id_ex_L[i]:id_ex_R[i],
            :
        ]
        df_ex = df_ex.reset_index(drop = True)
        # df_ex['time'] = df_ex.index.values * sampling_time
        dfs_ex.append(df_ex)
    return dfs_ex, id_ex_L, id_ex_R, df, threshold