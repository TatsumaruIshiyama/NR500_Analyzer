#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
#%%
def binaly(data, threshold, b):
    data_bin = np.where(data < threshold, 0, data)
    data_bin = np.where(threshold <= data, 1, data_bin)
    data_bin = np.convolve(data_bin, b, mode = 'same')
    data_bin = np.where(0.01 <= data_bin, 1, data_bin)
    data_bin = data_bin.astype(dtype = 'int')
    return data_bin
#%%
def extract_df(data, col_name, col_st, threshold = 0.3, n_conv = 500):
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
        dfs_ex.append(df_ex)
    return dfs_ex, id_ex_L, id_ex_R, df, threshold
# %%
def plot_format(ax, xlim, ylim, fontsize = 15, flame_width = 1.5, scale_length = 5, pad = [0, 0], grid_width = 0.5):
    ax.spines["top"].set_linewidth(flame_width)
    ax.spines["left"].set_linewidth(flame_width)
    ax.spines["bottom"].set_linewidth(flame_width)
    ax.spines["right"].set_linewidth(flame_width)
    ax.minorticks_on()
    ax.tick_params(
        which = 'major',
        axis = 'y',
        direction = 'in',
        labelsize = fontsize,
        width = flame_width,
        length = scale_length,
        pad = pad[1]
        )
    ax.tick_params(
        which = 'minor',
        axis = 'y',
        direction = 'in',
        width = flame_width,
        length = scale_length * 0.7
        )
    ax.tick_params(
        which = 'major',
        axis = 'x',
        direction = 'in',
        labelsize = fontsize,
        width = flame_width,
        length = scale_length,
        pad = pad[0]
        )
    ax.tick_params(
        which = 'minor',
        axis = 'x',
        direction = 'in',
        width = flame_width,
        length = scale_length * 0.7
        )
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(ylim[0], ylim[1])
    ax.grid(color = 'black', linewidth = grid_width)
# %%
def show_wave(data, sampling_rate, axis):
    time = data.index * (1 / sampling_rate)
    xlim = time[-1]
    for i in range(len(axis)):
        data_plot = data[axis[i]]
        ylim = max(abs(data_plot)) * 1.1
        fig, ax = plt.subplots()   
        ax.plot(
            time,
            data_plot,
            c = 'black'
        )
        plot_format(
            ax,
            xlim = [0, xlim],
            ylim = [-ylim, ylim]
        )
        ax.set_title(axis[i])
        st.pyplot(fig)
# %%
