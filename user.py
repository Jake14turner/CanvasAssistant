import requests
import streamlit as st
import json
from database import retreiveKey, insertUserTokenIntoDatabase, registerUser, loginUser

class Assignment:
    def __init__(self, name, dueDate):
        self.name = name
        self.dueDate = dueDate

class Class:
    def __init__(self, name, assignmentList):
        self.name = name
        self.assignmentList = assignmentList


#####     This function is to access the users assignments and return them to UI in JSON form     #####
def initializeUserInfoJSON(username):
    #courseIDList, courseNameList, studentInfo, username
    courseIDList = []
    courseNameList =  []
    studentInfo = []

   #This is the database component's responsiblity: We need to retreive the key from the database
    testToken = retreiveKey(username)

    #define the link for the api
    apiLink = 'https://canvas.instructure.com/api/v1'

    #define headers for authentication
    headers = {
    'Authorization': f'Bearer {testToken}'
    }

    data = {"courses": []}

    #now generate the actual link to access the api endpoint we want, right here we are accesing courses
    #just append the endpointe "courses" to the root link
    link = f'{apiLink}/courses'

    #now print out all courses
    while link:
        #define the response using the requests tool
        response = requests.get(link, headers=headers)
        #check if the request receives an approriate response
        if response.status_code == 200:
            #take in the response in json form and put it into the var courses. 
            courses = response.json()
            #loop through each course in the response json var
            for course in courses:
                #checking for name, because if we dont some courses that are random garbage without names or other defining characteristics will be included
                if 'name' in course:
                    #st.text(f"Course name: {course['name']}, Course ID: {course['id']}")
                    #append each courses id into the course id list. This makes them more easily accesable for other functions in the future
                    courseIDList.append(course['id'])
                    courseNameList.append(course['name'])

                    #each course will have a name, id, and list of assignemts
                    course_data = {
                        "course_name": course['name'],
                        "course_id": course['id'],
                        "assignments": []
                    }

                    #for each class there will be a new link to the assignemtns
                    assignments_link = f"{apiLink}/courses/{course['id']}/assignments"
                    while assignments_link:
                        #get the json response of the assignemtns for a particular course
                        assignments_response = requests.get(assignments_link, headers=headers)
                        #if we successfully get a response
                        if assignments_response.status_code == 200:
                            #put the response into json type variable assignemtns
                            assignments = assignments_response.json()
                            #for eveery assignemt
                            for assignment in assignments:
                                #append the assignment name and due date to the list of assignments
                                course_data["assignments"].append({
                                    "name": assignment.get('name'),
                                    "due_date": assignment.get('due_at', 'N/A')
                                })
                            assignments_link = assignments_response.links.get('next', {}).get('url')
                        else:
                            st.text(f"Failed to fetch assignments for Course ID {course['id']}")
                            break
                    #append the course as a whole to the json
                    data["courses"].append(course_data)




                    #check if there is a next page, otherwise end.
                link = response.links.get('next', {}).get('url')
    with open("studentData.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

  #  st.json(data)

    return data


#####   this function will take the data returned by the previous function and sort it into a list of class objects and assignment objects so we can easily use them   #####
def sortUserDataIntoList(data):
    i = 0
    studentInfo = []
    for course in data['courses']:

        assignmentList = []
        className = Class(course['course_name'], assignmentList)
        studentInfo.append(className)
        
        for assignment in course['assignments']:
            thisOne = Assignment(assignment['name'], assignment['due_date'])
            studentInfo[i].assignmentList.append(thisOne)
        i = i + 1

    return studentInfo









#####   this function is to check if a user has a key already with us   #####
def checkForUserKey(username):

    if 'hasKey' not in st.session_state:
        st.session_state.hasKey = False
   
    #This is the database component's responsiblity: We need to retreive the key from the database
    testToken = retreiveKey(username)

    
    
    #if the user does not have a key do this
    if testToken is None:

            #the first thing we need to do is make the user enter their key and then write that to their name in the database
        st.text("Lets start off by connecting your canvas account. Please input your canvas token:")
            #put the users token into token
        token = ""
        token = st.text_input("Please enter your token")
        testToken = ""

            
        if st.button("Submit token"):

            if token and username:
                        
                    #this is the database components respoonsibility:  we need to insert informatin into the database, so we will have the database component take care of it and not user.
                    testToken = insertUserTokenIntoDatabase(token, username)
                    st.session_state.hasKey = True

                    if testToken == token:
                        st.success(f"Token saved for {username}.")
                        st.session_state.hasToken = True
                        st.session_state.token_saved = True
                        return
                    else:
                        st.error(f"Failed to save or retrieve the token for user {username}.")
    #if the user already has a key, return
    else:
        st.session_state.hasKey = True
        return
    

#####   This function is to register a user   #####
def register():
   
    words = "Submit"
    can = False

    if 'show_text' not in st.session_state:
        st.session_state.show_text = True
    if 'can_show_homepage' not in st.session_state:
        st.session_state.can_show_homepage = False


    if st.session_state.show_text:

        username = st.text_input("Please enter a username")
        password = st.text_input("Please choose a password", type="password")

        if st.button(words):
            if username and password:
                

                #This is the responsibiliyt of the database component: We need to take the entered username and password, check if they are already taken, and if not they can create an account
                success = registerUser(username, password)
                if success:
                    st.text("click again to exit login")
                    st.success("User registered successfully!")
                    st.session_state.show_text = False
                    st.session_state.can_show_homepage = True
                    can = True
                    st.session_state.registered = True
                else:
                    return

                    
                    
                    

                
            
                        
            else:
                st.error("Please fill in both fields before submitting.")

    if st.session_state.can_show_homepage:
        st.text("Thanks for registering, You can now login to your account")


#####   this functinon is for a user to log into their account   #####
def login():
   


    username = st.text_input("Please enter a username")
    password = st.text_input("Please choose a password")

    text = ""


    if st.button("Log in"):

        if username and password:  # Check if both fields are filled
            

            #This is the responsibility of the Database component: we need to take a username and password then check if they are in the databse
            user = loginUser(username, password)
            
            if user:
                st.success(f"Welcome back, {username}! Your user ID is {user[0]}.")
              # st.session_state.isLoggedIn = True
                st.session_state.username = username
                return True
            else:
                st.error("Invalid username or password")
                return False
        else:
            st.error("Please fill in both fields before submitting.")
