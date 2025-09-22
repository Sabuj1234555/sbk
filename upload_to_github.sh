# Line 6-এ থাকা secret বা token মুছে দিন#!/bin/bash

# === কনফিগারেশন ===
GITHUB_USER="Sabuj1234555"
REPO_NAME="sbk"


# === Django প্রোজেক্ট লোকেশন ===
PROJECT_PATH="/storage/emulated/0/Download/sbk_music/myproject/myproject"

# === GitHub Repo URL (TOKEN সহ) ===
REMOTE_URL="https://$GITHUB_USER:$TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"

# === Script Start ===
echo "[INFO] প্রোজেক্ট ফোল্ডারে যাচ্ছি..."
cd "$PROJECT_PATH" || exit

echo "[INFO] Git init করছি..."
git init

echo "[INFO] Safe directory সেট করছি..."
git config --global --add safe.directory "$PROJECT_PATH"

echo "[INFO] User info সেট করছি..."
git config --global user.name "$GITHUB_USER"
git config --global user.email "your_email@example.com"

echo "[INFO] .gitignore তৈরি করছি..."
cat > .gitignore <<EOL
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
*.log
env/
venv/
*.egg-info/
staticfiles/
media/
EOL

echo "[INFO] সব ফাইল add করছি..."
git add .

echo "[INFO] Commit করছি..."
git commit -m "Initial commit" || echo "[WARN] Commit স্কিপ করা হলো (হয়তো আগেই commit করা হয়েছে)"

echo "[INFO] Remote সেট করছি..."
git branch -M main
git remote remove origin 2>/dev/null
git remote add origin "$REMOTE_URL"

echo "[INFO] GitHub এ push করছি..."
git push -u origin main

echo "[DONE] 🎉 তোমার প্রোজেক্ট GitHub রিপো '$REPO_NAME' এ আপলোড হয়ে গেছে!"
