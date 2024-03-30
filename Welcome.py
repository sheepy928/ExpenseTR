import streamlit as st

import os
if os.environ.get("STREAMLIT_SERVER_DEBUG"):
    st.session_state['IS_DEBUG'] = True
else:
    st.session_state['IS_DEBUG'] = False
st.set_page_config(
    page_title="CS 348 Project",
    page_icon="👋",
)

st.write("# Welcome👋")

st.sidebar.success("Select a function above.")

st.markdown(
    """
    This is a simple web application that allows you to track your expenses.
"""
)