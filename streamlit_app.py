import streamlit as st
from PIL import Image

# Load image for branding (optional)
logo = Image.open("logo.png")

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
    st.subheader("🔑 Login to Your Account")
    username = st.text_input("👤 Username", placeholder="Enter your username")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
    login_col, _ = st.columns([1, 3])
    with login_col:
        if st.button("Login", use_container_width=True):
            if login_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"✅ Logged in as {username}")
            else:
                st.error("❌ Invalid username or password")

# Function to show the signup form
def signup():
    st.subheader("📝 Create an Account")
    name = st.text_input("📛 Name", placeholder="Enter your full name")
    username = st.text_input("👤 Username", placeholder="Choose a username")
    password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
    signup_col, _ = st.columns([1, 3])
    with signup_col:
        if st.button("Sign Up", use_container_width=True):
            if signup_user(username, password, name):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username

# Function to show the dashboard
def show_dashboard():
    st.sidebar.success(f"👤 Logged in as {st.session_state['username']}")
    st.sidebar.image(logo, use_column_width=True)  # Show logo in sidebar if applicable
    main_option = st.sidebar.selectbox("Go to", ["Browse Businesses", "My Dashboard"])

    if main_option == "Browse Businesses":
        st.header("🏢 Available Businesses for Investment")
        st.markdown("Choose a business to invest in and help grow their mission!")
        
        # Display businesses in columns for a better layout
        businesses = [
            {"name": "💻 Tech Startup", "description": "A new AI platform.", "category": "Technology", "fund_needed": 100000, "fund_raised": 50000},
            {"name": "🌞 Green Energy Co.", "description": "Developing solar panels.", "category": "Energy", "fund_needed": 200000, "fund_raised": 120000},
        ]
        for biz in businesses:
            st.subheader(biz['name'])
            st.write(f"**Category**: {biz['category']}")
            st.write(f"**Funds Needed**: ${biz['fund_needed']}")
            st.write(f"**Funds Raised**: ${biz['fund_raised']}")
            
            # Investment section in a columns layout
            investment_col, button_col = st.columns([2, 1])
            with investment_col:
                investment_amount = st.number_input(f"💸 Invest in {biz['name']}", min_value=50, step=50, key=biz['name'])
            with button_col:
                if st.button(f"💰 Invest ${investment_amount}", key=f"invest_{biz['name']}", use_container_width=True):
                    st.success(f"🎉 Successfully invested ${investment_amount} in {biz['name']}!")

    elif main_option == "My Dashboard":
        st.header("📊 My Investments")
        st.info("You haven't made any investments yet (local demo).")

    # Add logout button
    logout_col, _ = st.columns([1, 3])
    with logout_col:
        if st.button("Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.success("✅ Successfully logged out.")

# Main app logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Set the title and theme for the app
st.set_page_config(
    page_title="Business Investment App",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🌐 Navigation")
auth_option = st.sidebar.selectbox("Choose Option", ["Login", "Sign Up"])

# Branding at the top
st.image(logo, width=100)  # Optionally show a logo
st.title("Welcome to the Business Investment Platform")

if st.session_state["logged_in"]:
    show_dashboard()
else:
    if auth_option == "Login":
        login()
    elif auth_option == "Sign Up":
        signup()
