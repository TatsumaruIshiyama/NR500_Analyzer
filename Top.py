#%%
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import wave_extractor_NR500 as ex
import interface
# %%
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

st.title('NR500 Analyzer')
st.session_state['data_origin'] = st.file_uploader('Upload csv', accept_multiple_files = True, type = 'csv')
st.session_state['sampling_rate'], st.session_state['col_name'], st.session_state['col_st'], read_btn = interface.read_form()
if read_btn:
    st.session_state['filename'], st.session_state['df_st'] = interface.read()
mode, threshold, n_conv, extract_btn = interface.extract_form(st.session_state['filename'], st.session_state['data_origin'])
if extract_btn:
    st.session_state['df_ex'] = interface.extract(threshold, n_conv, mode)
if mode == 'Extract' and st.session_state['df_ex']:
    data_select, name = interface.select_data()
    analyze_mode = interface.sidebar(data_select, name)
    interface.analyze(data_select, analyze_mode)
reset_btn = st.button(label = 'Reset')
if reset_btn:
    st.session_state['data_origin'] = []
    st.session_state['df_st'] = []
    st.session_state['df_ex'] = []
    st.session_state['filename'] = []
    st.session_state['sampling_rate'] = 0
    st.session_state['col_name'] = []
    st.session_state['col_st'] = []
    mode = False