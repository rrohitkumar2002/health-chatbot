import streamlit as st
from google import genai  # <--- THIS IS THE NEW 2026 WAY

# --- 1. CONFIGURATION ---
# Use the Secret key we set up in Streamlit Cloud
MY_API_KEY = st.secrets["GEMINI_API_KEY"]

# Create the 2026 Client
client = genai.Client(api_key=MY_API_KEY)

# Use the latest 2026 stable model
MODEL_ID = "gemini-1.5-flash" 

# --- 2. WEB INTERFACE ---
st.set_page_config(page_title="Health Advisor 2026", page_icon="🏥")
st.title("🏥 Gemini Health Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask me a health question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Modern 2026 way to call the model
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config={'system_instruction': "You are a health assistant. Always give a medical disclaimer."}
            )
            
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"Error: {e}")
