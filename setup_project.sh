#!/bin/bash

# Create a new directory for your project
mkdir discord_sentiment_project
cd discord_sentiment_project

# Initialize a git repository
git init

# Create a .gitignore file
echo "# Python
*.pyc
__pycache__/
venv/
*.db
.env
# IDE
.vscode/
.idea/
# Misc
.DS_Store" > .gitignore

# Create a README file
echo "# Discord Sentiment Analysis Project

This project analyzes sentiment and topics in Discord messages for the game 'Walker World' using Transformers and HuggingFace models." > README.md

# Make initial commit
git add .
git commit -m "Initial commit: Project setup"

echo "Project setup complete!"