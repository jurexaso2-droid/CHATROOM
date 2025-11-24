#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def display_banner():
    os.system('clear')
    banner = """
    ╔══════════════════════════════════════╗
    ║               ReCHAT                 ║
    ║      Real-Time Chat System           ║
    ║         Auto Ngrok Setup             ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

def check_ngrok():
    try:
        subprocess.run(["ngrok", "--version"], capture_output=True, check=True)
        return True
    except:
        return False

def install_ngrok():
    display_banner()
    print("[+] Installing ngrok...")
    try:
        # Download and install ngrok
        subprocess.run(["pkg", "install", "wget", "-y"], capture_output=True)
        subprocess.run(["wget", "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz"], capture_output=True)
        subprocess.run(["tar", "xzf", "ngrok-v3-stable-linux-arm64.tgz"], capture_output=True)
        subprocess.run(["chmod", "+x", "ngrok"], capture_output=True)
        subprocess.run(["mv", "ngrok", "/data/data/com.termux/files/usr/bin/"], capture_output=True)
        
        # Clean up
        if os.path.exists("ngrok-v3-stable-linux-arm64.tgz"):
            os.remove("ngrok-v3-stable-linux-arm64.tgz")
        
        print("[+] Ngrok installed successfully!")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"[-] Failed to install ngrok: {e}")
        return False

def main():
    display_banner()
    
    # Check and install dependencies
    print("[+] Checking dependencies...")
    
    # Install Python packages
    try:
        import requests
    except:
        print("[+] Installing requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"])
    
    # Check and install ngrok
    if not check_ngrok():
        print("[-] Ngrok not found!")
        if install_ngrok():
            print("[+] Ngrok setup completed!")
        else:
            print("[-] Ngrok installation failed!")
            return
    
    print("[+] All dependencies are ready!")
    print("\nChoose an option:")
    print("1. Start Chat Server")
    print("2. Join Chat")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        from server import start_server
        start_server()
    elif choice == "2":
        from client import start_client
        start_client()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
