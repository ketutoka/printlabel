#!/usr/bin/env python3
"""
Migration script to make recipient fields optional in shipping_labels table
"""

import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Run the database migration to make recipient fields nullable and add label_size"""
    
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        print("🔄 Starting migration to make recipient fields optional and add label_size...")
        
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                # Make recipient_name nullable
                print("📝 Making recipient_name nullable...")
                conn.execute(text("""
                    ALTER TABLE shipping_labels 
                    ALTER COLUMN recipient_name DROP NOT NULL
                """))
                
                # Make recipient_address nullable
                print("📝 Making recipient_address nullable...")
                conn.execute(text("""
                    ALTER TABLE shipping_labels 
                    ALTER COLUMN recipient_address DROP NOT NULL
                """))
                
                # Make recipient_phone nullable
                print("📝 Making recipient_phone nullable...")
                conn.execute(text("""
                    ALTER TABLE shipping_labels 
                    ALTER COLUMN recipient_phone DROP NOT NULL
                """))
                
                # Add label_size column
                print("📝 Adding label_size column...")
                conn.execute(text("""
                    ALTER TABLE shipping_labels 
                    ADD COLUMN label_size VARCHAR(10) NOT NULL DEFAULT '58mm'
                """))
                
                # Commit transaction
                trans.commit()
                print("✅ Migration completed successfully!")
                print("📋 Changes:")
                print("   • Recipient fields (name, address, phone) are now optional")
                print("   • Added label_size column with default '58mm'")
                return True
                
            except Exception as e:
                # Rollback on error
                trans.rollback()
                raise e
                
    except SQLAlchemyError as e:
        print(f"❌ Database error during migration: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        return False

def verify_migration():
    """Verify that the migration was successful"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        return False
    
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Check table structure
            result = conn.execute(text("""
                SELECT column_name, is_nullable, column_default 
                FROM information_schema.columns 
                WHERE table_name = 'shipping_labels' 
                AND column_name IN ('recipient_name', 'recipient_address', 'recipient_phone', 'label_size')
                ORDER BY column_name
            """))
            
            print("\n📊 Current column status:")
            for row in result:
                nullable_status = "✅ NULLABLE" if row.is_nullable == "YES" else "❌ NOT NULL"
                default_val = f" (default: {row.column_default})" if row.column_default else ""
                print(f"   {row.column_name}: {nullable_status}{default_val}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting enhanced migration for shipping labels...")
    print("=" * 60)
    
    if run_migration():
        print("\n🔍 Verifying migration...")
        verify_migration()
        print("\n🎉 Migration process completed!")
        print("\nNew features available:")
        print("  • recipient_name can be empty")
        print("  • recipient_address can be empty") 
        print("  • recipient_phone can be empty")
        print("  • shipping_code was already optional")
        print("  • label_size supports 58mm and 80mm")
        print("\n📱 Frontend now supports multiple label sizes with adaptive layouts.")
    else:
        print("\n💥 Migration failed. Please check the errors above.")