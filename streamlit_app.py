import streamlit as st

# Hardcoded username and password (can be extended)
USER_CREDENTIALS = {
    "dude": "duude",
    "user2": "password2",
    "admin": "admin123"
}

# Function to handle login
def login_user(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return True
    else:
        return False

# Function to handle signup (this is a simple local signup)
def signup_user(username, password, name):
    if username in USER_CREDENTIALS:
        st.error("User already exists.")
        return False
    else:
        # Simulate adding the user to a local "database"
        USER_CREDENTIALS[username] = password
        st.success("User created successfully!")
        return True

# Function to show the login form
def login():
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username or password")

# Function to show the signup form
def signup():
    st.subheader("Create an Account")
    name = st.text_input("Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if signup_user(username, password, name):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username

# Function to show the dashboard
def show_dashboard():
    st.sidebar.success(f"Logged in as {st.session_state['username']}")
    main_option = st.sidebar.selectbox("Go to", ["Browse Businesses", "My Dashboard"])
    
    if main_option == "Browse Businesses":
        st.header("Available Businesses for Investment")
        businesses = [
            {"name": "Tech Startup", "description": "A new AI platform.", "category": "Technology", "fund_needed": 100000, "fund_raised": 50000},
            {"name": "Green Energy Co.", "description": "Developing solar panels.", "category": "Energy", "fund_needed": 200000, "fund_raised": 120000},
        ]
        for biz in businesses:
            st.subheader(biz['name'])
            st.write(biz['description'])
            st.write(f"Category: {biz['category']}")
            st.write(f"Funds Needed: ${biz['fund_needed']}")
            st.write(f"Funds Raised: ${biz['fund_raised']}")
            investment_amount = st.number_input(f"Invest in {biz['name']}", min_value=50, step=50, key=biz['name'])
            if st.button(f"Invest ${investment_amount} in {biz['name']}", key=f"invest_{biz['name']}"):
                st.success(f"Successfully invested ${investment_amount} in {biz['name']}!")

    elif main_option == "My Dashboard":
        st.header("My Investments")
        # For this demo, we are not storing investments persistently.
        st.write("You haven't made any investments yet (local demo).")

    # Add logout button
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.success("Successfully logged out.")

# Main app logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

st.sidebar.title("Navigation")
auth_option = st.sidebar.selectbox("Choose Option", ["Login", "Sign Up"])

if st.session_state["logged_in"]:
    show_dashboard()
else:
    if auth_option == "Login":
        login()
    elif auth_option == "Sign Up":
        signup()
