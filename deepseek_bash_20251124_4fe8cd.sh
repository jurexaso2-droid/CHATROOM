#!/data/data/com.termux/files/usr/bin/bash

echo "Installing ReCHAT for Termux..."
pkg update -y
pkg install python wget -y
pip install --upgrade pip
pip install requests

echo "Making scripts executable..."
chmod +x rechat.py server.py client.py

echo "Installation complete!"
echo ""
echo "To start ReCHAT:"
echo "python rechat.py"
echo ""
echo "Features:"
echo "✅ Auto ngrok installation"
echo "✅ User registration/login"
echo "✅ Real-time chat"
echo "✅ No port forwarding needed"