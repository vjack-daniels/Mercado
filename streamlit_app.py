import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import base64

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("shellhacked-72947-firebase-adminsdk-nvkpw-1d815b210e.json")  # Replace with your path
    firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Simulated local user database
user_db = {"admin": {"password": "adminpass"}}

# Session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Function to convert local image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convert 'latino.jpg' to base64
img_base64 = get_base64_image("latino.jpg")

# Custom CSS with the latino.jpg background image
background_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .main {{
        background-color: #ffffff;  /* Solid white background */
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);  /* Softer shadow */
    overflow: auto;  /* Enable scrolling */
    }}
    </style>
"""

# Apply the background image style
st.markdown(background_image, unsafe_allow_html=True)

# Custom CSS to make all text bold and noticeable
st.markdown(
    f"""
    <style>
    body {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        padding: 0;
        margin: 0;
    }}
    .main {{
        background-color: rgba(255, 255, 255, 0.7);  /* Subtle white background with slight transparency */
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);  /* Softer shadow */
        overflow: auto;  /* Enable scrolling */
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #1f2937;  /* Darker text color for better contrast */
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: bold;  /* Make headings bold */
    }}
    p {{
        font-size: 16px;
        line-height: 1.6;
        color: #4a5568;  /* Muted text color */
        font-family: 'Arial', sans-serif;
        text-align: justify;
        font-weight: bold;  /* Make paragraph text bold */
    }}
    .stButton>button {{
        background-color: #007bff;  /* Blue primary button */
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        margin: 0 auto; /* Ensures the button is centered */
        display: block;
        font-weight: bold;  /* Make button text bold */
    }}
    .stButton>button:hover {{
        background-color: #0056b3;  /* Darker blue on hover */
        transition: background-color 0.3s ease;
    }}
    .stTextInput>div>input {{
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #ced4da;
        font-size: 14px;
        background-color: #ffffff;
        font-weight: bold;  /* Make input text bold */
    }}
    .stSelectbox>div>div>div {{
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #ced4da;
        font-weight: bold;  /* Make selectbox text bold */
    }}
    .stSidebar {{
        background-color: #343a40;  /* Dark gray for sidebar */
        color: white;
    }}
    .stSidebar h2, .stSidebar p, .stSidebar select {{
        color: white;
        font-weight: bold;  /* Make sidebar text bold */
    }}
    .stSidebar .stButton>button {{
        background-color: #17a2b8;  /* Teal button in sidebar */
        color: white;
        font-weight: bold;  /* Make sidebar button text bold */
    }}
    .stSidebar .stButton>button:hover {{
        background-color: #138496;  /* Darker teal on hover */
        transition: background-color 0.3s ease;
    }}

    /* Centering the Login and Sign-up buttons */
    .stRadio>div {{
        display: flex;
        justify-content: center;
        font-weight: bold;  /* Make radio button text bold */
    }}

    /* Centering the blue login button at the bottom of the signup page */
    .stButton {{
        display: flex;
        justify-content: center;
    }}
    </style>
    """, 
    unsafe_allow_html=True
)

# Login Function
def login(username, password):
    if username in user_db and user_db[username]["password"] == password:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success(f"Welcome {username}!")
    else:
        st.error("Invalid username or password!")

# Sign-up Function
def signup(username, password):
    if username in user_db:
        st.error("Username already exists!")
    else:
        user_db[username] = {"password": password}
        st.success("Account created successfully! You can log in now.")

# Function to fetch all businesses
def get_all_businesses():
    businesses_ref = db.collection('Latino_Small_Businesses')  # Replace with your collection name
    docs = businesses_ref.stream()

    businesses = []
    for doc in docs:
        business_data = doc.to_dict()
        business_data['id'] = doc.id  # Store document ID for future reference
        businesses.append(business_data)
    return businesses

# Function to simulate investment with a slider
def invest_in_business(business_id):
    with st.container():
        st.markdown(f"#### {business_id}")
        amount = st.slider(f"How much would you like to invest in {business_id}?", min_value=1, max_value=10000, value=100)
        if st.button(f"Invest in {business_id}"):
            # Simulated saving investment to Firestore
            db.collection('investments').add({
                'business_id': business_id,
                'user_id': st.session_state["username"],  # Use logged-in user ID
                'amount': amount
            })
            st.success(f"Successfully invested ${amount} in {business_id}!")

# Simulated reviews database (local)
reviews_db = {
    "Business A": [
        {"user": "John", "review": "Great business, invested and got good returns!"},
        {"user": "Maria", "review": "Really loved the products they offer."}
    ],
    "Business B": [
        {"user": "Carlos", "review": "Fantastic team, very transparent in their dealings."}
    ],
    "Business C": []
}

# Community Page Function
def community_page():
    st.markdown("<h2 style='text-align:center;'>Community Reviews</h2>", unsafe_allow_html=True)
    st.write("Here, you can read reviews from other investors and post your own!")

    # Select a business to review
    business_options = ["Business A", "Business B", "Business C"]
    selected_business = st.selectbox("Select a Business", business_options)

    # Display reviews for the selected business
    st.markdown(f"### Reviews for {selected_business}")
    if selected_business in reviews_db and len(reviews_db[selected_business]) > 0:
        for review in reviews_db[selected_business]:
            st.markdown(f"**{review['user']}**: {review['review']}")
    else:
        st.markdown("No reviews yet for this business.")

    # Add a form to submit a review
    st.markdown(f"### Post a Review for {selected_business}")
    user_review = st.text_area("Write your review here:")
    if st.button("Post Review"):
        if user_review:
            reviews_db[selected_business].append({"user": st.session_state["username"], "review": user_review})
            st.success(f"Thank you for your review on {selected_business}!")
        else:
            st.error("Please write a review before submitting.")

# Logout Function
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.success("You have been logged out!")

# Function to generate fake investment data
def generate_fake_investment_data():
    """Generates fake investment data to simulate portfolio performance."""
    dates = pd.date_range(start="2023-01-01", periods=12, freq="M")
    investments = np.cumsum(np.random.randint(1000, 5000, size=len(dates)))  # Cumulative investment growth
    return pd.DataFrame({"Date": dates, "Investments": investments})

# Define the main pages
def browse_businesses_page():
    with st.container():
        st.markdown("<h2 style='text-align:center;'>Browse Latino-Owned Small Businesses</h2>", unsafe_allow_html=True)

        businesses = get_all_businesses()
        categories = ["All"] + sorted(set([business['Category'] for business in businesses]))

        selected_category = st.selectbox("Filter by Category", categories)

        if selected_category == "All":
            filtered_businesses = businesses
        else:
            filtered_businesses = [b for b in businesses if b['Category'] == selected_category]

        for business in filtered_businesses:
            with st.expander(f"**{business.get('Name', 'Unnamed Business')}**"):
                st.write(business['Description'])
                st.write(f"Goal: ${business['Goal']} | Raised: ${business['Raised']}")
                if 'image_urls' in business and len(business['image_urls']) > 0:
                    st.image(business['image_urls'][0], use_column_width=True)
                invest_in_business(business.get('Name', 'Unnamed Business'))

# Dashboard Page
def dashboard_page():
    with st.container():
        st.markdown("<h2 style='text-align:center;'>Your Investment Dashboard</h2>", unsafe_allow_html=True)
        st.write(f"Welcome, {st.session_state['username']}!")
        
        # Quick Summary Section
        total_invested = np.random.randint(10000, 50000)  # Made-up total invested amount
        total_returns = total_invested + np.random.randint(500, 5000)  # Simulated returns
        num_businesses = np.random.randint(3, 10)  # Number of businesses invested in

        st.markdown(
            f"""
            <div style='text-align:center;'>
                <h3>Portfolio Summary</h3>
                <p>Total Invested: <strong>${total_invested}</strong></p>
                <p>Total Returns: <strong>${total_returns}</strong></p>
                <p>Businesses Invested In: <strong>{num_businesses}</strong></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Dynamic Line Graph
        st.markdown("<h3 style='text-align:center;'>Investment Performance</h3>", unsafe_allow_html=True)
        
        # Generate fake investment data
        investment_data = generate_fake_investment_data()

        fig, ax = plt.subplots()
        ax.plot(investment_data["Date"], investment_data["Investments"], marker='o')
        ax.set_title("Cumulative Investments Over Time", fontsize=14)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Total Investment ($)", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True)

        st.pyplot(fig)

        # Simulate a list of current investments
        st.markdown("<h3 style='text-align:center;'>Current Investments</h3>", unsafe_allow_html=True)

        investments = [
            {"Name": "Business A", "Amount": 5000, "Goal": 10000, "Raised": 6000},
            {"Name": "Business B", "Amount": 3000, "Goal": 8000, "Raised": 4000},
            {"Name": "Business C", "Amount": 2000, "Goal": 5000, "Raised": 3000},
        ]

        for inv in investments:
            progress = (inv['Raised'] / inv['Goal']) * 100
            st.markdown(
                f"""
                <div style='border: 1px solid #ddd; padding: 10px; margin-bottom: 10px;'>
                    <h4>{inv['Name']}</h4>
                    <p>Amount Invested: ${inv['Amount']}</p>
                    <p>Goal: ${inv['Goal']} | Raised: ${inv['Raised']}</p>
                    <progress value='{progress}' max='100' style='width: 100%; height: 20px;'></progress>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Projected Growth
        st.markdown("<h3 style='text-align:center;'>Projected Growth</h3>", unsafe_allow_html=True)

        projected_growth = np.random.randint(10000, 20000)  # Simulated projected growth
        st.markdown(
            f"""
            <div style='text-align:center;'>
                <p>Your portfolio is projected to grow by an estimated <strong>${projected_growth}</strong> over the next year based on current trends.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Simulate setting up payment info
def payment_info_page():
    st.title("Payment Information Setup")

    # Initialize session state for payment info if it doesn't exist
    if 'payment_info' not in st.session_state:
        st.session_state.payment_info = {
            'name': '',
            'card_number': '',
            'expiry_date': '',
            'cvv': '',
        }

    # Create form for payment info
    with st.form("payment_info_form"):
        st.write("Enter your payment details:")
        
        # Form fields
        st.session_state.payment_info['name'] = st.text_input("Cardholder Name", value=st.session_state.payment_info['name'])
        st.session_state.payment_info['card_number'] = st.text_input("Card Number", value=st.session_state.payment_info['card_number'])
        st.session_state.payment_info['expiry_date'] = st.text_input("Expiry Date (MM/YY)", value=st.session_state.payment_info['expiry_date'])
        st.session_state.payment_info['cvv'] = st.text_input("CVV", value=st.session_state.payment_info['cvv'], type="password")

        # Submit button
        submitted = st.form_submit_button("Submit")

    # If form is submitted, show payment info
    if submitted:
        st.success("Payment information saved successfully!")
        st.write("**Payment Information Summary:**")
        st.write(f"**Cardholder Name:** {st.session_state.payment_info['name']}")
        st.write(f"**Card Number:** **** **** **** {st.session_state.payment_info['card_number'][-4:]}")
        st.write(f"**Expiry Date:** {st.session_state.payment_info['expiry_date']}")
        st.write(f"**CVV:** {len(st.session_state.payment_info['cvv']) * '*'}")  # Mask CVV for security

# Welcome/Login/Signup Page
def welcome_page():
    with st.container():
        st.markdown("<h1 style='text-align:center;'>Welcome to</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-family: Arial, sans-serif; font-size: 60px;'>Mercado</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Connecting investors with Latino-owned small businesses</p>", unsafe_allow_html=True)

        option = st.radio("", ("Login", "Sign-up"), index=0)

        if option == "Login":
            st.markdown("<h3 style='text-align:center;'>Login</h3>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                login(username, password)
        elif option == "Sign-up":
            st.markdown("<h3 style='text-align:center;'>Create Account</h3>", unsafe_allow_html=True)
            new_username = st.text_input("Create Username")
            new_password = st.text_input("Create Password", type="password")
            if st.button("Sign-up"):
                signup(new_username, new_password)

# Navigation based on login status
if not st.session_state["logged_in"]:
    welcome_page()
else:
    # Add logout button in the sidebar
    with st.sidebar:
        st.markdown(f"**Logged in as {st.session_state['username']}**")
        if st.button("Logout"):
            logout()

    # Display the main navigation menu
    page = st.sidebar.selectbox("Navigate", ["Browse Businesses", "Dashboard", "Community", "Setup Payment Info"])

    if page == "Browse Businesses":
        browse_businesses_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Community":
        community_page()
    elif page == "Setup Payment Info":
        payment_info_page()