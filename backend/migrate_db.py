"""
Database migration script to add phone field to users table
Run this script to update existing database schema
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env file")
    exit(1)

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        # Check if phone column already exists
        result = connection.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'phone';
        """))
        
        if result.fetchone():
            print("✅ Phone column already exists in users table")
        else:
            # Add phone column to users table
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN phone VARCHAR(20);
            """))
            
            connection.commit()
            print("✅ Successfully added phone column to users table")
        
        # Check if shipping_labels table exists, if not create it
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'shipping_labels';
        """))
        
        if result.fetchone():
            print("✅ Shipping_labels table already exists")
        else:
            # Create shipping_labels table
            connection.execute(text("""
                CREATE TABLE shipping_labels (
                    id SERIAL PRIMARY KEY,
                    sender_name VARCHAR(255) NOT NULL,
                    sender_phone VARCHAR(20) NOT NULL,
                    recipient_name VARCHAR(255) NOT NULL,
                    recipient_address TEXT NOT NULL,
                    recipient_phone VARCHAR(20) NOT NULL,
                    shipping_code VARCHAR(100) UNIQUE NOT NULL,
                    image_path TEXT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """))
            
            connection.commit()
            print("✅ Successfully created shipping_labels table")
        
        print("\n🎉 Database migration completed successfully!")
        print("\nUpdated schema:")
        print("- users table: added phone column")
        print("- shipping_labels table: created with all required fields")

except Exception as e:
    print(f"❌ Migration failed: {e}")
    exit(1)