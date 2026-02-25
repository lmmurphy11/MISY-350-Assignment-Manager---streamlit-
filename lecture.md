# Streamlit UI Mastery: Building the Dashboard (Module 3) - Student Workbook
*Turning Data Logic into a Modern Web Application*

**Goal:** By the end of this module, you will have a running web app that can Create, Read, Update, and Delete assignments using a graphical interface, following the exact structure of the `app.py` file being built.

## Week Plan
**Monday:** Segments 0-3 (Setup through "Add Assignment" Inputs)
**Wednesday:** Segments 4-6 (Navigation, Search, and JSON Persistence)

---

## 0. Project & Repo Setup (The Foundation)
**Goal:** Create the project repo, install tools, and create the blank `app.py`.

### Step A: Create the GitHub Repository (Manual)
1.  Go to GitHub and click **New repository**.
2.  Set the repository name to `assignment-manager-streamlit`.
3.  Create the repo and copy its HTTPS URL.

### Step B: Create the Local Project Folder & Connect
1.  Create `assignment-manager-streamlit` folder locally.
2.  Open in VS Code.
3.  Run terminal commands:
    ```bash
    # TODO: Initialize git
    # TODO: Rename branch to main
    # TODO: Add remote origin
    ```

### Step C: Installation
1.  Install Streamlit:
    ```bash
    # TODO: Pip install command
    ```
2.  Create `requirements.txt`:
    ```txt
    streamlit
    ```

### Step D: Create & Run `app.py`
1.  Create `app.py` in the root.
2.  Run the server:
    ```bash
    # TODO: Streamlit run command
    ```

---

## 1. Step 1: Header First (Text Elements)
**Matches `app.py` Step 1**
*From "Script" to "Application UI".*

In the "Course Manager" running case, we need an interface that looks organized. We start by establishing the visual hierarchy.

### Concept: Streamlit Text Hierarchy
*   **`st.title`:** The main name of the application.
*   **`st.header`:** Major divisions.
*   **`st.caption`:** Small text for context.
*   **`st.divider`:** A visual separator line.

### Code Implementation
```python
import streamlit as st

# TODO: Set page configuration
# st.set_page_config(...)

# ============================================================
# Step 1: Header first
# TODO: Add Title
# TODO: Add Header
# TODO: Add Caption
# TODO: Add Divider
```

---

## 2. Step 2: Define Assignments List (Data Continuity)
**Matches `app.py` Step 2**
*Connecting to Week 2 Logic.*

We need data to display. Just like Week 2, we use a list of dictionaries. This acts as our "In-Memory Database".

### Concept: In-Memory Data Structures
- Week 2 built the **data engine** using lists and dictionaries.
- Week 3 builds the **UI layer** on top of that same structure.

### Code Implementation
```python
# ============================================================
# Step 2: Define assignments list (Week 2 continuity)
assignments = [
    # TODO: Create a list of dictionaries representing assignments
    # Each dictionary should have: id, title, description, points, due_date, type, available, resource_name
]
```

---

## 3. Step 3: Add New Assignment Section (Inputs & Layout)
**Matches `app.py` Step 3**
*Capturing user data and organizing the screen.*

This section covers the core of Streamlit's input widgets and layout tools.

### Concept A: Input Widgets
Streamlit provides widgets for every data type:
- **`st.text_input`**: Single line text.
- **`st.number_input`**: numeric values (int/float).
- **`st.text_area`**: Multi-line paragraphs.
- **`st.date_input`**: Date pickers.
- **`st.selectbox`**: Dropdowns.
- **`st.checkbox`**: boolean True/False.
- **`st.file_uploader`**: Handling files.

### Concept B: Layout (Columns & Containers)
A professional app groups related information.
- **`st.columns`**: Splits the screen horizontally.
- **`st.container`**: logical grouping of elements (often with a border).

### Concept C: Buttons & Feedback
- **`st.button`**: Triggers an event *once*.
- **`st.spinner`**: Shows loading state.
- **`st.success/warning/error`**: Feedback messages.

### Code Implementation
```python
# ============================================================
# Step 3: Add New Assignment section
st.subheader("Add New Assignment")

# TODO: Create a container with border=True
    # TODO: Create columns for Title and Points
    # TODO: Create text input for Title
    # TODO: Create number input for Points

    # TODO: Create text area for Description

    # TODO: Create columns for Due Date, Type, and File Upload
    # TODO: Add remaining input widgets

    # TODO: Add checkbox for availability

    # TODO: Display Live Preview using Markdown

    # Button Logic
    # if st.button("Create Assignment"):
        # TODO: Validate title is not empty
        # TODO: Create new assignment dictionary
        # TODO: Append to assignments list
        # TODO: Show success message
```

---

## 4. Step 4: Navigation & Control Flow
**Matches `app.py` Step 4**
*Controlling what the user sees.*

We introduce "Pages" within a single script using conditional logic.

### Concept: The `if/elif` Control Flow
Streamlit scripts run top-to-bottom. We can use a radio button to determine which "branch" of code executes. This simulates having multiple pages.

- **`st.radio`**: Serves as our "tab" selector.
- **Search Logic**: Implementing simple string matching loops (Week 2 logic) inside the UI.

### Code Implementation
```python
# ============================================================
# Step 4: Introduce radio buttons as tabs + if/elif flow
st.divider()
st.header("Navigation Step: Radio Buttons + if/elif")

# TODO: Create radio button for navigation (Assignments, Add, Search, etc.)
# nav_selection = st.radio(...)

# TODO: Implement if/elif logic for each selection

# if nav_selection == "Assignments":
    # TODO: Show dataframe

# elif nav_selection == "Add New Assignment":
    # TODO: Show placeholder for Add form

# elif nav_selection == "Search Assignments":
    # TODO: Add text input for search query
    # TODO: Loop through assignments and find matches
    # TODO: Display results
```

---

## 5. Step 5: Sidebar Navigation
**Matches `app.py` Step 5**
*Moving navigation to the side.*

Streamlit offers a special reserved area called the Sidebar for global controls.

### Concept: `st.sidebar`
The `with st.sidebar:` block places any widget (buttons, headers, inputs) into the collapsible side menu.

### Code Implementation
```python
# ============================================================
# Step 5: Sidebar Navigation

with st.sidebar:
    st.header("Course Manager")
    # TODO: Add Home button
    # TODO: Add Logout button
    st.info("Version 1.0.0")

# TODO: Handle sidebar button clicks
```

---

## 6. Step 6: JSON Persistence (Saving Data)
**Matches `app.py` Step 6 hierarchy**
*Making data survive the "Rerun".*

So far, every time we click a button, the script reruns and `assignments` resets to the hardcoded list. We need a file to store changes.

### 6.1 Create or Load JSON
We use Python's `pathlib` and `json` libraries.
- Check if file exists.
- If yes, load it.
- If no, use default list.

```python
import json
from pathlib import Path

json_path = Path("assignments.json")
json_records = []

# TODO: Check if file exists
# TODO: If yes, load with json.load()
# TODO: Else, use current assignments list
```

### 6.2 Data Cleaning (Conversions)
JSON stores everything as simple types. When reading back, we often need to ensure:
- Numbers are `int` not `str`.
- Dates are strings (JSON doesn't have a Date type).

```python
# Step 6.3 in app.py logic
# TODO: Loop through json_records and ensure types are correct (int for points)
```

### 6.3 Appending & Saving
To save a new assignment, we append to the list and write the entire list back to the file.

```python
# Step 6.5 in app.py logic
if st.button("Save File"):
    # TODO: Append new assignment to records
    # TODO: Open file in write mode
    # TODO: Dump clean_records to file
    st.success("Saved assignments.json")
```

---

## Final Review: The Mental Model
1.  **Rerun Cycle:** Streamlit reruns the *entire* script from top to bottom whenever an interaction occurs.
2.  **Persistence:** Variables reset on rerun unless stored in `st.session_state` or a file (like `assignments.json`).
3.  **Control Flow:** The UI is just a reflection of the current variables and `if` statements.

---

## Appendix: Useful Concepts (Not in `app.py` but good to know)
The following concepts were in the original curriculum but are not strictly used in the `app.py` structure. They are useful for expanding your app later.

### A. Alternative Layout Goals
While `app.py` uses `st.radio` for navigation and `st.container` for grouping, Streamlit offers other powerful layout tools.

**1. Tabs (`st.tabs`)**
good for switching views without reloading the whole page logic (like `st.radio` but visually different).
```python
# TODO: Create tabs
```

**2. Expander (`st.expander`)**
Great for hiding advanced options or "Show More" details.
```python
# TODO: Create expander
```

### B. Session State (`st.session_state`)
In `app.py`, we used a file (`assignments.json`) to save data. However, sometimes you want to remember things *temporarily* while the user is on the page (like which tab is active, or a counter), without saving to a file.

```python
# Example pattern
# if "key" not in st.session_state:
#     st.session_state.key = value
```

### C. Metrics (`st.metric`)
For building dashboard headers.
```python
# TODO: Create a metric
```

### D. Item Keys (`key`)
Streamlit tracks widgets by their type and label. If two widgets look identical (e.g., two "Save" buttons), Streamlit gets confused. Assigning a unique `key` solves this.

```python
# st.button("Save", key="unique_key_1")
```

### E. Dataframe vs. Table
- **`st.dataframe`**: Interactive, sortable, scrollable. Ideally for lists of dicts.
- **`st.table`**: Static, shows all rows at once. Good for small summaries.

### F. Performance (`st.cache_data`)
Wraps a function so it doesn't re-run on every script rerun. Useful for expensive database queries or file reads.

```python
# @st.cache_data
# def load_data():
#     return data
```

---

## Appendix: CSV Version (Optional)
*Alternative workflow if you want to teach local persistence with CSV instead of JSON.*

**CSV columns:** `id,title,description,point`

### Step 1: Create `assignments.csv`
Create a file named `assignments.csv` in the root folder with this header:
```csv
id,title,description,point
```

### Step 2: Read CSV Records
```python
import csv
csv_records = []
csv_path = Path("assignments.csv")

# TODO: Check if file exists
# TODO: Read with csv.DictReader
```

### Step 3: Save to CSV
```python
if st.button("Save to CSV"):
    # TODO: Append to list
    # TODO: Write specific fields using csv.DictWriter
    pass
```