import streamlit as st
import hashlib
import streamlit.components.v1 as components
import json
from user import initializeUserInfoJSON, checkForUserKey



#this is the UI component's responsibility: we need to check if the token is saved or not. If the bool variable to check is not present create it and set it to false until the token is saved.
if 'token_saved' not in st.session_state:
    st.session_state.token_saved = False

 
if 'isLoggedIn' not in st.session_state:
    st.session_state.isLoggedIn = False

if 'hasKey' not in st.session_state:
    st.session_state.hasKey = False

def homePageView():


    #this is the user component's responsibility: here we need to check if the user has a key registered with us, if not, prompt them to do so.
    username = st.session_state.username

    checkForUserKey(username)
    
    #connection point between UI and User. We call user function to return a json file for the UI to display
    if st.session_state.hasKey == True:
        data = initializeUserInfoJSON(username)



        html_code = f"""
        <style>
        :root {{
            --primary-clr: #b38add;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Poppins" , sans-serif;
        }}
        body {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #e2e1dc;
        }}
        .container{{
            position: relative;
            width: 1200px;
            min-height: 850px;
            margin: 0 auto;
            padding: 5px;
            color: #fff;
            display: flex;
            border-radius: 10px;
            background-color: #373c4f;
        }}
        .left {{
            width: 90%;
            padding: 20px;
        }}
        .calendar {{
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            flex-wrap: wrap;
            justify-content: space-between;
            color: #878895;
            border-radius: 5px;
            background-color: #fff;
        }}
        .calendar::before,
        .calendar::after {{
            content: "";
            position: absolute;
            top: 50%;
            left: 100%;
            width: 12px;
            height: 97%;
            border-radius: 0 5px 5px 0;
            background-color: #d3d5d6d7;
            transform: translateY(-50%);
        }}
        .calendar::before {{
            height: 94%;
            left: calc(100% + 12px);
            background-color: rgb(153, 153, 153);
        }}
        .calendar .month{{
            width: 100%;
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 50px;
            font-size: 1.2rem;
            font-weight: 500;
            text-transform: capitalize;
        }}
        .calendar .month .prev,
        .calendar .month .next {{
            cursor: pointer;
        }}
        .calendar .month .prev:hover,
        .calendar .month .next:hover {{
            color: var(--primary-clr);
        }}
        .calendar .weekdays {{
            width: 100%;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            font-size: 1rem;
            font-weight: 500;
            text-transform: capitalize;
        }}
        .calendar .weekdays div {{
            width: 14.28%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .calendar .days {{
            width: 100%;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            padding: 0 20px;
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 20px;
        }}
        .calendar .days .day {{
            width: 14.28%;
            height: 90px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: var(--primary-clr);
            border: 1px solid #f5f5f5;
        }}
        .calendar .day:not(.prev-date , .next-date):hover {{
            color : #fff;
            background-color: var(--primary-clr);
        }}
        .calendar .days .prev-date,
        .calendar .days .next-date {{
            color: #b3b3b3
        }}
        .calendar .days .active {{
            position: relative;
            font-size: 2rem;
            color: #fff;
            background-color: var(--primary-clr);
        }}
        .calendar .days .active::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            box-shadow: 0 0 10px 2px var(--primary-clr);
        }}
        .calendar .days .today {{
            font-size: 2rem;
        }}
        .calendar .days .event {{
            position: relative;
        }}
        .calendar .days .event::after {{
            content: ''; 
            position: absolute;
            bottom: 10%;
            left: 50%;
            width: 75%;
            height: 6px;
            border-radius: 30px;
            transform: translateX(-50%);
            background-color: var(--primary-clr);
        }}
        .calendar .event:hover::after {{
            background-color: #fff;
        }}
        .calendar .active.event::after {{
            background-color: #fff;
            bottom: 20%;
        }}
        .calendar .active.event{{
            padding-bottom: 10px;
        }}
        .calendar .goto-today {{
            width: 100%;
            height: 50px;   
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 5px;
            padding: 0 20px;
            margin-bottom: 20px;
            color: var(--primary-clr);
        }}
        .calendar .goto-today .goto {{
            display: flex;
            align-items: center;
            border-radius: 5px;
            overflow: hidden;
            border: 1px solid var(--primary-clr);
        }}
        .calendar .goto-today .goto input {{
            width: 100%;
            height: 30px;   
            outline: none;
            border: none;
            border-radius: 5px;
            padding: 0 20px;
            color: var(--primary-clr);
            border-radius: 5px;
        }}
        .calendar .goto-today button {{
            padding: 8px 10px;
            border: 1px solid var(--primary-clr);
            border-radius: 5px;
            background-color: transparent;
            cursor: pointer;
            color: var(--primary-clr);
        }}
        .calendar .goto-today button:hover {{
            color: #fff;
            background-color: var(--primary-clr);
        }}
        .calendar .goto-today .goto button {{
            border: none;
            border-left: 1px solid var(--primary-clr);
            border-radius: 0;
        }}
        </style>

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <link rel="stylesheet" type="text/css" href="style.css"  />
            <link
            rel="stylesheet" 
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" 
            integrity="sha512-Kc323vGBEqzTmouAECnVceyQqyqdsSiqLQISBL29aUW4U/M7pSPA/gEUZQqv1cwx4OnYxTxve5UMg5GT6L4JJg==" 
            crossorigin="anonymous" 
            referrerpolicy="no-referrer" />
            <title>Calander</title>
        </head>  
        <body>
            <div class="container">
            <div class="left">
                <div class="calendar">
                <div class="month">
                    <i class="fa fa-angle-left prev"></i>
                        <div class="date">add curent day here</div>
                    <i class="fa fa-angle-right next"></i>
                </div>
                <div class="weekdays">
                    <div>sun</div>
                    <div>mon</div>
                    <div>tue</div>
                    <div>wed</div>
                    <div>thur</div>
                    <div>fri</div>
                    <div>sat</div>
                </div>
                <div class="days">
                    //add days by script.js
                </div>
                <div class="goto-today">
                    <div class="goto">
                    <input type="text" placeholder="mm/yyyy" class="date-input" >
                    <button class="goto-btn">go</button>
                    </div>
                    <button class="today-btn">today</button>
                </div>
                </div>
            </div>
            </div>
            <script src="script.js"></script>
        </body>
        </html> 

        <script>
            const calendar = document.querySelector(".calendar"),
        date = document.querySelector(".date"),
        daysContainer = document.querySelector(".days"),
        prev = document.querySelector(".prev"),
        next = document.querySelector(".next");
        todayBtn = document.querySelector(".today-btn"),
        gotoBtn = document.querySelector(".goto-btn"),
        dateInput = document.querySelector(".date-input");

        let today = new Date();
        let activeDay;
        let month = today.getMonth();
        let year = today.getFullYear();
        const months =[
            "January", 
            "February", 
            "March", 
            "April", 
            "May", 
            "June", 
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
        // function to add days
        function initCalendar(){{
            //first day of the month
            const firstDay = new Date(year, month, 1);
            //last day of the month, 0 mean the last day of the previous month-current month
            const lastDay = new Date(year, month+1, 0);
            //last day of previous month because O automatically set it to last day of previous month
            const prevLastDay = new Date(year, month, 0);
            //Number of days in the previous month
            const prevDays = prevLastDay.getDate();
            //Number of days in the current month
            const LastDate = lastDay.getDate();
            // Day of the week the month starts on
            const day = firstDay.getDay();
            //  Remaining days for next month
            const nextDays = 7 - lastDay.getDay()-1;
        //update date to top of calendar
        date.innerHTML =months[month] +" "+ year; 
        //adding days on dom
        let days = "";
        //prev month days
        for (let x= day; x > 0;x--){{
            //The class day is used to style all days, and prev-date can be used to style days from the previous month
            days +=`<div class= "day prev-date" >${{prevDays - x + 1}}</div>`;
        }}
        //current month days
        for (let i=1; i<= LastDate; i++){{
            //if day is today add class today
            if (i === new Date().getDate() && 
            year === new Date().getFullYear()&& 
            month == new Date().getMonth() ){{
                days +=`<div class= "day today" >${{i}}</div>`;        
            }}
            // add remaining as it is
            else{{
                days += `<div class ="day">${{i}}</div>`;
            }}
            }}
        //next  month days
        for(let j =1; j <= nextDays; j++){{
            days +=`<div class="day next-date" >${{j}}</div>`;
        }}
        daysContainer.innerHTML = days;
        }}
        initCalendar();
        //prev month 
        function prevMonth(){{
            month--;
            if(month <0){{
                month = 11;
                year--;
            }}
            initCalendar();

        }}
        // next month
        function nextMonth(){{
            month++;
            if (month > 11){{
                month = 0;
                year++;
            }}
            initCalendar();
        }}
        //add eventListnner on prev and next
        prev.addEventListener("click",prevMonth);
        next.addEventListener("click", nextMonth);
        // lets add togo date and goto today functionality
        todayBtn.addEventListener("click", ()=>{{
            today = new Date();
            month = today.getMonth();
            year = today.getFullYear();
            initCalendar();
        }});
        dateInput.addEventListener("input",(e)=>{{
            dateInput.value = dateInput.value.replace(/[^0-9/]/g,"");
            if (dateInput.value.length ===2){{
                dateInput.value +="/";

            }}
            if (dateInput.value.lenth >7){{
                // don't allow more than 7 character
                dateInput.value = dateInput.value.slice(0,7);
            }}
            //if backspace pressed
            if(e.inputType ==="deleteContentBackward"){{
                if(dateInput.value.length === 3){{
                    dateInput.value = dateInput.value.slice(0,2);
                }}
            }}

        }});
        gotoBtn.addEventListener("click", gotoDate);
        //function to go to entered date
        function gotoDate(){{
            const dateArr = dateInput.value.split("/");
            //some data validation
            if(dateArr.length ===2){{
                if(dateArr[0]>0 && dateArr[0]<13 && dateArr[1].length ===4){{
                    month = dateArr[0]-1;
                    year = dateArr[1];
                    initCalendar();
                    return;
                }}
            }}
            //if invalid date
            alert("invalid date");
        }}


        //////////////////     create array of assignments     ////////////////

        class Assignment {{
                constructor(name, dueDate) {{
                this.name = name;
                this.dueDate = dueDate;
                }}
            }}

        //create an array to store all of the assignments
        const assignmentsArray = [];

        //this will get the json data from the backend and put it into data
        const data = {json.dumps(data)};

            

        //populate the array
        data.courses.forEach(course => {{
                //in each course, loop thorugh each assignment, make it an object, and add it to an assignemtn array
                course.assignments.forEach(assignment => {{
                    const individualAssignment = new Assignment(assignment.name, assignment.due_date);
                    assignmentsArray.push(individualAssignment);
                }});
            }});

        /////////////////     array of assignments now exists as "assignmentsArray"      ////////////
        //now you just need to loop through the assignments array, sort them by date, and then display them on the calender.
        //each assignemnt in the array is an assignment object with a name and a dueDate.










        </script>
        
        """
        components.html(html_code, height=840, width=700)          

    

#this is the responisbility of UI component: Check if the user has logged in, if they have then they can access the home page, other wise tell them to go log in.
if st.session_state.isLoggedIn:
    homePageView()
else:
    st.text("Please log in to view home page.")