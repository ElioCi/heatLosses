import streamlit as st

st.session_state

extDia = st.session_state['extDia']
thk = st.session_state['thk']
intDia = st.session_state['intDia']

st.write("Page 2")

st.title("Results")
st.markdown("---")

st.markdown("<h3 style='text-align: Left;'>Results </h3>", unsafe_allow_html=True)
st.markdown("---")
# st.write("Selected Dia = ", DN, '"')
st.write("External Dia =", extDia, "mm")
st.write("Thikness =", thk, "mm")
st.write("Internal Dia =", intDia, "mm")
