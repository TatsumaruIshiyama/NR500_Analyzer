#%%
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import wave_extractor_NR500 as ex
import interface
# %%
if 'order' not in st.session_state:
    st.session_state['data_origin'] = 1
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
if 'analyze' not in st.session_state:
    st.session_state['analyze'] = False

st.title('NR500 Analyzer')
reset_btn = st.button(label = 'Reset')
if reset_btn:
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
    st.session_state['analyze'] = False
    mode = False
st.subheader('1. Upload csv')
st.session_state['data_origin'] = st.file_uploader('Limit 500MB in total', accept_multiple_files = True, type = 'csv')
if st.session_state['data_origin']:
    total = []
    for data_origin in st.session_state['data_origin']:
        size = data_origin.size
        total.append(size)
    total = sum(total)
    if total > 550e6:
        st.text('File size is too large')
st.session_state['sampling_rate'], st.session_state['col_name'], st.session_state['col_st'], read_btn = interface.read_form()
if read_btn:
    interface.read()
file_id, check_btn = interface.check_form()
if check_btn:
    interface.check(file_id)
extract_btn = interface.extract_form()
if extract_btn:
    interface.extract()
    st.session_state['analyze'] = True
if st.session_state['analyze'] and st.session_state['df_ex']:
    st.sidebar.header('5. Analyzing')
    data_select, name = interface.select_data()
    analyze_mode = interface.sidebar(data_select, name)
    interface.analyze(data_select, analyze_mode)