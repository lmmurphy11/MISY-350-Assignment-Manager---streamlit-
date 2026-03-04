# Streamlit Reviews: State Management, Dynamic Keys, and Layouts

This guide covers the critical next steps for your Streamlit application: fixing data update issues using **State Management**, ensuring the app refreshes correctly with **`st.rerun`**, and cleaning up the UI using the **Sidebar**.

---

## 0. Page Configuration
The `st.set_page_config` command allows you to customize how your app looks in the browser tab and how it behaves on load. **Important:** This must be the first Streamlit command in your script!

```python
st.set_page_config(
    page_title="Course Manager",      # Title shown in the browser tab
    page_icon="🎓",                   # Icon shown in the browser tab
    layout="centered",                # "centered" (default) or "wide"
    initial_sidebar_state="collapsed" # "expanded", "collapsed", or "auto"
)
```
*   **page_title:** Sets the tab name (so it doesn't just say "Streamlit").
*   **layout:** `centered` confines the app to a central column (good for forms). `wide` uses the full screen width (good for dashboards).
*   **initial_sidebar_state:** Controls if the sidebar is open or closed by default.

---

## 0.1. Understanding the `key` Argument
Before we dive into the bugs, we need to understand the most important argument in Streamlit widgets: `key`.

### What is a `key`?
Think of the `key` as the **ID card** for a widget. It tells Streamlit exactly which widget this is.
If you don't provide a `key`, Streamlit generates one automatically based on:
1. The **type** of widget (e.g., `text_input`).
2. The **label** (e.g., "Title").
3. The **order** it appears in your code.

### Why is it Important?
Streamlit destroys and rebuilds your app every time you interact with it. The `key` is the only way Streamlit remembers the state of a widget across these rebuilds.
- **Identity:** If two widgets have the same `key`, Streamlit thinks they are the same widget.
- **Persistence:** Streamlit stores the value of the widget in `st.session_state` using this key.

### Example
If you have a text input:
```python
name = st.text_input("Enter your name", key="user_name")
```
Streamlit stores the value in `st.session_state["user_name"]`. This is crucial when we start dynamically creating widgets inside loops or based on selections.

---

## 1. The "Sticky Input" Problem (State Management)
### The Issue
In your current "Update Assignment" tab, you might notice a bug. If you select "HW1", edit the title, and then switch the dropdown to "HW2", the text input might still show the text from "HW1".

### Why is this happening?
Streamlit widgets are identified by their `key`. 
```python
# Current Code in app_day4.py
edit_title = st.text_input("Title", key="edit_title", value=selected_assignment['title'])
```
Because the `key` is always `"edit_title"`, Streamlit thinks this is the **same widget** every time the app reruns. 
1. Streamlit remembers the last thing you typed into the widget with key `"edit_title"`.
2. Even though you changed the `value` parameter in your code (from HW1 to HW2), Streamlit prioritizes the **user's last input state** for that specific widget ID.

### The Fix: Dynamic Keys
To force Streamlit to treat the input box as a *brand new widget* when you switch assignments, we need a unique key that changes whenever the selection changes. We can do this by appending the assignment's ID (or title) to the key string.

```python
# 1. Get a unique identifier from the selected item
current_id = selected_assignment['id']

# 2. Embed that ID into the key
edit_title = st.text_input(
    "Title", 
    value=selected_assignment['title'],
    key=f"edit_title_{current_id}"  # e.g., "edit_title_HW1"
)
```
**Result:** When you switch from HW1 to HW2, the key changes from `"edit_title_HW1"` to `"edit_title_HW2"`. Streamlit discards the old widget and creates a fresh one with the correct new value.

---

## 1.5. Dynamic vs. Static Keys & Best Practices
Now that you've seen both types, how do you decide which to use?

### When to use Static Keys (`key="fixed_name"`)
Use static keys for widgets that represent a **permanent part of your UI** that should retain its state regardless of other actions.
*   **"Create" Forms:** Fields like "New Title" shouldn't clear just because you clicked a sidebar button. 
*   **Sidebar Filters:** Your search box or filters should persist while you browse results.
*   **Navigation:** Tabs or radio buttons for changing views.

### When to use Dynamic Keys (`key=f"name_{id}"`)
Use dynamic keys when a **single widget instance re-purposes itself** to display different data.
*   **Edit Forms:** As seen above, one set of inputs displays data for many different items.
*   **Loops:** If you generate buttons inside a `for` loop, every button needs a unique key.
    ```python
    for item in items:
        st.button("Delete", key=f"btn_del_{item['id']}")
    ```

### Naming Conventions: The "Action_Context_ID" Rule
As your app grows, `st.session_state` will get crowded. Using a consistent naming scheme helps you debug and avoid duplicate key errors.

**Bad Names:** `key="text1"`, `key="button"`, `key="val"`

**Good Pattern:** `[action]_[field]_[identifier]`
1.  **create_title:** (Action: create, Field: title)
2.  **update_desc_HW1:** (Action: update, Field: description, ID: HW1)
3.  **search_sidebar_query:** (Action: search, Context: sidebar, Field: query)

**Why this helps:**
If you look at `st.session_state`, you instantly know what each value does:
```python
{
    "create_title": "Database Lab",
    "update_title_HW1": "Intro to SQL",
    "sidebar_filter": "Homework"
}
```

---

## 2. Immediate Updates with `st.rerun`
### The Issue
When you click "Save" or "Update", you update the `assignments` list or the JSON file. However, the code for the "View" tab (which is usually at the top of your script or in `tab1`) has **already run** by the time the button is clicked at the bottom.
Result: You save a new assignment, but it doesn't appear in the table until you click something else.

### The Fix
Trigger a rerun immediately after saving data. This restarts the script from top to bottom, ensuring the "View" tab re-reads the updated data file.

```python
if update_btn:
    # ... (save logic) ...
    
    st.success("Assignment Updated!")
    st.rerun() # Restarts the app immediately
```

---

## 3. Sidebar Navigation (`st.sidebar`)
The sidebar is perfect for global controls (like user settings, file operations, or admin buttons) that should remain visible regardless of which tab is active.

### Implementation
You can use `st.sidebar` just like `st.container` or `st.columns`.

```python
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Course Admin")
    st.header("Settings")
    
    # Example: Global Toggle
    auto_save = st.checkbox("Auto-save mode", value=True, key="sidebar_autosave")
    
    st.divider()
    
    # Example: Admin Action
    if st.button("Clear All Assignments", key="sidebar_clear_btn"):
        st.error("Admin access required!")
```

---

## 4. Enhanced Edit Form (Radio Buttons & Logic)
Currently, you might be displaying the "Type" as simple text or not allowing it to be edited. Let's add a Radio Button to the update form so users can change an assignment from "Homework" to "Lab".

```python
# In Tab 3 (Update)

# 1. Determine the index of the current type to set the radio button correctly
# We need to know if the current type is "Homework" (index 0) or "Lab" (index 1)
type_options = ["Homework", "Lab"]
try:
    current_index = type_options.index(selected_assignment['type'])
except ValueError:
    current_index = 0

# 2. Create the Radio Button with a Dynamic Key
new_type = st.radio(
    "Assignment Type", 
    options=type_options,
    index=current_index,
    horizontal=True,
    key=f"edit_type_{selected_assignment['id']}" # Dynamic Key!
)

# 3. Use 'new_type' when saving the object
# selected_assignment['type'] = new_type
```

---

## 5. Advanced Selection: Handling Duplicate Titles
### The Issue
Currently, we create a list of titles `[a['title'] for a in assignments]` and pass that to `st.selectbox`.
**Problem:** What if you have two assignments named "Homework 1"?
1. The dropdown will show "Homework 1" twice (confusing).
2. When you select the second one, your code to find the object (`if item["title"] == selected_title`) will always find the **first** match. You will never be able to edit the second one!

### The Fix: Pass Objects, Not Strings
Streamlit allow you to pass the actual list of dictionaries to `options`. But wait—if you do that, the dropdown will show `{'id': '...', 'title': '...'}` which looks terrible.

### The `format_func` Solution
We can direct Streamlit on how to *display* the object using `format_func`.

```python
# Pass the FULL LIST of objects, not just titles
selected_assign = st.selectbox(
    "Select Assignment",
    options=assignments, 
    # Lambda function: Takes the object 'x' and returns a string
    format_func=lambda x: f"{x['title']} ({x['type']})",
    key="advanced_selection_box"
)

# precise selection!
st.write(f"You selected ID: {selected_assign['id']}")
```

**Benefits:**
1. **Handles Duplicates:** Even if titles are the same, the objects are different in memory (or have different IDs), so Streamlit treats them as distinct options.
2. **Cleaner Code:** `selected_assign` **IS** the assignment object. You don't need the loop `for item in assignments: if item['title'] == ...` anymore!

---

## 6. Delete Assignment Functionality
Finally, let's implement the ability to remove assignments using the `remove()` method and our new `format_func` trick.

### Implementation
We will use a similar selection method as above to ensure we are deleting the *exact* assignment the user wants.

```python
with tab4: # Assuming you created a 4th tab
    st.markdown("## Delete Assignment")
    
    if len(assignments) > 0:
        # 1. Select the object directly
        # format_func is crucial here to distinguish between items with same title
        selected_to_delete = st.selectbox(
            "Select Assignment to Delete",
            options=assignments,
            format_func=lambda x: f"{x['title']} (ID: {x['id']})",
            key="delete_select"
        )
        
        # 2. Show a confirmation warning
        st.warning(f"Are you sure you want to delete **{selected_to_delete['title']}**?")
        st.write(f"Description: {selected_to_delete['description']}")
        
        # 3. The Delete Action
        if st.button("Confirm Delete", type="primary", key="confirm_delete_btn"):
            # Remove the object from the list
            assignments.remove(selected_to_delete)
            
            # Save the updated list to JSON
            with open(json_file, "w") as f:
                json.dump(assignments, f, indent=4)
            
            st.success("Deleted successfully!")
            st.rerun()
    else:
        st.info("No assignments to delete.")
```