#!/bin/bash

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt file not found"
    exit 1
fi

# Read requirements.txt line by line and install packages
while IFS= read -r package || [ -n "$package" ]; do
    # Skip empty lines and comments
    if [ -z "$package" ] || [[ $package == \#* ]]; then
        continue
    fi
    
    echo "Installing $package..."
    pip install "$package"
    
    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "Error installing $package"
        exit 1
    fi
done < "requirements.txt"

echo "All packages installed successfully"
