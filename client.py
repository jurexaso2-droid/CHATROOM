#!/usr/bin/env python3
import socket
import threading
import sys
import os
import time
import re

def display_banner():
    os.system('clear')
    banner = """
    ╔══════════════════════════════════════╗
    ║               ReCHAT                 ║
    ║          Chat Client                 ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

def get_ngrok_address():
    display_banner()
    print("Connect to ReCHAT Server")
    print("=" * 40)
    print("1. Connect via ngrok URL (shared by server host)")
    print("2. Connect via local network")
    print("3. Back to main menu")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        url = input("Enter ngrok URL (e.g., tcp://0.tcp.ngrok.io:12345): ").strip()
        # Parse ngrok URL
        match = re.match(r'tcp://([^:]+):(\d+)', url)
        if match:
            host = match.group(1)
            port = int(match.group(2))
            return host, port
        else:
            print("Invalid ngrok URL format!")
            return None, None
    elif choice == "2":
        host = input("Server IP: ").strip()
        port = int(input("Port (default 8888): ").strip() or "8888")
        return host, port
    else:
        return None, None

def auth_flow():
    """Handle user registration/login"""
    display_banner()
    print("ReCHAT Authentication")
    print("=" * 30)
    print("1. Register new account")
    print("2. Login")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "3":
        return None, None, None
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    if not username or not password:
        print("Username and password are required!")
        return None, None, None
    
    if choice == "1":
        return "REGISTER", username, password
    elif choice == "2":
        return "LOGIN", username, password
    else:
        return None, None, None

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.username = None
        
    def connect_to_server(self, host, port):
        try:
            display_banner()
            print(f"[+] Connecting to {host}:{port}...")
            self.client.connect((host, port))
            
            # Handle authentication
            action, username, password = auth_flow()
            if not action:
                return
                
            auth_data = f"{action}|{username}|{password}"
            self.client.send(auth_data.encode('utf-8'))
            
            response = self.client.recv(1024).decode('utf-8')
            
            if response == "SUCCESS":
                self.username = username
                print(f"[+] Authentication successful! Welcome {username}")
                time.sleep(2)
                
                # Start receiving thread
                receive_thread = threading.Thread(target=self.receive_messages)
                receive_thread.daemon = True
                receive_thread.start()
                
                self.send_messages()
                
            elif response == "EXISTS":
                print("[-] Username already exists!")
                input("Press Enter to continue...")
            elif response == "FAILED":
                print("[-] Invalid username or password!")
                input("Press Enter to continue...")
            else:
                print("[-] Authentication failed!")
                input("Press Enter to continue...")
            
        except Exception as e:
            print(f"[-] Connection error: {e}")
            input("Press Enter to exit...")
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(f"\r{message}\n{self.username}: ", end='')
                else:
                    print("\n[-] Server disconnected")
                    self.running = False
                    break
            except:
                print("\n[-] Connection lost")
                self.running = False
                break
    
    def send_messages(self):
        display_banner()
        print(f"[+] Connected as {self.username}")
        print("[+] Type your messages and press Enter")
        print("[+] Commands: /users, /help, /quit")
        print("-" * 50)
        
        while self.running:
            try:
                message = input(f"{self.username}: ")
                if message.lower() == '/quit':
                    self.running = False
                    break
                if message.strip():
                    self.client.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                print("\n[!] Disconnecting...")
                self.running = False
                break
            except Exception as e:
                print(f"\n[-] Error sending message: {e}")
                self.running = False
                break
        
        self.client.close()
        print("[+] Disconnected from chat")

def start_client():
    host, port = get_ngrok_address()
    if host and port:
        client = ChatClient()
        client.connect_to_server(host, port)
