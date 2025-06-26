#!/usr/bin/env python3
"""
FIBO Semantic Agent Web UI Launcher
Simple script to launch the Streamlit web interface
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        print("✅ Streamlit available")
        return True
    except ImportError:
        print("❌ Streamlit not found. Please install with:")
        print("   pip install streamlit")
        return False

def check_planner():
    """Check if planner is available"""
    try:
        from planner import run_natural_language_query
        print("✅ FIBO planner available")
        return True
    except ImportError as e:
        print(f"❌ FIBO planner not available: {e}")
        print("   Make sure you're in the correct directory with planner.py")
        return False

def launch_streamlit():
    """Launch the Streamlit app"""
    app_file = Path(__file__).parent / "fibo_web_ui.py"
    
    if not app_file.exists():
        print(f"❌ Web UI file not found: {app_file}")
        return False
    
    print(f"🚀 Launching FIBO Semantic Agent Web UI...")
    print(f"📁 App file: {app_file}")
    print(f"🌐 Opening in browser...")
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_file),
            "--server.headless", "false",
            "--server.port", "8501",
            "--theme.base", "light"
        ])
        return True
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")
        return False

def main():
    """Main launcher function"""
    print("🧠 FIBO Semantic Agent Web UI Launcher")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    if not check_planner():
        return False
    
    # Launch the web UI
    return launch_streamlit()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)