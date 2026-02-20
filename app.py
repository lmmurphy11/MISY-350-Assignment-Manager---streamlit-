import streamlit as st 

#1. Step 1: Header First (Text Elements)
st.title("AI Course Manager")
st.subheader("Course Assignment Manager")
st.header("Course Assignment Manager")

st.divider()
#2. Step 2: Define Assignments List (Data Continuity)

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

#3. Step 3: Add New Assignment Section (Inputs & Layout)
#col1, col2 = st.columns(2) -----> this will give you 50%---50%
st.subheader("Add New Assignment")

with st.container(border= True)

col1, col2 = st.columns([2,1])
#col1, col2, col3 = st.colomns([1, 6, 1])

with col1:
    with st.container(border= True):
        st.markdown("### Assignment Details")
        title = st.text_input("Assignment title", placeholder="homework1", help= "Enter a short name")
        description = st.text_area("Assignment Description", placeholder= "ex. details...")    

with col2:
    st.markdown("**Due Date Selection**")
    due_date = st.date_input("Due Date")
