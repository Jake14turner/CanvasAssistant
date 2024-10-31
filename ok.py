import requests
import streamlit as st
import json
import streamlit.components.v1 as components


def initializeUserInfo(courseIDList, courseNameList, studentInfo, token):
    st.text("Fetching course and assignment data...")

    # Define the API link and headers for authentication
    apiLink = 'https://canvas.instructure.com/api/v1'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {"courses": []}

    # Link to fetch all courses
    link = f'{apiLink}/courses'
    while link:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            courses = response.json()
            for course in courses:
                if 'name' in course:
                    courseIDList.append(course['id'])
                    courseNameList.append(course['name'])
                    course_data = {
                        "course_name": course['name'],
                        "course_id": course['id'],
                        "assignments": []
                    }

                    # Link to fetch assignments for each course
                    assignments_link = f"{apiLink}/courses/{course['id']}/assignments"
                    while assignments_link:
                        assignments_response = requests.get(assignments_link, headers=headers)
                        if assignments_response.status_code == 200:
                            assignments = assignments_response.json()
                            for assignment in assignments:
                                course_data["assignments"].append({
                                    "name": assignment.get('name'),
                                    "due_date": assignment.get('due_at', 'N/A')
                                })
                            assignments_link = assignments_response.links.get('next', {}).get('url')
                        else:
                            st.text(f"Failed to fetch assignments for Course ID {course['id']}")
                            break
                    
                    data["courses"].append(course_data)

            # Check if there is a next page of courses
            link = response.links.get('next', {}).get('url')
        else:
            st.text("Failed to fetch courses.")
    
    # Save JSON data to file and return
    with open("studentData.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    return data


def main():
    courseIDlist = []
    courseNameList = []
    studentInfo = []

    # Fetch course and assignment data
    data = initializeUserInfo(courseIDlist, courseNameList, studentInfo, "9082~H94WY2RcwPDe3G823RXMC3nemFu4MCcDa8M8GyFC6KT6KaWNxfKuEyCGAntZt4PU")
    
    # HTML and JavaScript template for displaying the data
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Course and Assignment Display</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .scrollable-container {{
                max-height: 400px;  /* Set a max height for scrolling */
                overflow-y: auto;   /* Enable vertical scrolling */
                border: 1px solid #ccc; /* Add a border for clarity */
                padding: 10px; /* Add some padding */
            }}
            .course {{ margin-bottom: 20px; }}
            .course h3 {{ color: #2a9d8f; }}
            .assignment {{ margin-left: 20px; }}
        </style>
    </head>
    <body>
        <div class="scrollable-container" id="courses-container"></div>
        <script>

            //create a class called assignment to store assignments
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

            
            const container = document.getElementById("courses-container");

            //loop thorugh each course in the data
            data.courses.forEach(course => {{
                const courseDiv = document.createElement("div");
                courseDiv.className = "course";
                courseDiv.innerHTML = `<h3>${{course.course_name}}</h3>`;  // Corrected line

                //in each course, loop thorugh each assignment, make it an object, and add it to an assignemtn array
                course.assignments.forEach(assignment => {{
                    const individualAssignment = new Assignment(assignment.name, assignment.due_date);
                    assignmentsArray.push(individualAssignment);
                    const assignmentDiv = document.createElement("div");
                    assignmentDiv.className = "assignment";
                    assignmentDiv.innerHTML = `<strong>Assignment:</strong> ${{assignment.name}} <br><strong>Due Date:</strong> ${{assignment.due_date}}`;  // Corrected line
                    courseDiv.appendChild(assignmentDiv);
                }});

                container.appendChild(courseDiv);
            }});
            
        </script>
    </body>
    </html>
    """

    # Render HTML in Streamlit
    components.html(html_code, height=500)


if __name__ == "__main__":
    main()
