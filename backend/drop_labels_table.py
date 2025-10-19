#!/usr/bin/env python3
"""
Script to drop the unused 'labels' table from the database.
Run this after confirming that the labels table is empty and all functionality
has been migrated to the shipping_labels system.
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def drop_labels_table():
    # Load environment variables
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL not found in environment variables")
        return False
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Check if table exists and is empty
        with engine.connect() as connection:
            # Check if table exists
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'labels'
                );
            """))
            table_exists = result.fetchone()[0]
            
            if not table_exists:
                print("✅ Labels table does not exist. Nothing to drop.")
                return True
            
            # Check if table is empty
            result = connection.execute(text("SELECT COUNT(*) FROM labels;"))
            count = result.fetchone()[0]
            
            if count > 0:
                print(f"⚠️ WARNING: Labels table contains {count} records!")
                print("Please ensure all data is migrated before dropping the table.")
                confirm = input("Continue anyway? (yes/no): ").lower().strip()
                if confirm != 'yes':
                    print("❌ Operation cancelled.")
                    return False
            
            # Drop the table
            print("🗑️ Dropping labels table...")
            connection.execute(text("DROP TABLE IF EXISTS labels CASCADE;"))
            connection.commit()
            
            print("✅ Successfully dropped labels table!")
            return True
            
    except Exception as e:
        print(f"❌ Error dropping labels table: {e}")
        return False

if __name__ == "__main__":
    print("🚨 Label Table Cleanup Script")
    print("================================")
    print("This script will DROP the 'labels' table from the database.")
    print("Make sure you have:")
    print("1. ✅ Verified the table is empty (0 records)")
    print("2. ✅ Migrated all functionality to shipping_labels")
    print("3. ✅ Tested the application without label endpoints")
    print()
    
    confirm = input("Are you sure you want to proceed? (yes/no): ").lower().strip()
    if confirm == 'yes':
        success = drop_labels_table()
        if success:
            print("\n🎉 Cleanup completed successfully!")
            print("The labels table has been removed from the database.")
        else:
            print("\n💥 Cleanup failed. Please check the error messages above.")
    else:
        print("\n❌ Operation cancelled by user.")