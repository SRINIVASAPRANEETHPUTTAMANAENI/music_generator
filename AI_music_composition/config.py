"""
Configuration settings for AI Music Composition Engine
Contains all constants, model settings, and mappings used throughout the application
"""

import torch

class Config:
    # =============================================================================
    # MODEL CONFIGURATION
    # =============================================================================
    
    # Hugging Face Models
    SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MUSICGEN_MODEL_NAME = "facebook/musicgen-small"
    
    # Model Parameters
    MAX_LENGTH = 128
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Audio Processing
    DEFAULT_SAMPLE_RATE = 32000
    DEFAULT_DURATION = 30.0  # seconds
    MAX_DURATION = 30.0  # MusicGen small model limit

    # =============================================================================
    # MOOD ANALYSIS CONFIGURATION
    # =============================================================================
    
    # Mood Categories with Descriptions
    MOOD_CATEGORIES = {
        "happy": "joyful, upbeat, cheerful, positive energy, celebration",
        "sad": "melancholic, sorrowful, emotional, introspective, blue",
        "calm": "peaceful, relaxed, serene, tranquil, meditation",
        "energetic": "high energy, powerful, dynamic, intense, active",
        "mysterious": "dark, enigmatic, atmospheric, suspenseful, unknown",
        "romantic": "loving, tender, intimate, passionate, affectionate"
    }
    
    # Energy Level Keywords
    HIGH_ENERGY_KEYWORDS = [
        "excited", "energetic", "pumped", "intense", "powerful", "dynamic",
        "fast", "quick", "rush", "adrenaline", "workout", "party", "dance",
        "explosive", "vibrant", "electric", "charged", "aggressive", "fierce"
    ]
    
    LOW_ENERGY_KEYWORDS = [
        "calm", "peaceful", "quiet", "slow", "gentle", "soft", "relaxed",
        "tired", "sleepy", "meditation", "ambient", "minimal", "subtle",
        "tranquil", "serene", "mellow", "laid-back", "chill", "drowsy"
    ]
    
    # Energy Calculation Parameters
    BASE_ENERGY = 5
    TEMPO_ENERGY_MULTIPLIER = 8
    SENTIMENT_ENERGY_BOOST = {
        "positive": 2,
        "negative": -1,
        "neutral": 0
    }

    # =============================================================================
    # MUSICAL PARAMETER MAPPINGS
    # =============================================================================
    
    # Mood to Tempo Mapping (BPM)
    MOOD_TO_TEMPO = {
        "happy": {"base": 120, "range": (100, 140)},
        "sad": {"base": 70, "range": (60, 90)},
        "calm": {"base": 80, "range": (65, 95)},
        "energetic": {"base": 130, "range": (120, 160)},
        "mysterious": {"base": 90, "range": (70, 110)},
        "romantic": {"base": 85, "range": (70, 100)}
    }
    
    # Mood to Key Mapping
    MOOD_TO_KEY = {
        "happy": "major",
        "sad": "minor",
        "calm": "major",
        "energetic": "major",
        "mysterious": "minor",
        "romantic": "major"
    }
    
    # Mood to Instruments Mapping
    MOOD_TO_INSTRUMENTS = {
        "happy": ["piano", "guitar", "drums", "brass", "strings"],
        "sad": ["piano", "cello", "violin", "soft_strings", "flute"],
        "calm": ["piano", "acoustic_guitar", "flute", "harp", "ambient_pads"],
        "energetic": ["electric_guitar", "drums", "bass", "synthesizer", "brass"],
        "mysterious": ["synthesizer", "ambient_pads", "cello", "percussion", "piano"],
        "romantic": ["piano", "violin", "cello", "acoustic_guitar", "soft_strings"]
    }

    # =============================================================================
    # UI CONFIGURATION
    # =============================================================================
    
    # Enhanced sample texts with 15 prompts total
    SAMPLE_TEXTS = [
        "I'm feeling happy and energetic today!",
        "I need some calm music for studying",
        "Feeling a bit sad and melancholic",
        "Want something mysterious and atmospheric",
        "Looking for romantic and tender music",
        "Need high-energy music for my workout",
        "I want to feel motivated and inspired",
        "Creating peaceful music for meditation",
        "Need something uplifting for a celebration",
        "Want dark and moody background music",
        "Looking for gentle music to help me sleep",
        "Need energetic music for dancing",
        "Want nostalgic and emotional melodies",
        "Creating dramatic and cinematic sounds",
        "Looking for cheerful music to brighten my day"
    ]
    
    # Emoji Mappings for UI
    EMOJI_MAPPING = {
        "happy": "😊",
        "sad": "😢",
        "calm": "😌",
        "energetic": "⚡",
        "mysterious": "🌙",
        "romantic": "💖",
        "positive": "😊",
        "negative": "😔",
        "neutral": "😐"
    }
    
    # Instrument Emojis
    INSTRUMENT_EMOJIS = {
        "piano": "🎹",
        "guitar": "🎸",
        "electric_guitar": "🎸",
        "acoustic_guitar": "🎸",
        "drums": "🥁",
        "bass": "🎸",
        "violin": "🎻",
        "cello": "🎻",
        "flute": "🪈",
        "harp": "🪕",
        "brass": "🎺",
        "synthesizer": "🎹",
        "strings": "🎻",
        "soft_strings": "🎻",
        "ambient_pads": "🌊",
        "percussion": "🥁",
        "saxophone": "🎷"
    }
    
    # Color Scheme for UI
    PRIMARY_COLOR = "#1f77b4"
    SECONDARY_COLOR = "#ff7f0e"
    SUCCESS_COLOR = "#2ca02c"
    WARNING_COLOR = "#d62728"
    INFO_COLOR = "#17becf"

    # =============================================================================
    # AUDIO PROCESSING CONFIGURATION
    # =============================================================================
    
    # Audio Quality Settings
    MP3_BITRATE = "128k"
    WAV_SAMPLE_WIDTH = 2  # 16-bit
    NORMALIZATION_TARGET_RMS = 0.1
    MAX_GAIN_DB = 20.0
    
    # Volume Adjustment by Energy Level
    ENERGY_VOLUME_MAP = {
        1: 0.4, 2: 0.5, 3: 0.6,
        4: 0.7, 5: 0.8, 6: 0.9,
        7: 1.0, 8: 1.1, 9: 1.2, 10: 1.3
    }

    # =============================================================================
    # GENERATION PARAMETERS
    # =============================================================================
    
    # MusicGen Generation Settings
    DEFAULT_GUIDANCE_SCALE = 3.0
    DEFAULT_DO_SAMPLE = True
    MAX_NEW_TOKENS_LIMIT = 1503  # For musicgen-small
    TOKENS_PER_SECOND = 50  # MusicGen token rate
    
    # Prompt Engineering
    MAX_PROMPT_LENGTH = 200
    PROMPT_TEMPLATES = {
        "default": "{mood} {tempo_desc} {key_desc} music with {instruments}",
        "detailed": "{mood} {sentiment} {tempo_desc} {key_desc} instrumental music featuring {instruments} with {energy_desc} energy"
    }
    
    # Super Enhanced Authentication styling with animations and modern design
    AUTH_STYLE = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .auth-container {
            max-width: 450px;
            margin: 2rem auto;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.1), 
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            backdrop-filter: blur(20px);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .auth-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(255,255,255,0.1), transparent);
            pointer-events: none;
        }
        
        .auth-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            color: white;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        .home-container {
            max-width: 1000px;
            margin: 1rem auto;
            padding: 2rem;
            text-align: center;
            animation: fadeInUp 0.8s ease-out;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 2.5rem;
            margin: 1.5rem;
            border-radius: 20px;
            box-shadow: 
                0 10px 15px -3px rgba(0, 0, 0, 0.1), 
                0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 
                0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(103, 126, 234, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .feature-card:hover::before {
            left: 100%;
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 25px;
            color: white;
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
            animation: slideDown 0.6s ease-out;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>');
            background-size: 50px 50px;
            animation: float 20s infinite linear;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 1rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.1), 
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        .history-item {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            padding: 2rem;
            margin: 1rem 0;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            animation: slideInLeft 0.5s ease-out;
        }
        
        .history-item:hover {
            transform: translateX(10px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .music-player-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .analysis-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(103, 126, 234, 0.2);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .prompt-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            margin: 0.25rem;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .prompt-button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(103, 126, 234, 0.4);
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes glow {
            from {
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            to {
                text-shadow: 0 2px 4px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.5);
            }
        }
        
        @keyframes float {
            from { transform: translateX(-100px); }
            to { transform: translateX(calc(100vw + 100px)); }
        }
        
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            border: 1px solid rgba(103, 126, 234, 0.3);
        }
        
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.95);
            color: black !important;
            border-radius: 10px;
            border: 1px solid rgba(103, 126, 234, 0.3);
            padding: 0.75rem 1rem;
        }
        
        .stTextArea > div > div > textarea {
            background: rgba(255, 255, 255, 0.95);
            color: black !important;
            border-radius: 10px;
            border: 1px solid rgba(103, 126, 234, 0.3);
            padding: 1rem;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #5a6fd8, #6b46a3);
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #666 !important;
        }
    </style>
    """
