#bug found! When check mark and delete reminder, it gives error when u delete link

#import
import streamlit as st

#checks + variables
if "reminders" not in st.session_state:
    st.session_state["reminders"] = [] #starts as an empty list

if "links" not in st.session_state:
    st.session_state["links"] = []

if "courses" not in st.session_state:
    st.session_state["courses"] = []

#-----FUNCTIONS------
def add_reminder():
    #first check if the text is not empty:
    if st.session_state["reminder_input"] != "":
        st.session_state["reminders"].append({"text": st.session_state["reminder_input"], "done": False}) #append the text to the list

    #setting the box to blank again
    st.session_state["reminder_input"] = ""

def add_links():
    #first check if the text is not empty:
    if st.session_state["link_input"] != "":
        st.session_state["links"].append(st.session_state["link_input"])

    #setting the box to blank again
    st.session_state["link_input"] = ""

@st.dialog("Course Details")
def show_course(course):
    with st.popover("✏️ Edit Course Name"):
        with st.form(f"edit_course_name_{course['course_name']}"):
            new_name = st.text_input("Course name:", value=course["course_name"])
            save_name = st.form_submit_button("Save")
            if save_name:
                course["course_name"] = new_name
                st.rerun()

    st.write(course["course_name"])

    for j, detail in enumerate(course["course_details"]):
        st.subheader(detail["type"])
        st.write(f"Days: {', '.join(detail['day'])}")
        st.write(f"Time: {detail['start_time']} - {detail['end_time']}")
        st.write(f"Room: {detail['room']}")
        st.write(f"CRN: {detail['crn']} | Section: {detail['section']}")
        st.write(f"Instructor: {detail['instructor_name']} ({detail['instructor_email']})")

        with st.popover(f"✏️ Edit {detail['type']}"):
            with st.form(f"edit_detail_{course['course_name']}_{j}"):
                edit_type = st.text_input("Type:", value=detail["type"])
                edit_days = st.multiselect("Days:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], default=detail["day"])
                edit_start = st.text_input("Start time:", value=detail["start_time"])
                edit_end = st.text_input("End time:", value=detail["end_time"])
                edit_room = st.text_input("Room:", value=detail["room"])
                edit_crn = st.text_input("CRN:", value=detail["crn"])
                edit_section = st.text_input("Section:", value=detail["section"])
                edit_instructor = st.text_input("Instructor:", value=detail["instructor_name"])
                edit_email = st.text_input("Contact email:", value=detail["instructor_email"])

                save_detail = st.form_submit_button("Save Changes")
                if save_detail:
                    detail["type"] = edit_type
                    detail["day"] = edit_days
                    detail["start_time"] = edit_start
                    detail["end_time"] = edit_end
                    detail["room"] = edit_room
                    detail["crn"] = edit_crn
                    detail["section"] = edit_section
                    detail["instructor_name"] = edit_instructor
                    detail["instructor_email"] = edit_email
                    st.rerun()

        st.divider()

#-----UI-----
st.title("slate")

with st.sidebar:
    #-----REMINDERS-----
    st.subheader("Reminders")
    reminder = st.text_input("add a reminder:", icon="📌", key="reminder_input", on_change=add_reminder)

    for i, reminder in enumerate(st.session_state["reminders"]):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

        with col1:
            checked = st.checkbox("", value=reminder["done"], key=f"done_{i}")
            st.session_state["reminders"][i]["done"] = checked

        with col2:
            st.write(reminder["text"])

        with col3:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state["reminders"].pop(i)
                st.rerun()

    #-----QUICKLINKS-----
    st.subheader("Quick Links")
    quicklinks = st.text_input("add your quick links:", icon="🔗", key="link_input", type="url", on_change=add_links)

    for i, links in enumerate(st.session_state["links"]):
        col1, col2 = st.columns([0.7, 0.2])
    
        with col1:
            st.write(links)

        with col2:
            if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state["links"].pop(i)
                        st.rerun()

#-----COURSE SECTION-----
with st.popover("➕ Add Session"):
    with st.form("session_form", clear_on_submit=True):
        course_name = st.text_input("Course name:")
        course_type = st.text_input("Type:")
        days = st.multiselect("Days:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        start_time = st.text_input("Start time:")
        end_time = st.text_input("End time:")
        room = st.text_input("Room:")
        crn = st.text_input("CRN:")
        section = st.text_input("Section:")
        instructor_name = st.text_input("Instructor:")
        instructor_email = st.text_input("Contact email:")

        submitted = st.form_submit_button("Add Session")

        if submitted:
            new_detail = {
                "type": course_type, "day": days, "start_time": start_time, "end_time": end_time,
                "room": room, "crn": crn, "section": section,
                "instructor_name": instructor_name, "instructor_email": instructor_email
            }

            found = False
            for course in st.session_state["courses"]:
                if course["course_name"] == course_name:
                    course["course_details"].append(new_detail)
                    found = True

            if not found:
                st.session_state["courses"].append({"course_name": course_name, "course_details": [new_detail]})

for i, course in enumerate(st.session_state["courses"]):
    if st.button(course["course_name"], key=f"course_{i}"):
        show_course(course)