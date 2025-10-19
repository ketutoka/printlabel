#!/usr/bin/env python3
"""
Debug script to check label_size values in database
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_label_sizes():
    """Check what label_size values exist in database"""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment variables")
        return
    
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("🔍 Checking shipping_labels table structure...")
            
            # Check if label_size column exists
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'shipping_labels' 
                AND column_name = 'label_size'
            """))
            
            column_info = result.fetchone()
            if column_info:
                print(f"✅ label_size column exists:")
                print(f"   Type: {column_info.data_type}")
                print(f"   Nullable: {column_info.is_nullable}")
                print(f"   Default: {column_info.column_default}")
            else:
                print("❌ label_size column does NOT exist!")
                return
            
            print("\n📊 Checking label_size distribution...")
            
            # Check label_size values
            result = conn.execute(text("""
                SELECT 
                    label_size,
                    COUNT(*) as count
                FROM shipping_labels 
                GROUP BY label_size
                ORDER BY label_size
            """))
            
            sizes = result.fetchall()
            if sizes:
                print("Label sizes in database:")
                for size_row in sizes:
                    print(f"   {size_row.label_size}: {size_row.count} labels")
            else:
                print("No labels found in database")
            
            print("\n📋 Recent labels with details...")
            
            # Show recent labels with all details
            result = conn.execute(text("""
                SELECT 
                    id,
                    sender_name,
                    recipient_name,
                    shipping_code,
                    label_size,
                    created_at
                FROM shipping_labels 
                ORDER BY created_at DESC
                LIMIT 10
            """))
            
            recent_labels = result.fetchall()
            if recent_labels:
                print("Recent labels:")
                for label in recent_labels:
                    recipient = label.recipient_name or "No recipient"
                    code = label.shipping_code or "No code"
                    print(f"   ID:{label.id} | {label.sender_name} → {recipient} | {code} | Size:{label.label_size} | {label.created_at}")
            else:
                print("No labels found")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_label_sizes()