import sqlite3

def fix_database_schema():
    """Fix the database schema by adding missing audio columns or recreating tables"""
    db_path = "music_app.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if prompt_history table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prompt_history';")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Creating tables from scratch...")
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
        
        # Create prompt history table with audio columns
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
        print("Tables created successfully!")
    else:
        # Add missing columns to existing table
        print("Adding missing columns to existing table...")
        
        # Get existing columns
        cursor.execute("PRAGMA table_info(prompt_history);")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        # Add missing columns
        new_columns = {
            'audio_data': 'BLOB',
            'audio_format': 'TEXT',
            'audio_filename': 'TEXT', 
            'duration': 'REAL'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE prompt_history ADD COLUMN {col_name} {col_type}")
                    print(f"Added column: {col_name}")
                except Exception as e:
                    print(f"Error adding {col_name}: {e}")
    
    conn.commit()
    conn.close()
    print("Database schema updated successfully!")

if __name__ == "__main__":
    fix_database_schema()
