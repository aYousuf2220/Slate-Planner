#make links shorter! and add a customizeable name to it as well
#course details -> make name of course bigger than the type
#when adding time to schedule, add it through clock?
#add a delete button for courses

#import
import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import json

st.set_page_config(layout="wide") #add page_icon = whatever icon

#checks
if "reminders" not in st.session_state:
    try:
        with open("reminders.json", "r") as f:
            st.session_state["reminders"] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state["reminders"] = []

if "links" not in st.session_state:
    try:
        with open("links.json", "r") as f:
            st.session_state["links"] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state["links"] = []

if "courses" not in st.session_state:
    try:
        with open("courses.json", "r") as f:
            st.session_state["courses"] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state["courses"] = []

if "tasks" not in st.session_state:
    try:
        st.session_state["tasks"] = pd.read_csv("tasks.csv", parse_dates=["due"])
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.session_state["tasks"] = pd.DataFrame({
        "title": pd.Series(dtype="str"),
        "course": pd.Series(dtype="str"),
        "status": pd.Series(dtype="str"),
        "due": pd.Series(dtype="datetime64[ns]")
    })

if "schedule" not in st.session_state:
    try:
        st.session_state["schedule"] = pd.read_csv("schedule.csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.session_state["schedule"] = pd.DataFrame(columns=["time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

#-----FUNCTIONS------
def add_reminder():
    #first check if the text is not empty:
    if st.session_state["reminder_input"] != "":
        st.session_state["reminders"].append({"text": st.session_state["reminder_input"], "done": False}) #append the text to the list
        save_json(st.session_state["reminders"], "reminders.json")

    #setting the box to blank again
    st.session_state["reminder_input"] = ""

def add_links():
    #first check if the text is not empty:
    if st.session_state["link_input"] != "":
        st.session_state["links"].append(st.session_state["link_input"])
        save_json(st.session_state["links"], "links.json")

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
                save_json(st.session_state["courses"], "courses.json")
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
                    save_json(st.session_state["courses"], "courses.json")
                    st.rerun()

        st.divider()

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)

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
            save_json(st.session_state["reminders"], "reminders.json")
        with col2:
            st.write(reminder["text"])

        with col3:
            if st.button("🗑️", key=f"delete_reminder_{i}"):
                st.session_state["reminders"].pop(i)
                save_json(st.session_state["reminders"], "reminders.json")
                st.rerun()

    #-----QUICKLINKS-----
    st.subheader("Quick Links")
    quicklinks = st.text_input("add your quick links:", icon="🔗", key="link_input", type="url", on_change=add_links)

    for i, links in enumerate(st.session_state["links"]):
        col1, col2 = st.columns([0.7, 0.2])
    
        with col1:
            st.write(links)

        with col2:
            if st.button("🗑️", key=f"delete_link_{i}"):
                        st.session_state["links"].pop(i)
                        save_json(st.session_state["links"], "links.json")
                        st.rerun()

#-----COURSE SECTION-----
with st.popover("➕ Add Course"):
    with st.form("course_form", clear_on_submit=True):
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

        submitted = st.form_submit_button("Add Course")

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

            save_json(st.session_state["courses"], "courses.json")
for i, course in enumerate(st.session_state["courses"]):
    if st.button(course["course_name"], key=f"course_{i}"):
        show_course(course)

#-----TASKS-----
st.subheader("Tasks")

course_names = [course["course_name"] for course in st.session_state["courses"]]
st.session_state["tasks"] = st.session_state["tasks"].reset_index(drop=True)

with st.form("tasks_form"):
    edited_tasks = st.data_editor(
        st.session_state["tasks"],
        column_config={
            "title": st.column_config.TextColumn("Title"),
            "course": st.column_config.SelectboxColumn("Course", options=course_names),
            "status": st.column_config.SelectboxColumn("Status", options=["Not Started", "In Progress", "Done", "Late"]),
            "due": st.column_config.DateColumn("Due Date")
        },
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        key="tasks_editor"
    )
    save_tasks = st.form_submit_button("Save Tasks")

if save_tasks:
    edited_tasks["due"] = pd.to_datetime(edited_tasks["due"], errors="coerce")
    st.session_state["tasks"] = edited_tasks.reset_index(drop=True)
    st.session_state["tasks"].to_csv("tasks.csv", index=False)

#----SCHEDULE----
st.subheader("Course Schedule")

course_names = [course["course_name"] for course in st.session_state["courses"]]
st.session_state["schedule"] = st.session_state["schedule"].reset_index(drop=True)
with st.form("schedule_form"):
    edited_schedule = st.data_editor(
        st.session_state["schedule"],
        column_config={
            "time": st.column_config.TextColumn("Time"),
            "Monday": st.column_config.SelectboxColumn("Mon", options=course_names),
            "Tuesday": st.column_config.SelectboxColumn("Tue", options=course_names),
            "Wednesday": st.column_config.SelectboxColumn("Wed", options=course_names),
            "Thursday": st.column_config.SelectboxColumn("Thu", options=course_names),
            "Friday": st.column_config.SelectboxColumn("Fri", options=course_names),
            "Saturday": st.column_config.SelectboxColumn("Sat", options=course_names),
            "Sunday": st.column_config.SelectboxColumn("Sun", options=course_names)
        },
        num_rows="dynamic",
        width="stretch",
        hide_index=True
    )
    save_schedule = st.form_submit_button("Save Schedule")

if save_schedule:
    st.session_state["schedule"] = edited_schedule.reset_index(drop=True)
    st.session_state["schedule"].to_csv("schedule.csv", index=False)

#-----CALENDAR-----
daysOfWeek = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
calendar_events = []

for _, task in st.session_state["tasks"].iterrows(): #gives row number and row contents; _ is "ignore this"
    if pd.notna(task["title"]) and pd.notna(task["due"]):
       calendar_events.append({"title": task["title"], "start": str(task["due"])})


for _, row in st.session_state["schedule"].iterrows():
    for day_name, day_num in daysOfWeek.items(): #.items gets the halves of the dictionaries' pairs at once
        if pd.notna(row[day_name]):
            calendar_events.append({"title": f"{row[day_name]} ({row['time']})", "daysOfWeek": [day_num]})

calendar(events=calendar_events, options={"initialView": "dayGridMonth", "firstDay": 1}, key="calendar")

#AI Agent
