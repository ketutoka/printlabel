-- Migration SQL Script
-- Run this directly in PostgreSQL to add phone field to users table
-- and create shipping_labels table

-- Add phone column to users table (if not exists)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'phone'
    ) THEN
        ALTER TABLE users ADD COLUMN phone VARCHAR(20);
        RAISE NOTICE 'Added phone column to users table';
    ELSE
        RAISE NOTICE 'Phone column already exists in users table';
    END IF;
END $$;

-- Create shipping_labels table (if not exists)
CREATE TABLE IF NOT EXISTS shipping_labels (
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

-- Show success message
DO $$ 
BEGIN
    RAISE NOTICE 'Migration completed successfully!';
    RAISE NOTICE 'Users table now has phone column';
    RAISE NOTICE 'Shipping_labels table created';
END $$;