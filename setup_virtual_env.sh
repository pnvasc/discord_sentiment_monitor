#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required packages
pip install discord.py pandas sqlalchemy transformers torch datasets

# Save dependencies
pip freeze > requirements.txt

# Commit changes
git add requirements.txt
git commit -m "Add project dependencies"