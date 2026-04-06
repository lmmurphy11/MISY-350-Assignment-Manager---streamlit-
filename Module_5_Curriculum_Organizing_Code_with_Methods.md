# Module 5 Curriculum: Organizing Code with Methods (and the Road to Classes)

As our applications grow, putting all of our code in one long file from top to bottom causes "Spaghetti Code"—it becomes a nightmare to read, fix, and maintain. Today, we learn how to package our code into reusable blocks called **Methods** (Functions), which will eventually lead us to **Classes**. We will take our massive Assignment Manager script and transform it into a professional, scalable architecture.

## Learning Objectives

1. **Defining & Calling Methods:** Understand method anatomy (parameters, execution, return values) and Python list mutability.
2. **Separation of Concerns (SoC):** Learn to cleanly separate your visual UI (Frontend) from your Data and Service Logic (Backend).
3. **Refactoring & The DRY Principle:** Use the "Don't Repeat Yourself" principle to conquer spaghetti code and build reusable logic blocks.
4. **The Main Router:** Securely encapsulate your application state and navigation inside a central `main()` loop using `if __name__ == "__main__":`.

---

## 0. Build the Base Code (Procedural Style)

Before we jump into new concepts, let's assemble our assignment application piece by piece using the sequential (top-to-bottom) style you are familiar with.

### 0.1 Imports and Page Config
We start with the required imports and setting up the Streamlit page appearance.

```python
import streamlit as st
import time
import json
from pathlib import Path
import uuid

st.set_page_config(
    page_title="Course Management",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Course Management App")
st.divider()
```

### 0.2 Loading the Data
Next, we define our default assignment data and try to load any existing saved data from a JSON file.

```python
# Placeholder Default Data
assignments = [
    {
        "id": "HW1",
        "title": "Intro to Database",
        "description": "basics of database design",
        "points": 100,
        "type": "homework"
    },
    {
        "id": "HW2",
        "title": "Normalization",
        "description": "normalizing",
        "points": 100,
        "type": "homework"
    }
]

json_path = Path("assignments.json")

# Load the data from a json file if it exists
if json_path.exists():
    with open(json_path, "r", encoding="utf-8") as f:
        assignments = json.load(f)
```

### 0.3 Session State Initialization
We need to track our navigation (`page`) and an empty dictionary to hold the user's form inputs (`draft`).

```python
if "page" not in st.session_state:
    st.session_state["page"] = "Assignments Dashboard"

if "draft" not in st.session_state:
    st.session_state["draft"] = {}
```

### 0.4 The Dashboard View
If we are on the dashboard, we write a quick loop to display all the assignments we loaded in step 0.2.

```python
pass

```

### 0.5 The "Add New Assignment" Form
If the user clicked the add button, our state changes and this massive `elif` block takes over to draw the form, handle validation, append data, and write directly back into the JSON file.

```python
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Add New Assignment")
    with col2:
        if st.button("Back", key="back_btn", use_container_width=False):
            st.session_state["page"] = "Assignments Dashboard" 
            st.rerun()

    # Form Inputs
    st.session_state['draft']['title'] = st.text_input("Title")
    st.session_state['draft']['description'] = st.text_area("Description", placeholder="normalization is covered here",
                            help="Here you are entering the assignment details")
    st.session_state["draft"]['points'] = st.number_input("Points")

    st.session_state['draft']['assignment_type'] = st.selectbox("Type", ["Select an option", "Homework", "Lab", "other"])
    if st.session_state["draft"]['assignment_type'] == "other":
        st.session_state["draft"]['assignment_type'] = st.text_input("Type", placeholder="Enter the assignment Type")

    # Live Preview
    with st.container(border=True):
        with st.expander("Assignment Details", expanded=True):
            # Using .get() for safe dictionary access on initial load
            st.markdown(f"### Title: {st.session_state['draft'].get('title', '')}")
            st.markdown(f"**Description**: {st.session_state['draft'].get('description', '')}")
            st.markdown(f"Type: **{st.session_state['draft'].get('assignment_type', '')}**")
    
    # Save Action
    btn_save = st.button("Save", use_container_width=True, key="save_btn", type="primary")

    if btn_save:
        if not st.session_state['draft'].get('title'):
            st.warning("Title needs to be provided!")
        else:
            with st.spinner("Assignment is being recorded...."):
                time.sleep(2)
                
                # Append to list
                assignments.append(
                    {
                        "id": str(uuid.uuid4()),
                        "title": st.session_state['draft']['title'],
                        "description": st.session_state['draft']['description'],
                        "points": st.session_state['draft']['points'],
                        "type": st.session_state['draft']['assignment_type']
                    }
                )

                # Record directly into JSON file 
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(assignments, f, indent=4)

                st.success("New Assignment is recorded!")
                st.info("This is a new assignment")
                
                time.sleep(2)
                st.session_state["page"] = "Assignments Dashboard"
                st.session_state["draft"] = {}
                st.rerun()
```

---

## 1. The Problem: Spaghetti Code

Now look at the combined code we just built for our Assignment Manager. It controls navigation using `st.session_state["page"]` and a massively long `if/elif` block. 

```python
# ... imports and setup ...

if st.session_state["page"] == "Assignments Dashboard":
    col1, col2 = st.columns([3, 1])
    # ... lots of code drawing the dashboard ...
    pass
    
elif st.session_state["page"] == "Add New Assignment":
    st.markdown("## Add New Assignment")
    # ... 30 lines of inputs ...
    # ... 20 lines of saving to JSON logic inside the button click ...
    pass

elif st.session_state["page"] == "Edit Assignment":
    st.markdown("## Edit Assignment")
    # ... 40 lines of edit form ...
    # ... 20 lines of updating existing JSON logic ...
    pass
```

**Why is a massive if/elif block a problem?**
1. **Spaghetti Code (Unreadable):** The file is hundreds of lines long. Finding where the "Save" logic lives takes scrolling forever, creating a maintenance nightmare.
2. **Violates the DRY Principle (Hard to Reuse):** If we want to add a feature to bulk-upload assignments via an Excel file, we can't cleanly do it. The "save to JSON" logic is trapped inside a Streamlit UI button click. We'd have to copy/paste the code, violating the "Don't Repeat Yourself" principle.
3. **No Separation of Concerns (Trapped Logic):** Our backend business logic (saving data) is permanently tangled with our frontend UI (Streamlit buttons). This makes the app rigid and impossible to scale or upgrade to a new UI later.
4. **Variable Intersections:** With everything in one giant global file, it's dangerously easy to accidentally overwrite a variable in one section that you meant to safely use in another.

---

## 2. The Solution: Methods (Functions)

Imagine a factory that builds cars. Right now, your code is like one single worker running around the factory floor doing everything sequentially (Procedural Code). 

**Methods** are like setting up dedicated workstations. You have a "Data Station" and a "Dashboard UI Station". The single worker just delegates the task to the station, and the station does its specific job perfectly every time.

---

## 3. Two Core Pillars: Refactoring and Separation of Concerns

Before we fix our spaghetti code, we need to understand the two major software engineering ideas driving our changes.

### Pillar 1: Refactoring & Reusability
**Refactoring** is the process of restructuring existing code without changing its external behavior. It's like organizing a messy closet: you aren't buying new clothes, you are just arranging them so they are easier to find and maintain.
A major goal of refactoring is **Reusability** (often referred to as the DRY principle: *Don't Repeat Yourself*). If you find yourself copying and pasting the same 10 lines of code to save a JSON file in three different places, you are creating a nightmare to maintain. Instead, you should *refactor* that logic into a single method and just call it whenever you need it. Write once, use anywhere!

### Pillar 2: Separation of Concerns (SoC)
**Separation of Concerns (SoC)** states that your app should be divided into distinct sections, where each section handles a singular, specific job.
*   **Data Layer:** Reads and writes to the file system (JSON).
*   **Service Layer:** Handles the "business logic" (validating, formatting dictionaries, generating IDs).
*   **UI Layer:** Draws the Streamlit buttons and inputs.

**Connecting to the Industry: Frontend vs. Backend**
In the professional software world, this separation is often described in terms of **Frontend** and **Backend**.
*   **Frontend (The Face):** What the user sees, clicks, and interacts with. In our app, this is the **UI Layer** (Streamlit). It should *only* care about displaying information and capturing input, not doing complex math or writing to databases.
*   **Backend (The Brains):** The hidden engine and memory of the application. In our app, this is the **Service Layer** (logic/rules) and the **Data Layer** (JSON files). It doesn't care if the user is clicking a button on a website, a mobile app, or a smart TV; it just processes data and returns answers.

**Why is SoC crucial for Scalability?**
When your code is firmly mixed together (e.g., saving data to a file directly inside a Streamlit button click event), you are permanently tying your backend business logic to your frontend visual interface. If you decide to upgrade your app in the future and replace Streamlit with a modern web framework like Next.js, React, or even a mobile app, you would have to throw away and rewrite *everything*. 

By separating concerns, your **Data Layer** and **Service Layer** (Backend) become completely independent of the UI (Frontend). If you ever swap out Streamlit, your core Python business logic and file management remain completely untouched—you only have to rewrite the visual UI layer! This modularity is the secret to building robust applications that can scale, adapt, and evolve over time without breaking.

### Application Architecture Overview

Here is a simple visualization of how data flows through a well-organized application:

```text
📱 1. FRONTEND (User Interface)
      [ Streamlit / Next.js / Mobile App ]
                    ↕
           (Sends User Input)
         (Receives Screen Updates)
                    ↕
⚙️ 2. BACKEND (The Brains)
      [ Service Layer: Business Logic & Rules ]
                    ↕
      [ Data Layer: File Readers & Writers ]
                    ↕
           (Reads & Writes)
                    ↕
💾 3. STORAGE
      [ assignments.json ]
```

Let's refactor our giant assignment app step-by-step.

### 🐍 Crash Course: Defining Methods in Python
Before we start moving code around, let's review the exact anatomy of a method. A method has three main components: the **Definition**, the **Inputs (Parameters)**, and the **Output (Return Value)**.

```python
# 1. 'def' tells Python we are creating a method.
# 2. 'calculate_grade' is the name of the method.
# 3. The variables inside the parentheses are the INPUTS (parameters).
def calculate_grade(points_earned, points_possible):
    
    # Everything indented underneath is the logic.
    percentage = (points_earned / points_possible) * 100
    
    # 4. 'return' hands the final OUTPUT back to whatever part of the code called it.
    return percentage

# Using (Calling) the method
# We pass the data in, and capture the 'return' value into a new variable.
my_grade = calculate_grade(85, 100)
print(my_grade) # Output: 85.0
```

Now that we understand how parameters and returns work, let's apply them to our Assignment App!

### Step 3.1: Extracting the Data Layer
Instead of writing `with open(...)` everywhere, let's create dedicated data methods.

```python
def load_data(json_path):
    """Loads assignments from standard JSON."""
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(assignments, json_path):
    """Saves assignments array to JSON."""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(assignments, f, indent=4)
```

### Step 3.2: Extracting the Service Layer
When a user wants to add an assignment, we have to generate a UUID and format a dictionary. Let's pull that logic *out* of the Streamlit UI button click.

```python
def add_assignment(assignments, title, description, points, assignment_type):
    """Service layer method to create and append a new assignment."""
    import uuid
    new_assignment = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "points": points,
        "type": assignment_type
    }
    assignments.append(new_assignment)
    # Notice we don't return the list. Lists in Python are mutable so the original is updated automatically!
```
*Why?* If we ever build an automatic grading tool that generates assignments securely in the background, it can just call `add_assignment()` directly without needing a Streamlit Web Interface!

### Step 3.3: Extracting the UI Layer (The Add Form)
Now we take the `st.text_input` and `st.button` code specifically for the "Add New Assignment" screen and move it into its own targeted UI method: `show_add_new_assignment`. 

Notice how clean the "Save" button logic becomes because it purely delegates to our robust Service and Data methods!

```python
def show_add_new_assignment(assignments, json_path):
    """Renders the form to add a new assignment."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## Add New Assignment")
    with col2:
        if st.button("Back", key="back_btn", use_container_width=False):
            st.session_state["page"] = "Assignments Dashboard"
            st.rerun()

    # ... (Streamlit inputs capturing title, description, etc. into session_state['draft']) ...
    
    btn_save = st.button("Save", type="primary")

    if btn_save:
        with st.spinner("Recording..."):
            # 1. Call Service Layer Method
            add_assignment(
                assignments, 
                st.session_state['draft']['title'], 
                st.session_state['draft']['description'], 
                st.session_state['draft']['points'], 
                st.session_state['draft']['assignment_type']
            )

            # 2. Call Data Layer Method
            save_data(assignments, json_path)

            st.success("Saved!")
            st.session_state["page"] = "Assignments Dashboard"
            st.rerun()
```

### Step 3.4: Extracting the UI Layer (The Dashboard)
Next, we do the exact same thing for the main dashboard screen. We wrap the code that displays existing assignments into its own method:

```python
def show_dashboard(assignments, json_path):
    """Renders the main assignments list dashboard."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Assignments")
        
    with col2:
        if st.button("Add New Assignment", type="primary"):
            st.session_state["page"] = "Add New Assignment"
            st.rerun()
            
    for assignment in assignments:
        with st.container(border=True):
            st.markdown(f"**Assignment Title:** {assignment['title']}")
            # Edit button logic would go here
```

---

## 4. The Final App Architecture: The Main Router

### Step 4.1: Encapsulating the App in `main()`
At this point, we have successfully moved all our Data, Service, and UI code into distinct methods. But what about the remaining code? The initial file setup, the `st.session_state` initializations, and the `if/elif` blocks that decide which page to show?

We take this remaining code and place it into a master method called `main()`. 

**Why put this in `main()`?** 
It prevents global variables from loosely floating around our file, keeps the application highly organized, and acts purely as a central **Router** (Traffic Cop) that delegates the user to the correct UI method based on the current state.

```python
def main():
    st.title("Course Management App")
    st.divider()

    # 1. Initialization & Data Loading
    json_path = Path("assignments.json") 
    assignments = load_data(json_path)

    if "page" not in st.session_state:
        st.session_state["page"] = "Assignments Dashboard"
    if "draft" not in st.session_state:
        st.session_state["draft"] = {}

    # 2. Router (Traffic Cop)
    if st.session_state["page"] == "Assignments Dashboard":
        show_dashboard(assignments, json_path)
        
    elif st.session_state["page"] == "Add New Assignment":
        show_add_new_assignment(assignments, json_path)
```

### Step 4.2: Safely Executing the App

Finally, since everything in our file is now hidden inside methods, simply running the file will result in a totally blank screen! The methods exist, but nothing is telling Python to actually start executing them. We need to *call* `main()`.

We do this using a specific Python idiom at the very bottom of the file:

```python
if __name__ == "__main__":
    main()
```

**Why add this?**
This is a built-in safety lock. It tells Python: "Only run `main()` if I am running this file directly (e.g., typing `streamlit run app.py` in the terminal). Do not run it if I am simply importing this file into another script." This allows us to import our `load_data()` function elsewhere (like in a testing file) without accidentally triggering the Streamlit app to start drawing pages.

---

## 5. What NOT To Do: The "God Method" Anti-Pattern (Mixing Layers)

We just spent time carefully separating our UI, Service, and Data layers. However, a very common beginner mistake is to dump all three layers into a single function. This is often called a **"God Method"** because it tries to do everything itself.

Let's look at how someone might incorrectly write an "Edit Assignment" feature by failing to apply Separation of Concerns:

```python
def edit_assignment_bad(assignment_id, json_path):
    # 1. UI LAYER (Mixed in)
    st.markdown("## Edit Assignment")
    new_title = st.text_input("New Title")
    
    if st.button("Save Edit"):
        # 2. DATA LAYER (Mixed in) - Reading instead of calling load_data()
        with open(json_path, "r") as f:
            import json
            assignments = json.load(f)
        
        # 3. SERVICE LAYER (Mixed in) - Business Logic for updating
        for assign in assignments:
            if assign["id"] == assignment_id:
                assign["title"] = new_title
                break
                
        # 4. DATA LAYER (Mixed in) - Writing instead of calling save_data()
        with open(json_path, "w") as f:
            json.dump(assignments, f, indent=4)
            
        st.success("Updated!")
```

**Why is this a disaster for Reusability and Scalability?**
*   **Failed Reusability:** What if a teacher wants to computationally bulk-edit 50 assignment titles using an Excel spreadsheet upload? We can't reuse this `edit_assignment_bad()` method to update our data because invoking it would attempt to physically draw 50 `st.text_input` boxes and 50 `st.button` widgets onto the screen! The backend data logic is permanently trapped behind a visual button click.
*   **Failed Scalability:** If our university decides to replace Streamlit (Frontend) with a totally new web framework or a mobile app next semester, this entire method must be thrown into the trash. Because the core saving logic (`json.dump`) is locked tightly inside the Streamlit button's `if` statement, we lose all of our business rules just by changing the visual interface.

*Rule of thumb: Always keep your visual buttons (UI) separate from your computations (Service) and memory (Data)!*

---

## 6. Foreshadowing Classes

Methods definitely cleaned up our code! But notice how we always have to pass `assignments` around? 
`save_data(assignments, path)` 
`add_assignment(assignments, ...)`
`show_dashboard(assignments, path)`

Our functions and our data are completely separate entities. What if an Assignment knew how to save itself? What if we could just say `my_assignment.save()`? 

That is what **Object-Oriented Programming (Classes)** solves, and that is where we head next!