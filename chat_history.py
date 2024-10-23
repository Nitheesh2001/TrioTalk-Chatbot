# chat_history.py

import streamlit as st

def show_chat_history_page():
    st.title("Chat History")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        st.write("No chat history available.")
    else:
        # Display chat history in reverse order (most recent first)
        st.subheader("Recent Conversations")
        for i in range(len(st.session_state['chat_history']) - 1, -1, -1):
            role, text = st.session_state['chat_history'][i]

            # Display the message in a styled box
            if role == "You":
                st.markdown(
                    f"""
                    <div style='background-color: #d4edda; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>
                        <b style='color: #000000;'>{role}:</b> <span style='color: #000000;'>{text}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='background-color: #f8d7da; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>
                        <b style='color: #000000;'>{role}:</b> <span style='color: #000000;'>{text}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
