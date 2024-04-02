# %%
import numpy as np
import streamlit as st
import wave_extractor_NR500 as ex
# %%
def def_session_state():
    if 'data_origin' not in st.session_state:
        st.session_state['data_origin'] = []
    if 'df_st' not in st.session_state:
        st.session_state['df_st'] = []
    if 'df_ex' not in st.session_state:
        st.session_state['df_ex'] = []
    if 'filename' not in st.session_state:
        st.session_state['filename'] = []
    if 'sampling_rate' not in st.session_state:
        st.session_state['sampling_rate'] = 0
    if 'col_name' not in st.session_state:
        st.session_state['col_name'] = []
    if 'col_st' not in st.session_state:
        st.session_state['col_st'] = []
    if 'threshold' not in st.session_state:
        st.session_state['threshold'] = [0.5]
    if 'skip' not in st.session_state:
        st.session_state['skip'] = [0.3]
    if 'sensitivity' not in st.session_state:
        st.session_state['sensitivity'] = [500]
    if 'id_L' not in st.session_state:
        st.session_state['id_L'] = []
    if 'id_R' not in st.session_state:
        st.session_state['id_R'] = []
    if 'analyze' not in st.session_state:
        st.session_state['analyze'] = False
# %%
def reset():
    st.session_state['data_origin'] = []
    st.session_state['df_st'] = []
    st.session_state['df_ex'] = []
    st.session_state['filename'] = []
    st.session_state['sampling_rate'] = 0
    st.session_state['col_name'] = []
    st.session_state['col_st'] = []
    st.session_state['threshold'] = [0.5]
    st.session_state['skip'] = [0.3]
    st.session_state['sensitivity'] = [500]
    st.session_state['id_L'] = []
    st.session_state['id_R'] = []
    st.session_state['analyze'] = False
# %%
def upload():
    st.subheader('1. Upload csv')
    st.session_state['data_origin'] = st.file_uploader('Limit 500MB in total', accept_multiple_files = True, type = 'csv')
    if st.session_state['data_origin']:
        total = []
        for data_origin in st.session_state['data_origin']:
            size = data_origin.size
            total.append(size)
        total = sum(total) / 1e6
        total = np.round(total, decimals = 2)
        st.text(f'Total file size : {total} MB')      
# %%
def read_form():
    with st.form('read'):
        st.subheader('2. Read csv')
        st.session_state['sampling_rate'] = st.slider(
            label = 'Sampling Rate',
            min_value = int(0),
            max_value = int(100e3),
            value = int(100e2),
            step = int(1e3)
        )
        st.session_state['col_name'] = st.text_input(
        label = 'Columns Name',
        value = 'mic,acc_Z,acc_X,acc_Y,curr_Y,curr_spindle,curr_Z,curr_X',
        help = '列名をカンマ区切りで入力'
        )
        st.session_state['col_name'] = list(st.session_state['col_name'].split(','))
        st.session_state['col_st'] = st.text_input(
            label = 'Standard Column',
            help = '基準にする列名を入力',
            value = 'acc_X'
        )
        read_btn = st.form_submit_button('Read')
    return read_btn
# %%
def read():
    st.session_state['filename'] = []
    st.session_state['df_st'] = []
    st.session_state['threshold'] = [0.5] * len(st.session_state['data_origin'])
    st.session_state['skip'] = [0.3] * len(st.session_state['data_origin'])
    st.session_state['sensitivity'] = [500] * len(st.session_state['data_origin'])
    st.session_state['id_L'] = [0] * len(st.session_state['data_origin'])
    st.session_state['id_R'] = [0] * len(st.session_state['data_origin'])
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
    id_L, id_R, fig = ex.check(
    st.session_state['df_st'][file_id],
    st.session_state['threshold'][file_id],
    st.session_state['skip'][file_id],
    st.session_state['sensitivity'][file_id],
    st.session_state['filename'][file_id],
    )
    st.session_state['id_L'][file_id] = id_L
    st.session_state['id_R'][file_id] = id_R
    st.pyplot(fig)
    st.text(id_L)
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
            st.session_state['col_name'],
            st.session_state['id_L'][i],
            st.session_state['id_R'][i],
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
def sidebar():
    st.sidebar.header('5. Analyzing')
    data, name = select_data()
    show_csv_btn = st.sidebar.button('Show csv')
    if show_csv_btn:
        st.dataframe(data.head())
    st.sidebar.download_button(
    label = 'Download csv',
    data = data.to_csv(index = False).encode('utf-8'),
    file_name = f'{name}.csv',
    mime = 'text/csv',
    key = 'download'
    )
    analyze_mode = st.sidebar.selectbox('Analyze Mode', ['Show Wave', 'FFT', 'Filter'])
    return data, analyze_mode
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
