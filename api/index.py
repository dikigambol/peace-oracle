import sys
import os

# Add parent directory to sys.path to allow imports from root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# For local testing if executed directly
if __name__ == "__main__":
    app.run()
