import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load configuration from config.yaml
with open('config.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Create the login widget
def login():
    authenticator.login()

# Create the logout widget
def logout():
    authenticator.logout()

# Create the reset password widget
def reset_password():
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

# Create the new user registration widget
def register_user():
    try:
        email, username, name = authenticator.register_user(preauthorization=False)
        if email:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

# Create the forgot password widget
def forgot_password():
    try:
        username, email, new_password = authenticator.forgot_password()
        if username:
            st.success('New password to be sent securely')
            # The developer should securely transfer the new password to the user.
        elif username == False:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

# Create the forgot username widget
def forgot_username():
    try:
        username, email = authenticator.forgot_username()
        if username:
            st.success('Username to be sent securely')
            # The developer should securely transfer the username to the user.
        elif username == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

# Create the update user details widget
def update_user_details():
    if st.session_state["authentication_status"]:
        try:
            if authenticator.update_user_details(st.session_state["username"]):
                st.success('Entries updated successfully')
        except Exception as e:
            st.error(e)

# Main Streamlit app
def main():
    st.title("Streamlit Authentication Example")

    # Sidebar for login/logout and other options
    st.sidebar.title("Authentication")
    if st.sidebar.button("Login"):
        login()
    if st.sidebar.button("Logout"):
        logout()

    # Main content area
    if st.session_state["authentication_status"]:
        st.write(f'Welcome {st.session_state["name"]}')
        st.title('Some restricted content')
        # Add your restricted content here
        if st.button("Reset Password"):
            reset_password()
        if st.button("Update User Details"):
            update_user_details()
    else:
        st.warning('Please log in to access the content.')

    # Other authentication options
    st.sidebar.title("Other Options")
    if st.sidebar.button("Register"):
        register_user()
    if st.sidebar.button("Forgot Password"):
        forgot_password()
    if st.sidebar.button("Forgot Username"):
        forgot_username()

if __name__ == "_main_":
    main()