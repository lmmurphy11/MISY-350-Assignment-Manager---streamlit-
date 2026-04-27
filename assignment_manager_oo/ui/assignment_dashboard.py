import streamlit as st
from data.assignment_store import AssignmentStore
from services.assignment_manager  import AssignmentManager

class AssignmentDashboard:
    def __init__(self, manager: AssignmentManager, store: AssignmentStore) -> None:
        self.manager = manager
        self.store = store

    def main(self):
        if st.session_state["page"] == "dashboard":
            self.show_manager_assignments()
        else:
            self.show_add_new_assignments()
    
    def show_manager_assignments(self):
        col1,col2 = st.columns([3,1])
        with col1:
            st.subheader("Assignments")
        with col2:
            if st.button("Add New Assignment", key="new_assignment_btn", type="primary", use_container_width=True):
                st.session_state['page'] = "add new assignment"
                st.rerun()
        
        for assignment in self.manager.all():
            with st.container(border=True):
                st.markdown(f"Title: {assignment['title']}")
                if st.button("Edit", key="edit_assignment_{assignment['id']}", type="secondary", use_container_width=True):
                    pass

            st.divider()


    def show_add_new_assignments(self):
        st.subheader("Add New Assignment")
        title = st.text_input("Title", key="title_txt")
        description = st.text_area("Description", key="description_txt")
        if st.button("Save", key="save_btn", type="primary", use_container_width=True):
            import time
            time.sleep(2)


            if not title:
                st.warning("Title is missing")
            else:
                new_assignment = self.manager.add(title, description, 100, "Homework")
                self.store.save(self.manager.all())

                st.success(f"Assignment is recorded. The new assignment id is {new_assignment['id']}")
                time.sleep(3)
                st.session_state['page'] = "dashboard"
                st.rerun()

