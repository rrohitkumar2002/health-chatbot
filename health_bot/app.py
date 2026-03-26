import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# Paste your actual API key from Google AI Studio here
MY_API_KEY = st.secrets["GEMINI_API_KEY"] 

genai.configure(api_key=MY_API_KEY)

# UPDATED: Using the 2026 stable model name
# If this still gives a 404, try 'gemini-1.5-flash' as a backup
MODEL_ID = 'gemini-2.5-flash'

model = genai.GenerativeModel(
    model_name=MODEL_ID,
    system_instruction="You are a professional Health Advisor. Provide helpful, empathetic advice. ALWAYS include this disclaimer: 'I am an AI, not a doctor. Please consult a medical professional for serious concerns.'"
)

# --- 2. WEB INTERFACE ---
st.set_page_config(page_title="Health Advisor", page_icon="🏥")
st.title("🏥 Gemini Health Advisor")
st.info("I can help with symptoms, wellness tips, and general health info.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use generate_content but the model name is now corrected
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("The model returned an empty response. Try rephrasing.")
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("TIP: If you see a 404 error, Google might still be updating your region. Try changing MODEL_ID to 'gemini-1.5-flash' in the code.")