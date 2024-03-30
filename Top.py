#%%
import streamlit as st
import interface
# %%
st.title('NR500 Analyzer')
interface.def_session_state()
reset_btn = st.button(label = 'Reset')
if reset_btn:
    interface.reset()
interface.upload()
read_btn = interface.read_form()
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
    data_select, analyze_mode = interface.sidebar()
    interface.analyze(data_select, analyze_mode)