import streamlit as st
from user import initializeUserInfoJSON, sortUserDataIntoList


if 'isLoggedIn' not in st.session_state:
    st.session_state.isLoggedIn = False

def toDoView():
    username = st.session_state.username

    #this is the responsibility of the user component: we need to get the information from the API into the user
    data = initializeUserInfoJSON(username)


    #this is the responsibility of the user componenet: we need to organize that data into a list with class objects and assignment objects
    studentInfo = sortUserDataIntoList(data)


    l = 0
    for k in studentInfo:
        st.subheader(f"{k.name}")
        st.write("Assignments:")
        for j in studentInfo[l].assignmentList:
            st.text(f" - **Title**: {j.name}, **Due**: {j.dueDate}")
        l = l + 1


if st.session_state.isLoggedIn:
    toDoView()
else:
    st.text("Please log in to view To Do page.")

