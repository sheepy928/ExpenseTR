import os

import streamlit as st

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

st.warning(
    "If any issues arise, please click the button below to kill the server. The server will restart automatically within 60 seconds. Note that data already entered will not be lost."
)

# Button with red background to kill the server
if st.button("Kill Server"):
    os._exit(0)