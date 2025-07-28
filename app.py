from langchain_core.tools import tool
import streamlit as st
from langchain_core.messages import HumanMessage
from textblob import TextBlob
import webbrowser
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

@tool
def emotion(data: str) -> str:
    """
    Get the text of user and give back the emotion from that text
    """
    try:
        blob = TextBlob(data)
        sentiment = blob.sentiment
        
        if sentiment.polarity > 0:
            return "positive sentiment"
        elif sentiment.polarity == 0:
            return "neutral sentiment"
        else:
            return "negative sentiment"
    except Exception as e:
        return "sorry can't get your emotions"

@tool
def play_song_by_mood(mood: str) -> str:
    """Play a Spotify playlist in your browser based on the given mood (e.g., positive,negative,neutral)."""
    
    MOOD_PLAYLIST_URLS = {
        "positive": "https://open.spotify.com/playlist/5RrC9KKTVXsxfMqUijEaua?si=fvhS71A3T5Kvyn09rnecoA&pi=t2AZ0VTnS6W_w",  
        "positive sentiment": "https://open.spotify.com/playlist/5RrC9KKTVXsxfMqUijEaua?si=fvhS71A3T5Kvyn09rnecoA&pi=t2AZ0VTnS6W_w",
        "happy": "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
        "neutral": "https://open.spotify.com/playlist/6irxS2m3XrDjWPZFkE5qgo?si=psR_F7PBQfqqBkxrePgFXA", 
        "neutral sentiment": "https://open.spotify.com/playlist/6irxS2m3XrDjWPZFkE5qgo?si=psR_F7PBQfqqBkxrePgFXA",
        "calm": "https://open.spotify.com/playlist/37i9dQZF1DX4SBhb3fqCJd",
        "negative": "https://open.spotify.com/playlist/37i9dQZF1DX7Fuh4bRTaZz",  
        "negative sentiment": "https://open.spotify.com/playlist/37i9dQZF1DX7Fuh4bRTaZz",
        "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7Fuh4bRTaZz"
    }
    
    mood = mood.lower()
    
    if mood in MOOD_PLAYLIST_URLS:
        url = MOOD_PLAYLIST_URLS[mood]
        webbrowser.open(url)
        return f"Opened a {mood} Bollywood playlist in your browser 🎵"
    else:
        return f"Sorry, I don't have a playlist for the mood '{mood}'. Try: {', '.join(MOOD_PLAYLIST_URLS.keys())}"


st.title("🎵 Mood Swifter")
st.markdown("---")
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #f5576c 75%, 
            #4facfe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    /* Animated gradient */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        text-align: center;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    /* Text styling */
    .stMarkdown p, .stMarkdown li {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        backdrop-filter: blur(5px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Button styling */
    .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        color: white;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Alert styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    .stAlert > div {
        color: white !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid rgba(0, 255, 0, 0.3);
    }
    
    /* Error message styling */
    .stError {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.3);
    }
    
    /* Info message styling */
    .stInfo {
        background: rgba(0, 123, 255, 0.1);
        border: 1px solid rgba(0, 123, 255, 0.3);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: rgba(255, 255, 255, 0.3) !important;
        border-top-color: white !important;
    }
    
    /* Chat input styling */
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stChatInput input {
        background: transparent;
        color: white;
        border: none;
    }
    
    .stChatInput input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Footer styling */
    .footer {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Floating animation for title */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    h1 {
        animation: float 3s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

if 'detected_mood' not in st.session_state:
    st.session_state.detected_mood = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# LLM Setup
llm = ChatGoogleGenerativeAI(

    google_api_key="AIzaSyC5hFpd3IWzM3MT32RqFjUx1RReeHrHIM4", 
    model="gemini-2.0-flash-exp",
    convert_system_message_to_human=True,
    temperature=0.7
)

user_input = st.chat_input("Hi! Say anything you feel...")

if user_input:
    st.write(f"**You said:** {user_input}")
    
 
    with st.spinner("Analyzing your mood..."):
        try:
           
            emotion_tools = [emotion]
            emotion_agent = create_react_agent(llm, emotion_tools)

            input_message = HumanMessage(content=f"Analyze the emotion in this text: {user_input}")
            
            emotion_result = None
            for step in emotion_agent.stream({"messages": [input_message]}, stream_mode="values"):
                emotion_result = step["messages"][-1].content
            
        
            if emotion_result:
                if "positive" in emotion_result.lower():
                    detected_mood = "positive sentiment"
                elif "negative" in emotion_result.lower():
                    detected_mood = "negative sentiment"
                else:
                    detected_mood = "neutral sentiment"
                
                st.session_state.detected_mood = detected_mood
                st.session_state.analysis_done = True
                
                # Display mood analysis
                st.markdown("### 🧠 Mood Analysis:")
                if "positive" in detected_mood:
                    st.success(f"🟢 **Detected Mood:** {detected_mood}")
                elif "negative" in detected_mood:
                    st.error(f"🔴 **Detected Mood:** {detected_mood}")
                else:
                    st.info(f"🟡 **Detected Mood:** {detected_mood}")
                
        except Exception as e:
            st.error(f"Error in emotion analysis: {str(e)}")

# Step 2: Music Player Button
if st.session_state.analysis_done and st.session_state.detected_mood:
    st.markdown("---")
    if st.button("🎵 Play Music Based on My Mood", type="primary"):
        with st.spinner("Opening your Bollywood playlist..."):
            try:
                # Create agent with music tool
                music_tools = [play_song_by_mood]
                music_agent = create_react_agent(llm, music_tools)
                
                # Play music based on detected mood
                music_message = HumanMessage(content=f"Play music for {st.session_state.detected_mood} mood")
                
                music_result = None
                for step in music_agent.stream({"messages": [music_message]}, stream_mode="values"):
                    music_result = step["messages"][-1].content
                
                if music_result:
                    st.success(music_result)
                    st.info("💡 **Tip:** Make sure you have Spotify installed or use Spotify Web Player!")
                
            except Exception as e:
                st.error(f"Error in music player: {str(e)}")
