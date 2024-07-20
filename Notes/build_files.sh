#!/bin/bash

# Ensure the script is executable
chmod +x build_files.sh

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Deactivate the virtual environment (optional)
# deactivate
