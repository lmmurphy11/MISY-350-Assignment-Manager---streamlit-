#

In this practice session, you will build the foundational user interface for our upcoming "Course Manager" application. You will implement data loading, a registration form, and a login form.

By the end of this session, you will have a working Python script that can read/write user data to a file and display interactive forms.

---

## 1. Project Setup

Create a new file named `app_login_ui.py`.

### Step 1: Imports and Page Config
Start by importing the necessary libraries and configuring the page layout.

**Requirements:**
*   Import `streamlit`, `json`, `pathlib`, `datetime`, `uuid`, and `time`.
*   Set the page title to "Course Manager".
*   Set the layout to "centered".

### Step 2: Data Loading Logic
We need a way to store our users permanently. We will use a simple `users.json` file.

**Task:**
1.  Initialize a variable `json_file` pointing to `"users.json"`.
2.  If the file exists, load its content into a list variable called `users`.
3.  If the file does *not* exist, initialize `users` with a default Admin account (see below).

**Default Admin User Structure:**
```json
{
    "id": "1",
    "email": "admin@school.edu",
    "full_name": "System Admin",
    "password": "123ssag@43AE",
    "role": "Admin",
    "registered_at": "..."
}
```

---

## 2. Navigation and Page Structure

Instead of showing both forms at once, we want to let the user choose between **Register** and **Login**.

### 🧰 The Streamlit Toolbox
Use the following elements to build your UI. You decide how to combine them!

*   **Navigation:** `st.sidebar`, `st.radio`, `st.selectbox` (or `st.tabs` if you prefer).
*   **Inputs:** `st.text_input` (don't forget `type="password"`), `st.button`.
*   **Layout:** `st.container`, `st.columns`, `st.expander` (use them to organize your page).
*   **Feedback:** `st.success`, `st.error`, `st.spinner`.
*   **Data:** `st.dataframe` (to see your JSON data updates).

**Challenge:** Implement a navigation mechanism (in the sidebar or main page) that toggles between displaying the Registration Form and the Login Form.


---

## 3. The Registration Form

If the user selects "Register", show the "New Instructor Account" form.

**Task:**
    *   Email Address
    *   First and Last Name
    *   Password (make sure to mask the input using `type="password"`)
3.  Add a selectbox for Role (default to just `["Instructor"]` for now).
4.  Add a "Create Account" button.

**Button Logic:**
When the button is clicked:
1.  Display a spinner "Creating your account...".
2.  Simulate a delay.
3.  Append a new user dictionary to your `users` list. 
4.  Write the updated `users` list back to `users.json`.
5.  Show a success message: "Account created successfully!".

---

## 4. The Login Form and Data Display

If the user selects "Login", show the login interface.

**Task:**
1.  **Login Form:**
    *   Add inputs for Email and Password.
    *   Add a "Log In" button.

2.  **Login Button Logic:**
    When the button is clicked:
    *   Display a spinner "Verifying credentials...".
    *   Iterate through your `users` list to find a match.
    *   **If found:** Display a success message with the user info
    *   **If not found:** Display `st.error("Invalid email or password.")`.

3.  **User Database Display:**
    *   Below the login form (outside the container), display the current list of users using `st.dataframe(users)` or `st.table(users)`. This helps you verify that new registrations are actually being saved.

---

## 5. Critical Verification

Run your app (`streamlit run app_login_ui.py`) and perform this specific test:

1.  **Register:** Create a new user account. Verify that the new user appears in the table on the Login page.
2.  **Login:** Go to the Login page and enter the correct credentials for your new user.
3.  **Observe:** You should see the green "Welcome back" success message.
4.  **The Test:** While that success message is visible, click *any other button* or change the sidebar selection.
5.  **The Question:** Does the success message stay on the screen? Or does the app "forget" that you just logged in?


---

## Appendix: Getting the Current Time

To record when a user registers, you will need the `datetime` library.

1.  **Import it:** You should already have `from datetime import datetime` at the top of your file.
2.  **Get the time:** `datetime.now()` returns the current timestamp.
3.  **Convert to String:** JSON files strictly handle text, numbers, and lists. They cannot save Python "datetime objects". You must convert the time to a string using `str()`.

**Example:**
```python
# Correct way to save to JSON
"registered_at": str(datetime.now())
```