"""
Database Module for AI Music Composition
Handles user authentication, prompt history, and audio storage
"""

import sqlite3
import hashlib
import os
import base64
from datetime import datetime
import streamlit as st
import json
from typing import Dict, List, Optional, Tuple

class DatabaseManager:
    """Database manager for user authentication, prompt history, and audio storage"""
    
    def __init__(self, db_path: str = "music_app.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced prompt history table with audio storage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prompt_text TEXT NOT NULL,
                mood TEXT,
                energy_level INTEGER,
                generated_params TEXT,
                audio_data BLOB,
                audio_format TEXT,
                audio_filename TEXT,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, name: str, username: str, password: str) -> Tuple[bool, str]:
        """Create new user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, "Username already exists"
            
            # Create new user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
                (name, username, hashed_password)
            )
            conn.commit()
            conn.close()
            return True, "Account created successfully"
            
        except Exception as e:
            return False, f"Error creating account: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            cursor.execute(
                "SELECT id, name, username FROM users WHERE username = ? AND password = ?",
                (username, hashed_password)
            )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return True, {
                    'id': user[0],
                    'name': user[1],
                    'username': user[2]
                }
            return False, None
            
        except Exception as e:
            return False, None
    
    def save_prompt_history_with_audio(self, user_id: int, prompt_text: str, mood: str,
                                     energy_level: int, generated_params: str, 
                                     audio_bytes: bytes = None, audio_format: str = "mp3",
                                     duration: float = 0.0) -> bool:
        """Save prompt and generation history with audio"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate filename
            timestamp = int(datetime.now().timestamp())
            audio_filename = f"music_{mood}_{energy_level}_{timestamp}.{audio_format}" if audio_bytes else None
            
            cursor.execute(
                """INSERT INTO prompt_history 
                   (user_id, prompt_text, mood, energy_level, generated_params, 
                    audio_data, audio_format, audio_filename, duration) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, prompt_text, mood, energy_level, generated_params, 
                 audio_bytes, audio_format, audio_filename, duration)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"Error saving history: {str(e)}")
            return False
    
    def save_prompt_history(self, user_id: int, prompt_text: str, mood: str,
                          energy_level: int, generated_params: str) -> bool:
        """Save prompt history without audio (backward compatibility)"""
        return self.save_prompt_history_with_audio(
            user_id, prompt_text, mood, energy_level, generated_params
        )
    
    def get_user_history(self, user_id: int) -> List[Dict]:
        """Get user's prompt history with audio"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT prompt_text, mood, energy_level, audio_data, audio_format, 
                          audio_filename, duration, created_at 
                   FROM prompt_history WHERE user_id = ? ORDER BY created_at DESC""",
                (user_id,)
            )
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'prompt': row[0],
                    'mood': row[1],
                    'energy': row[2],
                    'audio_data': row[3],
                    'audio_format': row[4],
                    'audio_filename': row[5],
                    'duration': row[6],
                    'date': row[7],
                    'has_audio': row[3] is not None
                })
            
            conn.close()
            return history
            
        except Exception as e:
            st.error(f"Error fetching history: {str(e)}")
            return []
