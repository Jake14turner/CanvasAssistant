import sqlite3 as sqlite3
import streamlit as st


def retreiveKey(username):

    connection = sqlite3.connect('streamlitBase')
    connect = connection.cursor()

    connect.execute('''SELECT key FROM users WHERE username = ?''', (username,))
    testToken = connect.fetchone()
    return testToken[0]



def insertUserTokenIntoDatabase(token, username):
     
    connection = sqlite3.connect('streamlitBase')
    connect = connection.cursor()




    connect.execute('''UPDATE users SET key = ? WHERE username = ? ''', (token, username))
    connection.commit()
    connect.execute('''SELECT key FROM users WHERE username = ?''', (username,))
    testToken = connect.fetchone()
    return testToken[0]

def registerUser(username, password):
       
    connection = sqlite3.connect('streamlitBase')
    connect = connection.cursor()


    #create the database if there are no users yet
    connect.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, key TEXT)''')
    connection.commit()

    try:
        connect.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("username already exists please try another one")
        return False

def loginUser(username, password):

    connection = sqlite3.connect('streamlitBase')
    connect = connection.cursor()


    connect.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    return connect.fetchone()