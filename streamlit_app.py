# app.py

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
import hashlib

# Initialize Firebase
firebase_credentials = json.loads(st.secrets["firebase_credentials"])
cred = credentials.Certificate(firebase_credentials)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
    
db = firestore.client()

# Helper Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(email, password, name):
    try:
        user = auth.create_user(email=email, password=password)
        # Add user to Firestore
        db.collection('users').document(user.uid).set({
            'name': name,
            'email': email,
            'investments': []
        })
        st.success("User created successfully!")
    except Exception as e:
        st.error(f"Error creating user: {e}")

def login(email, password):
    try:
        users = db.collection('users').where('email', '==', email).get()
        if users:
            user_doc = users[0]
            # Simulate password check
            # In reality, use Firebase client SDK for proper auth
            return user_doc.id, user_doc.to_dict()
        else:
            st.error("User not found")
            return None, None
    except Exception as e:
        st.error(f"Error logging in: {e}")
        return None, None

# Sidebar Navigation
st.sidebar.title("Navigation")
auth_option = st.sidebar.selectbox("Choose Option", ["Login", "Sign Up"])

if auth_option == "Sign Up":
    st.header("Create an Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        signup(email, password, name)

elif auth_option == "Login":
    st.header("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id, user_info = login(email, password)
        if user_id:
            st.session_state['user_id'] = user_id
            st.session_state['user_info'] = user_info
            st.success("Logged in successfully!")

# Main App
if 'user_id' in st.session_state:
    st.sidebar.success(f"Logged in as {st.session_state['user_info']['name']}")
    main_option = st.sidebar.selectbox("Go to", ["Browse Businesses", "My Dashboard"])
    
    if main_option == "Browse Businesses":
        st.header("Available Businesses for Investment")
        businesses = db.collection('businesses').stream()
        for biz in businesses:
            biz_data = biz.to_dict()
            st.subheader(biz_data['name'])
            st.write(biz_data['description'])
            st.write(f"Category: {biz_data['category']}")
            st.write(f"Funds Needed: ${biz_data['fund_needed']}")
            st.write(f"Funds Raised: ${biz_data['fund_raised']}")
            investment_amount = st.number_input(f"Invest in {biz_data['name']}", min_value=50, step=50, key=biz.id)
            if st.button(f"Invest ${investment_amount} in {biz_data['name']}", key=f"invest_{biz.id}"):
                # Simulate investment
                new_fund_raised = biz_data['fund_raised'] + investment_amount
                db.collection('businesses').document(biz.id).update({'fund_raised': new_fund_raised})
                
                # Update user's investments
                investments = st.session_state['user_info'].get('investments', [])
                investments.append({
                    'business_id': biz.id,
                    'business_name': biz_data['name'],
                    'amount': investment_amount
                })
                db.collection('users').document(st.session_state['user_id']).update({'investments': investments})
                st.success(f"Successfully invested ${investment_amount} in {biz_data['name']}!")
                
                # Update session state
                st.session_state['user_info']['investments'] = investments

    elif main_option == "My Dashboard":
        st.header("My Investments")
        investments = st.session_state['user_info'].get('investments', [])
        if investments:
            for inv in investments:
                st.subheader(inv['business_name'])
                st.write(f"Amount Invested: ${inv['amount']}")
        else:
            st.write("You haven't made any investments yet.")
else:
    st.info("Please log in or sign up to continue.")
