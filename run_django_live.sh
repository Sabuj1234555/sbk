#!/bin/bash

# ===============================
# Django Live Server + ngrok Script
# ===============================

# 1. Check if ngrok exists
if ! command -v ngrok &> /dev/null
then
    echo "Ngrok not found! Downloading..."
    wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip -O ngrok.zip
    unzip ngrok.zip
    chmod +x ngrok
    mv ngrok $PREFIX/bin/
    rm ngrok.zip
    echo "Ngrok installed!"
fi

# 2. Ask for Django project path
read -p "Enter your Django project path: " PROJECT_PATH

cd "$PROJECT_PATH" || { echo "Project path not found!"; exit 1; }

# 3. Run Django server in background
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

sleep 2

# 4. Start ngrok
echo "Starting ngrok..."
ngrok http 8000
# Ctrl+C to stop ngrok

# 5. Stop Django server when done
kill $DJANGO_PID
