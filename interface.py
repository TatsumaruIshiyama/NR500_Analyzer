# %%
import numpy as np
import pandas as pd
import streamlit as st
import wave_extractor_NR500 as ex
# %%
def read_form():
    with st.form('read'):
        st.subheader('2. Read csv')
        sampling_rate = st.slider(
            label = 'Sampling Rate',
            min_value = int(0),
            max_value = int(100e3),
            value = int(100e2),
            step = int(10e3)
        )
        col_name = st.text_input(
        label = 'Columns Name',
        value = 'mic,acc_Z,acc_X,acc_Y,curr_Y,curr_spindle,curr_Z,curr_X',
        help = '列名をカンマ区切りで入力'
        )
        col_name = list(col_name.split(','))
        col_st = st.text_input(
            label = 'Standard Column',
            help = '基準にする列名を入力',
            value = 'acc_X'
        )
        read_btn = st.form_submit_button('Read')
    return sampling_rate, col_name, col_st, read_btn
# %%
def read():
    st.session_state['filename'] = []
    st.session_state['df_st'] = []
    st.session_state['threshold'] = [0.5] * len(st.session_state['data_origin'])
    st.session_state['skip'] = [0.3] * len(st.session_state['data_origin'])
    st.session_state['sensitivity'] = [500] * len(st.session_state['data_origin'])
    for i in range(len(st.session_state['data_origin'])):   
        filename = st.session_state['data_origin'][i].name.replace('.csv', '')
        st.session_state['filename'].append(filename)
        st.session_state['df_st'].append(
            ex.read_standard(
            st.session_state['data_origin'][i],
            st.session_state['col_name'],
            st.session_state['col_st']
            )
        )
    st.text('Reading Completed')
# %%
def check_form():
    with st.form('check'):
        st.subheader('3. Check extraction')
        file = st.selectbox(
            'File',
            st.session_state['filename']
        )
        threshold = st.slider(
            label = 'Threshold',
            min_value = float(0),
            max_value = float(1),
            step = 0.02,
            value = 0.5,
        )
        skip = st.slider(
            'Skip',
            min_value = float(0),
            max_value = float(1),
            step = 0.02,
            value = 0.3
        )
        n_conv = st.slider(
            label = 'Sensitivity',
            min_value = int(100),
            max_value = int(2000),
            step = int(100),
            value = int(500)
        )
        file_id = 0
        if st.session_state['filename']:
            file_id = st.session_state['filename'].index(file)
        st.session_state['threshold'][file_id] = threshold
        st.session_state['skip'][file_id] = skip
        st.session_state['sensitivity'][file_id] = n_conv
        check_btn = st.form_submit_button('Check')
    return file_id, check_btn
# %%
def check(file_id):
    ex.extract_df(
    st.session_state['data_origin'][file_id],
    st.session_state['df_st'][file_id],
    st.session_state['col_name'],
    st.session_state['threshold'][file_id],
    st.session_state['skip'][file_id],
    st.session_state['sensitivity'][file_id],
    st.session_state['filename'][file_id],
    'Check'
    )
# %%
def extract_form():
    with st.form('extract'):
        st.subheader('4. Extraction')
        extract_btn = st.form_submit_button(label = 'Extract')
    return extract_btn
# %%
def extract():
    st.session_state['df_ex'] = []
    for i in range(len(st.session_state['df_st'])):  
        df_ex = ex.extract_df(
            st.session_state['data_origin'][i],
            st.session_state['df_st'][i],
            st.session_state['col_name'],
            st.session_state['threshold'][i],
            st.session_state['skip'][i],
            st.session_state['sensitivity'][i],
            st.session_state['filename'][i],
            'Extract'
        )
        st.session_state['df_ex'].append(df_ex)
    st.text('Extraction Completed')
# %%
def select_data():
    n_data = st.sidebar.selectbox(
        'Select data',
        st.session_state['filename']
    )
    n_data = st.session_state['filename'].index(n_data)
    n_wave = np.array(range(len(st.session_state['df_ex'][n_data]))) + 1
    n_wave = st.sidebar.selectbox(
        'Select wave No',
        n_wave
    )
    n_wave -= 1
    data = st.session_state['df_ex'][n_data][n_wave]
    data_name = st.session_state['filename'][n_data]
    name = f'{data_name}_ex{n_wave + 1}'
    st.sidebar.header(f'Wave No. {data_name}-{n_wave + 1}')
    return data, name
# %%
def sidebar(data, name):
    show_csv_btn = st.sidebar.button('Show csv')
    if show_csv_btn:
        st.dataframe(data.head())
    download_btn = st.sidebar.download_button(
    label = 'Download csv',
    data = data.to_csv(index = False).encode('utf-8'),
    file_name = f'{name}.csv',
    mime = 'text/csv',
    key = 'download'
    )
    analyze_mode = st.sidebar.selectbox('Analyze Mode', ['Show Wave', 'FFT', 'Filter'])
    return analyze_mode
# %%
def analyze(data, analyze_mode):
    if analyze_mode == 'Show Wave':
        axis_wave = st.sidebar.multiselect(
            'Select axis',
            options = sorted(data.columns.values),
            key = 'show_wave'
        )
        show_wave_btn = st.sidebar.button('Show Wave')
        if show_wave_btn:
            ex.show_wave(data, st.session_state['sampling_rate'], axis_wave)
    if analyze_mode == 'FFT':
        axis_fft = st.sidebar.multiselect(
            'Select axis',
            options = sorted(data.columns.values),
            key = 'FFT'
        )
        peak = st.sidebar.radio('Show peak', [True, False], horizontal = True)
        peak_sense = st.sidebar.number_input(
            'sensitivity',
            0,
            100,
            value = 10
        )
        fft_btn = st.sidebar.button('FFT')
        if fft_btn:
            ex.show_FFT(data, st.session_state['sampling_rate'], axis_fft, peak, peak_sense)
    if analyze_mode == 'Filter':
        axis_filter = st.sidebar.selectbox(
            'Select axis',
            options = sorted(data.columns.values),
            key = 'filter'
        )
        type = st.sidebar.radio(
            'Select type',
            ['low', 'high', 'band'],
            horizontal = True
        )
        pass_value = int(st.session_state['sampling_rate'] / 4)
        if type == 'band':
            pass_value = [pass_value - 500, pass_value + 500]
        fp = st.sidebar.slider(
            'Pass frequency',
            min_value = int(0),
            max_value = int(st.session_state['sampling_rate'] / 2),
            value = pass_value,
            step = int(100),
            help = '通過域端周波数'
        )
        fs = st.sidebar.slider(
        'Stop frequency',
        min_value = int(0),
        max_value = int(st.session_state['sampling_rate'] / 2),
        value = pass_value,
        step = int(100),
        help = '阻止域端周波数'
        )
        filt_btn = st.sidebar.button('Filter')
        if filt_btn:
            data_filt = ex.filter(data[axis_filter],
                                    st.session_state['sampling_rate'],
                                    type,
                                    fp,
                                    fs
            )
            ex.show_filter(data,
                            data_filt,
                            st.session_state['sampling_rate'],
                            axis_filter
            )