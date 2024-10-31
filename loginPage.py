import streamlit as st
import sqlite3 as sqlite3
import hashlib
from user import login

st.session_state.isLoggedIn = False
def loginPageView():
    
    
    #This is the responsiblity of the User component: we need to allow someone to log into an account 
    success = login()
    if success:
        st.session_state.isLoggedIn = True
    else:
        st.session_state.isLoggedIn = False



loginPageView()
