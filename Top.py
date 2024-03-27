#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import wave_extractor_NR500 as ex
# %%
data = st.file_uploader('Upload csv', type = 'csv')
read_btn = st.button('Read')
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()
if 'df_ex' not in st.session_state:
    st.session_state['df_ex'] = []
if 'n_download' not in st.session_state:
    st.session_state['n_download'] = 0
if 'filename' not in st.session_state:
    st.session_state['filename'] = ''

if read_btn:
    st.session_state['df'] = pd.DataFrame()
    st.session_state['df_ex'] = []
    st.session_state['n_download'] = 0
    st.session_state['filename'] = data.name.replace('.csv', '')

    if data:
        st.session_state['df'] = pd.read_csv(
            data,
            skiprows = 70,
            skipfooter = 3,
            encoding = 'shift jis',
            engine = 'python'
        )
        st.session_state['df_ex'] = []
        st.session_state['n_download'] = 0
        st.dataframe(
            st.session_state['df'].head()
        )
    else:
        st.text('csvファイルをアップロードしてください')

with st.form('upload'):
    sampling_rate = st.slider(
            label = 'Sampling Rate',
            min_value = int(0),
            max_value = int(100e3),
            value = int(100e2),
            step = int(10e3)
            )
    col_name = st.text_input(
        label = 'Columns Name',
        value = 'mic,acc_Y,acc_Z,acc_X,curr_Y,curr_spindle,curr_Z,curr_X',
        help = '列名をカンマ区切りで入力'
    )
    col_st = st.text_input(
        label = 'Standard Column',
        help = '基準にする列名を入力',
        value = 'acc_X'
    )
    threshold = st.slider(
        label = 'Threshold',
        min_value = float(0),
        max_value = float(1),
        step = 0.05,
        value = 0.3
    )
    n_conv = st.number_input(
        label = 'Sensitivity',
        min_value = 10,
        step = 10,
        value = 500
    )
    n_conv = int(n_conv)
    extract_btn = st.form_submit_button(
        label = 'Extract'
    )

if extract_btn:
    st.session_state['n_download'] = 0
    st.session_state['df_ex'], id_L, id_R, df_plot, threshold_plot = ex.extract_df(
        st.session_state['df'].copy(),
        sampling_rate,
        col_name,
        col_st,
        threshold,
        n_conv
    )

    fig, ax = plt.subplots()
    ax.plot(
        df_plot.index,
        df_plot[col_st],
        c = 'black'
        )
    ax.hlines(
        y = threshold_plot,
        xmin = 0,
        xmax = df_plot.index[-1],
        color = 'red'
    )
    for i in range(len(st.session_state['df_ex'])):
        ax.plot(list(range(id_L[i], id_R[i])), st.session_state['df_ex'][i][col_st])
    st.pyplot(fig)

if st.session_state['df_ex']:
    if st.session_state['n_download'] == len(st.session_state['df_ex']):
        st.session_state['df'] = pd.DataFrame()
        st.session_state['df_ex'] = []
        st.session_state['n_download'] = 0
        st.subheader('alredy downloaded all files')
    else:
        i = st.session_state['n_download']
        st.sidebar.header(f'Wave No{i + 1}')
        with st.sidebar.form(key = 'fft'):
            st.sidebar.slider('test', 0, 1)
            st.sidebar.button('FFT')
        download_btn = st.sidebar.download_button(
            label = 'Download csv',
            data = st.session_state['df_ex'][i].to_csv(index = False).encode('utf-8'),
            file_name = f'{st.session_state['filename']}_ex{i + 1}.csv',
            mime = 'text/csv',
            key = 'download'
        )
        next_btn = st.sidebar.button('Next')
        if next_btn:
            print(i)
            st.session_state['n_download'] += 1
