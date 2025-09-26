from openai import OpenAI
import streamlit as st

# Setting up the Streamlit page configuration
st.set_page_config(page_title="Interview Page", page_icon="💬")
st.title("Interview Chatbot")

# Personal Information Section
st.subheader('Personal information', divider='rainbow')

# Input fields for collecting user's personal information
name = st.text_input(label = "Name", max_chars = None, placeholder = "Enter your name")

experience = st.text_area(label = "Experience", value = "", height = None, max_chars = None, placeholder = "Describe your experience")

skills = st.text_area(label = "Skills", value = "", height = None, max_chars = None, placeholder = "List your skills")

# Test labels for personal information
st.write(f"**Your Name**: {name}")
st.write(f"**Your Experience**: {experience}")
st.write(f"**Your Skills**: {skills}")

st.sidebar.title("Enter Open AI Key")
open_ai_key = st.sidebar.text_input("OPEN_AI_KEY", type="password")

# Company and Position Section
st.subheader('Company and Position', divider = 'rainbow')

#Field for selecting the job level, position and company
col1, col2 = st.columns(2)
with col1:
    level = st.radio(
    "Choose level",
    key="visibility",
    options=["Junior", "Mid-level", "Senior"],
    )

with col2:
    position = st.selectbox(
    "Choose a position",
    ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst"))

company = st.selectbox(
    "Choose a Company",
    ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify", "Eurotech Associates Inc")
)


st.write(f"**Your information**: {level} {position} at {company}")

def validate_api_key(open_ai_key):
    try:
        client = OpenAI(api_key=open_ai_key)
        _ = client.models.list()
        return True
    except:
        return False

if validate_api_key(open_ai_key):
    client = OpenAI(api_key=open_ai_key)
    max_tokens_input = st.sidebar.slider("Max Output Tokens", min_value=10, max_value=4000, value=500) 
    #client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.warning("Valid Open AI key is required to proceed.")
    st.stop() 


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"


#if "messages" not in st.session_state:
st.session_state.messages = [{"role":"system", "content": f"You are an HR executive that interviews an interviewee called {name} with expirience {experience} and skills {skills}. You should interview him for the position {level} {position} at the company {company}"}]


for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input("Your answer."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

try:

    # Assistant's response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            max_tokens=max_tokens_input,
            temperature=0.7,
        )
       
        # Display the assistant's response as it streams
        response = st.write_stream(stream)
          
      
    st.session_state.messages.append({"role": "assistant", "content": response})
except Exception as e:
    st.exception(e)
    st.error("An unexpected error occurred. Please try again later.")