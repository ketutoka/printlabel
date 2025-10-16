"""
Database migration script to make shipping_code nullable
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
        # Drop unique constraint on shipping_code if exists
        try:
            connection.execute(text("""
                ALTER TABLE shipping_labels 
                DROP CONSTRAINT IF EXISTS shipping_labels_shipping_code_key;
            """))
            print("✅ Dropped unique constraint on shipping_code")
        except Exception as e:
            print(f"⚠️ Warning dropping unique constraint: {e}")
        
        # Make shipping_code nullable
        try:
            connection.execute(text("""
                ALTER TABLE shipping_labels 
                ALTER COLUMN shipping_code DROP NOT NULL;
            """))
            print("✅ Made shipping_code nullable")
        except Exception as e:
            print(f"⚠️ Warning making shipping_code nullable: {e}")
        
        connection.commit()
        print("\n🎉 Database migration completed successfully!")
        print("- shipping_code is now nullable")
        print("- unique constraint removed from shipping_code")

except Exception as e:
    print(f"❌ Migration failed: {e}")
    exit(1)