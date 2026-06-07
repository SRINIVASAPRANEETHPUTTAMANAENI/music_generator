""" 
🎵 AI Music Composition - Complete Generation Engine with Authentication 🎵 
✨ Transform your emotions into beautiful music with full AI generation! ✨ 
Milestone 3: Authentication, Home Page, History & Enhanced UI with Audio Storage
"""

import streamlit as st
import json
import time
import traceback
import numpy as np
from io import BytesIO
from typing import Dict, Any, Optional
from datetime import datetime

# Import custom modules
from config import Config
from mood_analyzer import MoodAnalyzer
from music_parameters import MusicParametersMapper
from music_generator import MusicGenerator
from audio_processor import AudioProcessor
from database import DatabaseManager

# Initialize database
db = DatabaseManager()

# Enhanced page config
st.set_page_config(
    page_title="🎵 AI Music Generator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Super Enhanced styling
st.markdown(Config.AUTH_STYLE, unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'signin'
    if 'mood_analyzer' not in st.session_state:
        st.session_state.mood_analyzer = None
    if 'music_generator' not in st.session_state:
        st.session_state.music_generator = None

def show_signin_page():
    """Display sign-in page with super attractive UI"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">🎵 Sign In</h1>', unsafe_allow_html=True)
    
    with st.form("signin_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("🚀 Sign In", use_container_width=True)
        
        if submit_button:
            if not username or not password:
                st.error("⚠️ Please fill in all fields")
            else:
                success, user_data = db.authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.session_state.page = 'home'
                    st.success("✅ Login successful!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    st.markdown("---")
    if st.button("📝 New User? Sign Up", use_container_width=True):
        st.session_state.page = 'signup'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_signup_page():
    """Display sign-up page with super attractive UI"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">📝 Create Account</h1>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        name = st.text_input("👨‍💼 Full Name", placeholder="Enter your full name")
        username = st.text_input("👤 Username", placeholder="Choose a unique username")
        password = st.text_input("🔐 Password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm your password")
        submit_button = st.form_submit_button("✨ Create Account", use_container_width=True)
        
        if submit_button:
            if not all([name, username, password, confirm_password]):
                st.error("⚠️ Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("⚠️ Password must be at least 6 characters long")
            else:
                success, message = db.create_user(name, username, password)
                if success:
                    st.success(f"✅ {message}")
                    st.info("🎉 Welcome! Please sign in with your new account")
                    st.balloons()
                    time.sleep(2)
                    st.session_state.page = 'signin'
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    st.markdown("---")
    if st.button("🔙 Back to Sign In", use_container_width=True):
        st.session_state.page = 'signin'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_home_page():
    """Display enhanced home page after authentication"""
    # Header with user greeting
    st.markdown(f"""
    <div class="main-header">
        <h1>🎵 Welcome to AI Music Composer, {st.session_state.user['name']}! 🎵</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Transform your emotions and thoughts into beautiful, personalized music</p>
    </div>
    """, unsafe_allow_html=True)
    
    # App description with enhanced layout
    st.markdown('<div class="home-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown("""
        ### ✨ About AI Music Composer
        
        Our cutting-edge AI Music Composer uses advanced natural language processing and machine learning to create personalized music based on your emotions and preferences. Simply describe how you're feeling or what kind of music you want, and watch as AI transforms your words into beautiful melodies!
        
        **🌟 Key Features:**
        - 🧠 **Emotion Analysis**: AI understands your mood from text
        - 🎼 **Intelligent Composition**: Generates music matching your emotional state  
        - 💾 **Multiple Formats**: Download as MP3 or WAV
        - 🎸 **Instrument Selection**: AI chooses appropriate instruments
        - ⚡ **Tempo & Key Optimization**: Perfect musical parameters
        - 📚 **History Tracking**: Keep track of all your creations with audio
        """)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎵</div>
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎼</div>
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎧</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        ### 🚀 How It Works
        
        1. **Describe Your Mood** 📝  
           Tell us how you're feeling or what style you want
        
        2. **AI Analysis** 🔍  
           Our AI analyzes your text for emotions and energy
        
        3. **Music Generation** 🎵  
           Advanced models create your personalized soundtrack
        
        4. **Download & Save** 💾  
           Get your music in high quality with full history
        
        5. **Share & Enjoy** 🎧  
           Use your AI-generated music anywhere!
        """)
    
    st.markdown("---")
    
    # Enhanced action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎼</div>
            <h3>Create New Music</h3>
            <p>Start composing your personalized AI music by describing your mood or desired style. Experience the magic of AI-powered music generation!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Music Generator", key="launch_generator", use_container_width=True):
            st.session_state.page = 'generator'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📚</div>
            <h3>View Music History</h3>
            <p>Browse through all your previous music generations, replay your creations, and download them anytime. Your musical journey awaits!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📖 View My History", key="view_history", use_container_width=True):
            st.session_state.page = 'history'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    history = db.get_user_history(st.session_state.user['id'])
    audio_count = sum(1 for h in history if h['has_audio'])
    
    with col1:
        st.metric("🎵 Available Prompts", "15", "Ready to Use")
    with col2:
        st.metric("🎼 Music Styles", "6+", "Mood Categories")  
    with col3:
        st.metric("📈 Your Creations", len(history), "Total Generated")
    with col4:
        st.metric("🎧 Saved Audio", audio_count, "With Sound")

def show_history_page():
    """Display enhanced user's prompt history with audio playback"""
    st.markdown(f"""
    <div class="main-header">
        <h1>📚 Your Music Generation History</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Browse, replay, and download all your AI music creations</p>
    </div>
    """, unsafe_allow_html=True)
    
    history = db.get_user_history(st.session_state.user['id'])
    
    if not history:
        st.markdown("""
        <div class="feature-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎵</div>
            <h3>No music generated yet!</h3>
            <p>Start creating your first AI composition and build your musical collection.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Create Your First Music", use_container_width=True):
            st.session_state.page = 'generator'
            st.rerun()
    else:
        st.success(f"🎉 Found {len(history)} music generations in your history")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_mood = st.selectbox("Filter by Mood", ["All"] + list(Config.MOOD_CATEGORIES.keys()))
        with col2:
            filter_audio = st.selectbox("Filter by Audio", ["All", "With Audio", "Without Audio"])
        with col3:
            sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])
        
        # Filter and sort history
        filtered_history = history.copy()
        
        if filter_mood != "All":
            filtered_history = [h for h in filtered_history if h['mood'] == filter_mood]
        
        if filter_audio == "With Audio":
            filtered_history = [h for h in filtered_history if h['has_audio']]
        elif filter_audio == "Without Audio":
            filtered_history = [h for h in filtered_history if not h['has_audio']]
        
        if sort_order == "Oldest First":
            filtered_history = filtered_history[::-1]
        
        for i, item in enumerate(filtered_history):
            with st.container():
                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4>🎵 Generation #{len(history) - history.index(item)}</h4>
                        <span style="color: #666;">📅 {item['date']}</span>
                    </div>
                    <p><strong>💭 Prompt:</strong> "{item['prompt']}"</p>
                    <div style="display: flex; gap: 1rem; margin: 1rem 0;">
                        <span><strong>🎭 Mood:</strong> {get_mood_emoji(item['mood'])} {item['mood'].title()}</span>
                        <span><strong>⚡ Energy:</strong> {item['energy']}/10</span>
                        {f"<span><strong>🎧 Audio:</strong> ✅ Available</span>" if item['has_audio'] else "<span><strong>🎧 Audio:</strong> ❌ Not Available</span>"}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Audio player if available
                if item['has_audio'] and item['audio_data']:
                    st.markdown('<div class="music-player-container">', unsafe_allow_html=True)
                    st.markdown(f"### 🎧 Audio Player - {item['mood'].title()} Music")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.audio(item['audio_data'], format=f"audio/{item['audio_format']}")
                    with col2:
                        if item['duration']:
                            st.metric("Duration", f"{item['duration']:.1f}s")
                        
                        # Download button
                        st.download_button(
                            "💾 Download",
                            item['audio_data'],
                            item['audio_filename'],
                            f"audio/{item['audio_format']}",
                            key=f"download_{i}"
                        )
                    
                    st.markdown('</div>', unsafe_allow_html=True)

def get_mood_emoji(mood):
    """Get emoji for mood"""
    return Config.EMOJI_MAPPING.get(mood, '🎵')

# Load models with caching
@st.cache_resource(show_spinner=True)
def get_mood_models():
    """Load mood analysis models with caching"""
    with st.spinner("🔄 Loading mood analysis models..."):
        try:
            analyzer = MoodAnalyzer()
            mapper = MusicParametersMapper()
            return analyzer, mapper, None
        except Exception as e:
            return None, None, str(e)

@st.cache_resource(show_spinner=True)
def get_music_generator():
    """Load music generation model with caching"""
    with st.spinner("🔄 Loading music generation model (this may take a few minutes)..."):
        try:
            generator = MusicGenerator(model_name=Config.MUSICGEN_MODEL_NAME)
            return generator, None
        except Exception as e:
            st.error(f"Failed to load music generator: {str(e)}")
            return None, str(e)

def show_generator_page():
    """Display the enhanced music generation page"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🎼 AI Music Generator</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Describe your mood or desired music style and let AI create your perfect soundtrack</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models if not already loaded
    if st.session_state.mood_analyzer is None:
        analyzer, mapper, error = get_mood_models()
        if error:
            st.error(f"❌ Failed to load mood analysis models: {error}")
            return
        st.session_state.mood_analyzer = analyzer
        st.session_state.music_mapper = mapper
    
    if st.session_state.music_generator is None:
        generator, error = get_music_generator()
        if error:
            st.error(f"❌ Failed to load music generator: {error}")
            st.info("💡 You can still analyze mood and see musical parameters without music generation.")
        st.session_state.music_generator = generator
    
    # Enhanced sidebar with sample prompts
    with st.sidebar:
        st.markdown("### 🎵 Sample Prompts")
        st.markdown("*Click any prompt to use it:*")
        
        for i, sample in enumerate(Config.SAMPLE_TEXTS):
            if st.button(sample, key=f"sample_{i}", help="Click to use this prompt"):
                st.session_state.selected_prompt = sample
                st.rerun()
    
    # Main interface with enhanced layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced text input
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        user_input = st.text_area(
            "🎭 Describe your mood or desired music style:",
            value=st.session_state.get('selected_prompt', ''),
            height=120,
            placeholder="Example: I'm feeling happy and energetic, want upbeat music for dancing...",
            help="Be specific about your mood, energy level, and preferred style"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced generation settings
        with st.expander("⚙️ Advanced Settings", expanded=False):
            col_a, col_b = st.columns(2)
            with col_a:
                duration = st.slider("🕐 Duration (seconds)", 10, 30, 20, help="Longer durations may take more time")
                output_format = st.selectbox("📁 Output Format", ["mp3", "wav"], help="MP3 is smaller, WAV is higher quality")
            with col_b:
                guidance_scale = st.slider("🎨 Creativity Level", 1.0, 5.0, 3.0, help="Higher values = more creative but less predictable")
                auto_save_history = st.checkbox("💾 Save to History", value=True, help="Automatically save generated music")
        
        # Enhanced generate button
        if st.button("🎼 Generate Music", type="primary", use_container_width=True):
            if not user_input.strip():
                st.error("⚠️ Please enter a description of your desired music!")
                return
                
            with st.spinner("🎵 Analyzing your mood and generating music..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Analyze mood
                    status_text.text("🔍 Analyzing your mood...")
                    progress_bar.progress(25)
                    mood_result = st.session_state.mood_analyzer.analyze_mood(user_input)
                    
                    # Generate musical parameters
                    status_text.text("🎼 Generating musical parameters...")
                    progress_bar.progress(50)
                    musical_params = st.session_state.music_mapper.generate_musical_parameters(mood_result)
                    
                    # Display analysis results
                    with col2:
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        st.markdown("### 🎭 Mood Analysis")
                        mood = mood_result['mood']['mood']
                        energy = mood_result['energy']['energy_level']
                        sentiment = mood_result['sentiment']['primary_sentiment']
                        
                        st.markdown(f"""
                        **🎭 Mood:** {get_mood_emoji(mood)} {mood.title()}  
                        **⚡ Energy:** {energy}/10  
                        **💭 Sentiment:** {Config.EMOJI_MAPPING.get(sentiment, '😐')} {sentiment.title()}
                        """)
                        
                        st.markdown("### 🎼 Musical Settings")
                        st.markdown(f"""
                        **🥁 Tempo:** {musical_params['tempo']} BPM  
                        **🎹 Key:** {musical_params['key'].title()}  
                        **🎸 Instruments:** {', '.join(musical_params['instruments'][:3])}
                        """)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Generate music if model is available
                    if st.session_state.music_generator:
                        status_text.text("🎵 Generating your music...")
                        progress_bar.progress(75)
                        
                        audio_array, sample_rate = st.session_state.music_generator.generate_music(
                            musical_params, duration, guidance_scale
                        )
                        
                        # Process audio
                        status_text.text("🎧 Processing audio...")
                        progress_bar.progress(90)
                        
                        processor = AudioProcessor()
                        processed_audio = processor.process_generated_audio(
                            audio_array, sample_rate, energy, output_format
                        )
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Music generation complete!")
                        
                        # Enhanced audio player
                        st.markdown('<div class="music-player-container">', unsafe_allow_html=True)
                        st.markdown("### 🎵 Your Generated Music")
                        st.audio(processed_audio['audio_bytes'], format=f"audio/{output_format}")
                        
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Duration", f"{processed_audio['duration']:.1f}s")
                        with col_b:
                            st.metric("File Size", f"{processed_audio['file_size']/1024:.1f} KB")
                        with col_c:
                            st.metric("Quality", f"{output_format.upper()}")
                        
                        # Download button
                        filename = f"ai_music_{mood}_energy{energy}_{int(time.time())}.{output_format}"
                        st.download_button(
                            "💾 Download Music",
                            processed_audio['audio_bytes'],
                            filename,
                            f"audio/{output_format}",
                            use_container_width=True
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Save to history with audio
                        if auto_save_history:
                            success = db.save_prompt_history_with_audio(
                                st.session_state.user['id'],
                                user_input,
                                mood,
                                energy,
                                json.dumps(musical_params, default=str),
                                processed_audio['audio_bytes'],
                                output_format,
                                processed_audio['duration']
                            )
                            if success:
                                st.success("✅ Music saved to your history with audio!")
                                st.balloons()
                            else:
                                st.warning("⚠️ Music generated but couldn't save to history")
                    
                    else:
                        progress_bar.progress(100)
                        status_text.text("ℹ️ Analysis complete - Music generation unavailable")
                        st.info("🎼 Music generation model not available, showing analysis only.")
                        
                        # Still save analysis to history
                        if auto_save_history:
                            db.save_prompt_history(
                                st.session_state.user['id'],
                                user_input,
                                mood,
                                energy,
                                json.dumps(musical_params, default=str)
                            )
                    
                except Exception as e:
                    st.error(f"❌ Error during generation: {str(e)}")
                    st.exception(e)
                finally:
                    progress_bar.empty()
                    status_text.empty()
    
    with col2:
        if not user_input:
            st.markdown("""
            <div class="analysis-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎵</div>
                <h3>Ready to Create!</h3>
                <p>Enter your mood description to see AI analysis and generate personalized music.</p>
            </div>
            """, unsafe_allow_html=True)

def show_navigation():
    """Show enhanced navigation buttons in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        
        nav_buttons = [
            ("🏠 Home", 'home'),
            ("🎼 Music Generator", 'generator'),
            ("📚 History", 'history')
        ]
        
        for label, page in nav_buttons:
            if st.button(label, use_container_width=True):
                st.session_state.page = page
                st.rerun()
        
        st.markdown("---")
        
        # Enhanced user info
        if st.session_state.authenticated:
            st.markdown(f"""
            <div style="background: rgba(0, 0, 0, 0.1); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
                <strong>{st.session_state.user['name']}</strong><br>
                <small>@{st.session_state.user['username']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.page = 'signin'
                st.success("👋 Logged out successfully!")
                time.sleep(1)
                st.rerun()

def main():
    """Main application function"""
    init_session_state()
    
    # Show authentication pages if not authenticated
    if not st.session_state.authenticated:
        if st.session_state.page == 'signup':
            show_signup_page()
        else:
            show_signin_page()
    else:
        # Show navigation
        show_navigation()
        
        # Show appropriate page
        if st.session_state.page == 'home':
            show_home_page()
        elif st.session_state.page == 'generator':
            show_generator_page()
        elif st.session_state.page == 'history':
            show_history_page()
        else:
            show_home_page()

if __name__ == "__main__":
    main()
