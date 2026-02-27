import streamlit as st

st.title("Course Management App")
st.header("Assignment Management")
st.subheader("Dashboard")

next_assignment_id_number = 3

st.divider()
st.markdown("----------")

#load data
assignments = [
    {
        "id": "HW1",
        "title": "Intro to Database",
        "description": "basics of database design",
        "points": 100,
        "type": "homework"
    } ,
    {
        "id": "HW2",
        "title": "Normalization",
        "description": "normalizing",
        "points": 100,
        "type": "homework"
    }
]

#input
#st.markdown("# Add New Assignment")
st.markdown("## Add New Assignment")
#st.markdown("### Add New Assignment")

title = st.text_input("Title")
description = st.text_area("Description", placeholder = "normalization is covered here", 
                           help = "Here you are entering the assignmant details")
points = st.number_input("Points")

#assignment_type = st.text_input("Assignment Type")
assignment_type = st.radio("Type", ["Homework", "Lab"], horizontal = True)
assignment_type2 = st.selectbox("Type", ["Homework", "Lab", "other"])
if assignment_type2 == "other":
    assignment_type2 = st.text_input("Type", placeholder = "Enter the Assignment Type")

due_date = st.date_input("Due Date")

btn_save = st.button("Save", width= "stretch", disabled = False)

if btn_save:
    if not title:
        st.warning("Title needs to be provided!")
    else:
        with st.spinner("Assignment is being recorded...."):
            time.sleep(5)

            new_assignment_id = "HW" + str(next_assignment_id_number)
            next_assignment_id_number += 1

            assignments.append(
                {
                    "id" : new_assignment_id,
                    "title" : title,
                    "description" : description,
                    "points" : points,
                    "type" : assignment_type
                }
            )

            st.success("New Assignment is recorded!")
            st.info("This is a new assignment")
            st.dataframe(assignments)



