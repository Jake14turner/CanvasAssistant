import streamlit as st




st.title("3444 project")



registerPage = st.Page("registerPage.py", title="Register Page", icon=":material/add_circle:")
loginPage = st.Page("loginPage.py", title="Login Page", icon=":material/delete:")
homePage = st.Page("homePage.py", title="Home Page", icon=":material/add_circle:")
toDoPage = st.Page("toDoPage.py", title="To Do Page", icon=":material/add_circle:")




pg = st.navigation([registerPage, loginPage, homePage, toDoPage])

pg.run()

