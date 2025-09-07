import streamlit as st
from utils.api_client import login, register, query_agent, create_chat, save_message

st.title("Financial AI Agents")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if st.session_state.logged_in:
    st.success("Welcome! You are logged in.")
    
    # Initialize chat state when logged in
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_thread_id" not in st.session_state:
        st.session_state.current_thread_id = None
    # Your existing tabs
    tab1, tab2, tab3 = st.tabs(["Chat with Agent", "Upload Financial Data", "View Reports"])
    with tab1:
     st.subheader("Chat with Financial AI Agent")
    
    if st.button("Start New Chat"):
        # Create new chat in database
        if st.session_state.get("auth_token"):
            result = create_chat("Financial Chat", st.session_state.auth_token)
            if result["success"]:
                chat_data = result["data"]
                st.session_state.current_chat_id = chat_data["id"]
                st.session_state.current_thread_id = chat_data["thread_id"]
                st.session_state.messages = []
                st.success("New chat started!")
            else:
                st.error(f"Failed to create chat: {result['error']}")
    
    # Display existing messages
    for role, msg in st.session_state.messages:
        if role == "user":
            st.write(f"**You:** {msg}")
        else:
            st.write(f"**Agent:** {msg}")

    # Chat input (MOVE THIS INSIDE tab1)
    user_input = st.text_input("Your message:")
    if st.button("Send") and user_input:
        # Auto-create chat if none exists
        chat_created = True
        if not st.session_state.get("current_chat_id") and st.session_state.get("auth_token"):
            
            result = create_chat("Financial Chat", st.session_state.auth_token)
            if result["success"]:
                chat_data = result["data"]
                st.session_state.current_chat_id = chat_data["id"]
                st.session_state.current_thread_id = chat_data["thread_id"]
                
            else:
                st.error(f"Failed to create chat: {result['error']}")
                chat_created = False
        
        # Only proceed if we have a valid chat
        if chat_created and st.session_state.get("current_chat_id"):
            # Add user message to display
            st.session_state.messages.append(("user", user_input))
            
            # Save user message to database
            save_result = save_message(st.session_state.current_chat_id, "user", user_input, st.session_state.auth_token)
            
            
            # Get agent response
            thread_id = st.session_state.get("current_thread_id", "default")
            response = query_agent(user_input, thread_id)
            
            if response["success"]:
                answer = response["data"]["answer"]
                st.session_state.messages.append(("assistant", answer))
                
                # Save assistant message
                save_result = save_message(st.session_state.current_chat_id, "assistant", answer, st.session_state.auth_token)
                
                
                st.rerun()
            else:
                st.error(f"Error: {response['error']}")

                with tab2:
                 st.write("Upload financial data functionality will go here")
                with tab3:
                 st.write("Reports functionality will go here")
else:
    # Authentication tabs
    auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
    
    with auth_tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if email and password:
                result = login(email, password)
                if result["success"]:
                    st.session_state.logged_in = True
                    st.session_state.auth_token = result["data"]["access_token"]
                    st.rerun()
                else:
                    st.error(f"Login failed: {result['error']}")
            else:
                st.error("Please enter both email and password")
    
    with auth_tab2:
        st.write("Register a new account")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        full_name = st.text_input("Full Name", key="register_full_name")

        if st.button("Register"):
            if email and password and full_name:
                result = register(email, password, full_name)
                if result["success"]:
                    st.success("Registration successful! You can now log in.")
                else:
                    st.error(f"Registration failed: {result['error']}")
            else:
                st.error("Please fill in all fields")