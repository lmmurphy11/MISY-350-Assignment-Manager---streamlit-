# Module 3 Curriculum: From Stateless to Stateful

We've been building apps that reaction to *one interaction at a time*. Today, we face a major limitation of that approach: **Amnesia**.

## Learning Objectives

In this module, you will learn to master the following core concepts:

### 🧠 1. Session State (`st.session_state`)
**The "Brain" of the App.** It remembers data when Streamlit reruns.
*   **Concept:** Normal variables (like `found_user`) disappear every time the app reruns. Session State behaves like a permanent dictionary that survives.
*   **Where to find it:** Steps 1 & 2 illustrate initializing and saving to session state.
*   **Key Insight:** If you want the app to remember "I am logged in" or "Who am I?", you *must* store it here.

### 🚦 2. Role-Based Routing (The Traffic Cop)
**Controlling Access.** Deciding what to show based on *who* is logged in.
*   **Concept:** Using `if` / `elif` / `else` blocks to check `st.session_state["role"]`.
*   **Where to find it:** Step 3 (The Traffic Cop).
*   **Key Insight:** Security in a single-file app is primarily about "hiding" code blocks (like the Admin Dashboard) from users who don't have the right "key" (role).

### 🧭 3. State-Driven Navigation
**Moving between screens.** Using state to switch views inside the same app.
*   **Concept:** Changing a variable like `st.session_state["page"] = "register"` and rerunning the app causes it to draw the Register screen instead of the Login screen.
*   **Where to find it:** The Guest View logic in "The Final Result".
*   **Key Insight:** You aren't actually navigating to a new URL; you are just telling Streamlit to draw a different set of widgets on the next repaint.

---

## The Big Picture Analogy: The Goldfish vs. The Notebook

Before we dive in, here's a mental image to carry through all of today's work:

Imagine a cashier who **forgets every customer** the moment they look away. A customer walks up, orders a coffee, and the cashier starts making it. But then the cashier blinks, looks back, and says: "Hi! Welcome! What can I get you?" That's your Streamlit app right now — **a goldfish**.

`st.session_state` is a **notebook the cashier keeps on the counter**. Every time they help a customer, they jot down a note: "Customer #4, ordered a latte, already paid." Now, even when the cashier blinks (the app reruns), they glance at the notebook and pick up right where they left off.

Today, we're giving your app a notebook.

---

## 1. The Starting Point (The Broken App)

Let's start with the code we have right now in `app_day6.py`. It looks like a complete application. It has user loading, registration, and login logic. It even has loading spinners!

We will build the `app.py` file in three parts.

### Part 1: Setup and Data Loading

Copy this to the top of your `app.py`:

```python
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Course Manager", layout="centered")
st.title("Course Manager App")

# --- DATA LOADING ---
json_file = Path("users.json")
users = []
if json_file.exists():
    with open(json_file, "r") as f:
        users = json.load(f)
```

### Part 2: Login Section

Add this code below Part 1. It handles user authentication:

```python
# --- LOGIN ---
st.subheader("Log In")
with st.container(border=True):
    email_input = st.text_input("Email", key="login_email")
    password_input = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Log In"):
        with st.spinner("Logging in..."):
            time.sleep(2) # Fake backend delay
            
            # Find user
            found_user = None
            for user in users:
                if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                    found_user = user
                    break
            
            if found_user:
                st.success(f"Welcome back, {found_user['email']}!")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid credentials")
```

### Part 3: Registration Section

Finally, add the registration logic at the bottom:

```python
# --- REGISTRATION ---
st.subheader("New Instructor Account")
with st.container(border=True):
    new_email = st.text_input("Email Address", key="reg_email")
    new_password = st.text_input("Password", type="password", key="reg_password")
    
    if st.button("Create Account"):
        with st.spinner("Creating account..."):
            time.sleep(2) # Fake backend delay
            # ... (Assume validation logic here) ...
            users.append({
                "id": str(uuid.uuid4()),
                "email": new_email,
                "password": new_password,
                "role": "Instructor"
            })
            with open(json_file, "w") as f:
                json.dump(users, f, indent=4)
            st.success("Account created!")
            st.rerun()

st.write("---")
st.dataframe(users)
```

### 🛑 Critical Review: The "Duplicate Key" Trap

**⚠️ Warning:** If you run the code above exactly as written, your app will crash with this error:

> **DuplicateWidgetID:** There are multiple identical st.text_input widgets with the same label 'Password'.

### Why does this happen?
Streamlit identifies every widget by its **label**.
1. In the **Login** section, you have: `st.text_input("Password", type="password")`
2. In the **Registration** section, you have: `st.text_input("Password", type="password")`

Streamlit gets confused: *"I see 'Password' twice. Which one is which?"*

### The Solution: Unique Keys
Every widget must have a unique identifier. If the labels are the same (like "Password"), you must provide a `key` argument to tell them apart.

**Update your code with these keys:**

**1. Login Section:**
```python
email_input = st.text_input("Email", key="login_email")
password_input = st.text_input("Password", type="password", key="login_password")
```

**2. Registration Section:**
```python
new_email = st.text_input("Email Address", key="reg_email")
new_password = st.text_input("Password", type="password", key="reg_password")
```

---

### The Issue

Try to log in.
1. You enter your email/password.
2. You click "Log In".
3. The spinner spins... "Logging in..."
4. You see "Welcome back!" for a brief second.
5. The app reruns... **and you are back at the Login screen.**

### Why does this happen?
Streamlit runs **Top-to-Bottom** every time something changes.
1. When you clicked "Log In", the script ran, found the user, and printed "Welcome".
2. Then it hit `st.rerun()`.
3. Streamlit went back to line 1.
4. It cleared all variables (`found_user` is gone).
5. It redrew the screen. Since `found_user` is gone, it just draws the Login form again.

The app has **Amnesia**. It cannot remember what happened 5 seconds ago.

### Tracing Two Runs Side by Side

Here is exactly what happens across two consecutive runs:

```
Run 1 (user clicks "Log In"):
  line 1  → import libraries
  line 10 → load users.json
  line 15 → draw login form (email & password already filled in)
  line 20 → button was clicked → enters the if-block
  line 22 → found_user = {"email": "ali@example.com", ...}  ← EXISTS!
  line 25 → st.success("Welcome back!")  ← user sees this briefly
  line 26 → st.rerun()  ← IMMEDIATELY restarts the script

Run 2 (automatic rerun):
  line 1  → import libraries
  line 10 → load users.json
  line 15 → draw login form
  line 20 → button was NOT clicked this time → skips the if-block
  line 22 → found_user is NEVER CREATED  ← gone!
  ...      → login form is drawn again, as if nothing happened
```

### Wait — then why do we call `st.rerun()` at all?

Good question. `st.rerun()` is **not** the villain here. It's how we tell Streamlit: "I just changed something important — please redraw the screen now so the user sees the update." The real problem is that we changed a **temporary variable** (`found_user`) instead of saving to **permanent memory** (`st.session_state`). If we save first and *then* rerun, the new screen will reflect the saved state.

---

## Mental Model: What Resets and What Survives?

When you use Streamlit, your script is not "running forever" like a traditional loop. Instead, Streamlit re-executes your file from **top to bottom** every time the user interacts with the app.

Think of each interaction as creating a **new run** of the script:

1. The app starts at line 1.
2. It builds the page.
3. The user clicks a button or types in a widget.
4. Streamlit starts the script again from line 1.

That means you need to be very clear about **where your data lives**.

| Where the data lives | Example | Does it survive a rerun? | Scope / Lifetime | Why? |
|---|---|---|---|---|
| Normal Python variable | `found_user`, `email`, `password` | No | One script run | These variables exist only during the current script run. |
| Button click result | `if st.button("Log In"):` | Only for one run | One script run | A button click is an event, not permanent memory. |
| Widget state | text inside `st.text_input(..., key="login_email")` | Usually yes | One browser session | Streamlit reconnects the widget to the same key on the next rerun. |
| Session State | `st.session_state["user"]` | Yes | One browser session | Streamlit stores it for that user's browser session. |
| File on disk | `users.json` | Yes | Permanent (disk) | The data is saved outside the script and can be loaded again. |
| `st.rerun()` | `st.rerun()` | N/A — not storage | Instant (trigger only) | This is not a place to store data. It is a *trigger* that causes a fresh top-to-bottom execution. It restarts the script immediately. |

### What disappears on rerun?

- Temporary variables like `found_user`
- Success/error messages from the previous run
- Any logic result that was never saved anywhere permanent
- The `True` result from a button click after that run is over

### What survives rerun?

- Values stored in `st.session_state`
- Widget values when the same widget appears again with the same key
- Data saved to a file such as `users.json`

### Why this matters for login

In our broken app, `found_user` is just a normal variable. It exists during the login click, but after `st.rerun()` the app starts over and `found_user` is gone.

So the key lesson is:

**If the app must remember something after a rerun, store it in `st.session_state` or save it outside the app (for example, in a file or database).**

---

## 2. The Solution: `st.session_state`

`st.session_state` is a dictionary that **survives** reruns. It is the app's "Brain".

To fix our app, we need to stop relying on temporary variables and start storing the "State of the User" in this permanent dictionary.

### Step 1: Initialize the State

At the very top of your app (after imports), we need to set up our default values. If the app is opening for the first time, we assume the user is **not** logged in.

**Add this to the top of your file:**

```python
# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None 

if "page" not in st.session_state:
    st.session_state["page"] = "login" # or 'register'
```

> **Why the `if "key" not in` check?**
>
> Remember, this file runs from top to bottom on *every single interaction*. Without the guard, we'd reset `logged_in` back to `False` every time the user clicks *anything* — undoing our own login! The `if "logged_in" not in st.session_state` pattern means: **"Only set the default the very first time. After that, leave it alone."**
>
> This is one of the most common beginner mistakes. If you ever find that your app "forgets" your login after clicking a button, check whether you accidentally initialize without the guard.

---

## 3. Step 2: Saving "Who I Am" (The Login Logic)

Now, look at your Login button code. Currently, it just prints a success message and then forgets everything.

We need to change it so it **saves** the user into our new `st.session_state` dictionary.

**Change your Login Button code to this:**

```python
    if st.button("Log In", type="primary"):
        with st.spinner("Logging in..."):
            time.sleep(2)
            
            # ... (search for user logic) ...
            
            if found_user:
                # 1. SAVE the user to session state (The App remembers!)
                st.session_state["logged_in"] = True
                st.session_state["user"] = found_user
                st.session_state["role"] = found_user["role"] # The Role is Critical!
                
                st.success("Login Successful!")
                time.sleep(1)
                st.rerun()  # Force a redraw immediately
            else:
                st.error("Invalid credentials")
```

Now, when `st.rerun()` happens, Streamlit goes back to line 1, BUT `st.session_state["logged_in"]` is still `True`!

---

## 4. Step 3: The "Traffic Cop" (Role-Based Access Control)

We have memory now, but we are still drawing the Login form constantly. We need a **Router** (or a Traffic Cop). We use `if` statements to decide *what* to draw based on our memory.

> **Pattern: State-Driven Rendering**
>
> Instead of having multiple HTML pages or separate URLs, we use a **single Python file** that draws *different content* depending on what's stored in memory. Think of it like a theater stage: the same stage can show Act 1 or Act 2 — the stagehands just swap out the scenery. `st.session_state["role"]` tells the stagehands which scenery to use.
>
> This is a recognized UI design pattern. It's the same idea behind single-page applications (SPAs) in web development, where one page dynamically changes its content instead of loading new pages.

In this design, we check the **Role** first. If the role is `None` (which is our default), we treat them as a Guest.

> **Two Levels of Routing: `role` vs. `page`**
>
> You'll notice we use *two* different state variables for navigation:
> - **`role`** controls the **major view**: Admin Dashboard vs. Instructor Dashboard vs. Guest screens.
> - **`page`** controls **sub-navigation within the Guest view**: the login form vs. the registration form.
>
> Once someone is logged in, `page` doesn't matter anymore — `role` takes over. Think of `role` as choosing the building, and `page` as choosing the room inside that building.

**Refactor your main app logic into three blocks:**

```python
if st.session_state["role"] == "Admin":
    st.header("Admin Dashboard")
    st.success(f"Hello, {st.session_state['user']['full_name']} ({st.session_state['role']})")
    
    # Logout button
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.rerun()

elif st.session_state["role"] == "Instructor":
    st.header("Instructor Dashboard")
    st.success(f"Welcome, {st.session_state['user']['full_name']}!")
    
    # Logout button
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.rerun()

else:
    # GUEST VIEW (Login or Register)
    if st.session_state["page"] == "login":
        # ... Show Login Form ...
        pass
    else:
        # ... Show Register Form ...
        pass
```

---

## 5. The Final Result

Here is how the pieces fit together. Note how the **Logic** (saving state) and the **UI** (if/elif/else blocks) work together.

```python
# [TODO] Your complete code should go here.
```

---

## 6. Common Mistakes

As you build with session state, watch out for these frequent pitfalls:

### Mistake 1: Forgetting the Guard on Initialization
```python
# WRONG — resets state on every rerun!
st.session_state["logged_in"] = False

# RIGHT — only sets the default the first time
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
```
Without the `if not in` check, every click resets your app back to "not logged in."

### Mistake 2: Expecting Code After `st.rerun()` to Execute
```python
st.rerun()  # Script restarts IMMEDIATELY from line 1
st.success("This will NEVER display!")  # Dead code
```
`st.rerun()` is like hitting a reset button. Anything written after it on the same line path will never run. Always put your success messages and state changes *before* calling `st.rerun()`.

### Mistake 3: Putting Logout Logic Outside the Role Block
If you place the logout button outside the `if/elif/else` structure, *everyone* sees it — including guests who aren't even logged in. Always keep UI elements inside their role's block.

### Mistake 4: Forgetting to Reset `user` on Logout
```python
# INCOMPLETE — leaves stale user data in memory
st.session_state["logged_in"] = False
st.session_state["role"] = None
# Forgot: st.session_state["user"] = None
```
If you only reset `role` but not `user`, the old user's data is still floating around in session state. Always reset **all** related keys when logging out.

---

## 7. A Note on Security

The role-based routing we built today is **UI-level gating** — it controls what the user *sees*, not what they *can access* at a deep system level. In a real production application:

- Passwords should **never** be stored in plaintext (use hashing libraries like `bcrypt`).
- The `users.json` file is readable by anyone with access to the server.
- A determined user could potentially manipulate session state.

For a classroom exercise, this approach is perfectly fine for learning the concepts. Just be aware that production authentication requires additional layers of security (encrypted passwords, server-side session management, HTTPS, etc.).

---

## 8. When Should You Call `st.rerun()`?

You may have noticed that we call `st.rerun()` in some places (after login, after registration, after logout) but not others (the dashboards just display content). Here's the rule of thumb:

**Call `st.rerun()` when you've changed state and want the screen to immediately reflect it.**

- After login → role changed → need to jump from Guest view to Dashboard → `st.rerun()`
- After logout → role cleared → need to jump back to Login form → `st.rerun()`
- After switching pages → page changed → need to swap login/register forms → `st.rerun()`
- Displaying a dashboard → nothing changed → no need to rerun

If you call `st.rerun()` when nothing has changed, you'll create an infinite loop and Streamlit will stop your app.

---

## Recap: Three Things You Learned

1. **Session State is your app's memory.** Without it, every rerun starts from scratch. Use `st.session_state` to store anything the app needs to remember between interactions — like who is logged in and what role they have.

2. **Role-based routing is just `if/elif/else`.** You decide what to draw based on who's logged in. The same Python file can render completely different screens depending on the value of `st.session_state["role"]`.

3. **State-driven navigation replaces URLs.** Changing a value in `st.session_state` and calling `st.rerun()` is how you "navigate" in a single-file Streamlit app. You're not loading a new page — you're telling Streamlit to repaint the same page with different content.

Think back to our analogy: your app started as a goldfish. Now it has a notebook. Every interaction writes to the notebook, and every rerun reads from it. That's the entire mental model.

---



## Appendix: Hashing Passwords (No helper methods in this section)

The code above stores plain text passwords on purpose for speed. In a real login system, students should never store raw text.

Use a one-way hash with a salt. `hashlib` can do this safely when combined with a work factor.

### Key ideas
- Never store the original password.
- Store two values:
  - `password_salt` (random hex string)
  - `password_hash` (derived bytes from password + salt)
- Verify login by hashing the typed password with the same salt and comparing hashes.
- Use constant-time comparison (`hmac.compare_digest`) for safer equality checks.

### What this means in practice
On **register**, after the user enters a password:
```python
# Needed imports for this approach
import hashlib
import hmac
import secrets

# Generate a random salt
salt = secrets.token_hex(16)

# Derive key (a long hex string)
key = hashlib.pbkdf2_hmac(
    "sha256",
    password.encode("utf-8"),
    bytes.fromhex(salt),
    120_000,
    dklen=32,
).hex()

stored_entry = f"{salt}${key}"
```

On **login**, compare against stored hash:
```python
salt, stored_key = stored_entry.split("$", 1)
candidate = hashlib.pbkdf2_hmac(
    "sha256",
    entered_password.encode("utf-8"),
    bytes.fromhex(salt),
    120_000,
    dklen=32,
).hex()

is_match = hmac.compare_digest(candidate, stored_key)
```

### Important migration note
- If students already created users with plain `"password"`, this file format will not match the hash flow.
- For this lab, either rebuild `users.json` or keep a temporary compatibility path during the transition.

### Teaching recommendation
Keep this appendix separate from the main exercise so students first learn routing/state, then security as an extension.