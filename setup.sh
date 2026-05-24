#!/bin/bash

# One-Click Termux Deployment Script for Anime Stream Bot
echo "Starting deployment..."

# Update and upgrade packages
pkg update -y && pkg upgrade -y

# Install necessary packages
pkg install python ffmpeg mediainfo git tmux -y

# Upgrade pip
pip install -U pip

# Install requirements
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env template..."
    echo "API_ID=" > .env
    echo "API_HASH=" >> .env
    echo "BOT_TOKEN=" >> .env
    echo "MONGO_URI=" >> .env
    echo "BASE_URL=" >> .env
    echo ".env created! Please fill in your credentials before running bot.py"
fi

echo "Deployment finished successfully!"
echo "Use 'python bot.py' to start the bot."
echo "Use 'tmux' to run the bot 24/7."
