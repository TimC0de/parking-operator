import sqlite3
import os

DATABASE_NAME = "Parking.db"


def migrate():
    """Create message_history table if it doesn't exist"""
    # Ensure the database directory exists
    db_dir = os.path.dirname(DATABASE_NAME)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    
    try:
        # Create message_history table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                sender TEXT NOT NULL,
                message_content TEXT NOT NULL,
                sent_date TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES session(id)
            )
        """)
        
        connection.commit()
        print("✅ Successfully created message_history table")
        
        # Verify table was created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message_history'")
        if cursor.fetchone():
            print("✅ Table verification successful")
        else:
            print("❌ Table verification failed")
            
    except Exception as e:
        print(f"❌ Error creating message_history table: {e}")
        connection.rollback()
    finally:
        connection.close()


if __name__ == "__main__":
    migrate()
