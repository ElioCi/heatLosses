import streamlit as st



st.title("My forst app with pages")
st.header("first App")
st.subheader("firstApp")

st.markdown("---")

st.page_link("https://enginapps.it", label="Home", icon="🏠")
st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣", disabled=False)
st.page_link("http://www.google.com", label="Google", icon="🌎")


