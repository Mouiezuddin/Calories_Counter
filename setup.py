#!/usr/bin/env python3
"""
NutriCore Calorie Tracker - Automated Setup Script

This script automates the entire setup process:
- Creates virtual environment
- Installs dependencies
- Creates .env file from template
- Initializes database (optional)

Usage:
    python setup.py
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path


class Setup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.env_file = self.project_root / ".env"
        self.env_example = self.project_root / ".env.example"
        self.requirements_file = self.project_root / "requirements.txt"
        self.app_file = self.project_root / "app.py"
        self.os_type = platform.system()
        
    def print_header(self):
        """Print setup header"""
        print("\n" + "=" * 50)
        print("🍎 NutriCore Calorie Tracker - Setup")
        print("=" * 50 + "\n")
    
    def print_step(self, step_num, message):
        """Print step message"""
        print(f"[{step_num}] {message}")
    
    def print_success(self, message):
        """Print success message"""
        print(f"✓ {message}")
    
    def print_error(self, message):
        """Print error message"""
        print(f"❌ {message}")
        sys.exit(1)
    
    def print_info(self, message):
        """Print info message"""
        print(f"ℹ️  {message}")
    
    def check_python(self):
        """Check Python version"""
        self.print_step(1, "Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_error(f"Python 3.8+ required. Found: {version.major}.{version.minor}")
        
        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} found")
    
    def check_venv_exists(self):
        """Check if virtual environment already exists"""
        if self.venv_path.exists():
            self.print_info("Virtual environment already exists")
            return True
        return False
    
    def create_venv(self):
        """Create virtual environment"""
        self.print_step(2, "Creating virtual environment...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(self.venv_path)])
            self.print_success("Virtual environment created")
        except subprocess.CalledProcessError:
            self.print_error("Failed to create virtual environment")
    
    def get_pip_executable(self):
        """Get pip executable path"""
        if self.os_type == "Windows":
            return self.venv_path / "Scripts" / "pip.exe"
        else:
            return self.venv_path / "bin" / "pip"
    
    def get_python_executable(self):
        """Get python executable path"""
        if self.os_type == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"
    
    def install_dependencies(self):
        """Install dependencies from requirements.txt"""
        self.print_step(3, "Installing dependencies...")
        
        pip_exe = self.get_pip_executable()
        
        if not pip_exe.exists():
            self.print_error(f"pip not found at {pip_exe}")
        
        try:
            # Upgrade pip
            subprocess.check_call([str(pip_exe), "install", "--upgrade", "pip"])
            
            # Install requirements
            subprocess.check_call([str(pip_exe), "install", "-r", str(self.requirements_file)])
            self.print_success("Dependencies installed")
        except subprocess.CalledProcessError:
            self.print_error("Failed to install dependencies")
    
    def create_env_file(self):
        """Create .env file from template"""
        self.print_step(4, "Setting up environment file...")
        
        if self.env_file.exists():
            self.print_info(".env file already exists")
            return
        
        if not self.env_example.exists():
            self.print_error(f".env.example not found at {self.env_example}")
        
        try:
            shutil.copy(str(self.env_example), str(self.env_file))
            self.print_success(".env file created from template")
        except Exception as e:
            self.print_error(f"Failed to create .env file: {e}")
    
    def init_database(self):
        """Initialize database by importing app"""
        self.print_step(5, "Initializing database...")
        
        try:
            # Add project root to path
            sys.path.insert(0, str(self.project_root))
            
            # Import app to trigger database creation
            from app import app, db
            
            with app.app_context():
                db.create_all()
                self.print_success("Database initialized")
        except Exception as e:
            self.print_info(f"Database initialization skipped: {e}")
    
    def print_next_steps(self):
        """Print next steps"""
        print("\n" + "=" * 50)
        print("✅ Setup Complete!")
        print("=" * 50 + "\n")
        
        if self.os_type == "Windows":
            activate_cmd = ".\\venv\\Scripts\\activate.bat"
        else:
            activate_cmd = "source venv/bin/activate"
        
        print("Next steps:")
        print(f"  1. Activate virtual environment:")
        print(f"     {activate_cmd}")
        print(f"\n  2. Run the application:")
        print(f"     python app.py")
        print(f"\n  3. Open in browser:")
        print(f"     http://localhost:5000")
        print("\n" + "=" * 50 + "\n")
    
    def run(self):
        """Run the complete setup"""
        try:
            self.print_header()
            
            self.check_python()
            
            if not self.check_venv_exists():
                self.create_venv()
            
            self.install_dependencies()
            self.create_env_file()
            self.init_database()
            
            self.print_next_steps()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Setup cancelled by user")
            sys.exit(0)
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")


def main():
    """Main entry point"""
    setup = Setup()
    setup.run()


if __name__ == "__main__":
    main()
