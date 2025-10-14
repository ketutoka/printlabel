import os
import sys
from pathlib import Path

def check_environment():
    """Check if environment is properly set up"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Error: .env file not found!")
        print("Please copy .env.example to .env and configure your settings.")
        return False
    
    # Load and check required environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["DATABASE_URL", "SECRET_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file.")
        return False
    
    return True

def create_labels_directory():
    """Create labels directory if it doesn't exist"""
    labels_dir = Path("labels")
    labels_dir.mkdir(exist_ok=True)
    print(f"✅ Labels directory ready: {labels_dir.absolute()}")

if __name__ == "__main__":
    print("🏷️ Print Label Application - Starting up...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Create necessary directories
    create_labels_directory()
    
    # Import and start the application
    try:
        from main import app
        import uvicorn
        
        print("✅ Environment check passed")
        print("🚀 Starting FastAPI server...")
        print("📍 Server will be available at: http://localhost:8002")
        print("📖 API docs will be available at: http://localhost:8002/docs")
        print("=" * 50)
        
        uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed with: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)