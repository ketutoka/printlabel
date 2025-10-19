#!/usr/bin/env python3
"""
Script to update some existing shipping labels to 80mm for testing
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_sample_labels_to_80mm():
    """Update some existing labels to 80mm for testing"""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                print("🔍 Checking current label_size distribution...")
                
                # Check current distribution
                result = conn.execute(text("""
                    SELECT 
                        label_size,
                        COUNT(*) as count
                    FROM shipping_labels 
                    GROUP BY label_size
                """))
                
                current_dist = result.fetchall()
                print("Current distribution:")
                for row in current_dist:
                    print(f"   {row.label_size}: {row.count} labels")
                
                # Check if we have any labels
                result = conn.execute(text("SELECT COUNT(*) as total FROM shipping_labels"))
                total_labels = result.fetchone().total
                
                if total_labels == 0:
                    print("❌ No labels found in database")
                    return False
                
                print(f"\n🔄 Updating some labels to 80mm for testing...")
                
                # Update every 3rd label to 80mm (to create a mix)
                result = conn.execute(text("""
                    UPDATE shipping_labels 
                    SET label_size = '80mm'
                    WHERE id % 3 = 0
                    AND label_size != '80mm'
                """))
                
                updated_count = result.rowcount
                print(f"✅ Updated {updated_count} labels to 80mm")
                
                # Check new distribution
                result = conn.execute(text("""
                    SELECT 
                        label_size,
                        COUNT(*) as count
                    FROM shipping_labels 
                    GROUP BY label_size
                """))
                
                new_dist = result.fetchall()
                print("\nNew distribution:")
                for row in new_dist:
                    print(f"   {row.label_size}: {row.count} labels")
                
                # Show some examples
                result = conn.execute(text("""
                    SELECT 
                        id,
                        sender_name,
                        label_size,
                        created_at
                    FROM shipping_labels 
                    WHERE label_size = '80mm'
                    ORDER BY created_at DESC
                    LIMIT 5
                """))
                
                examples = result.fetchall()
                if examples:
                    print("\nExamples of 80mm labels:")
                    for label in examples:
                        print(f"   ID:{label.id} | {label.sender_name} | {label.label_size} | {label.created_at}")
                
                trans.commit()
                print("\n🎉 Update completed successfully!")
                return True
                
            except Exception as e:
                trans.rollback()
                raise e
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_sample_labels_to_80mm()