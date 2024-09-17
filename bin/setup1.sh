#!/bin/bash
echo "****************************************"
echo " Setting up Capstone Environment"
echo "****************************************"

# Check if Python is installed
echo "Checking if Python is installed..."
if ! command -v python --version &> /dev/null; then
    echo "Python is not installed. Please install Python 3.9+ from https://www.python.org/downloads/"
    exit 1
fi

echo "Checking Python version..."
python --version

echo "Creating a Python virtual environment"
# Adjust for Windows virtual environment
python -m venv ./venv

echo "Configuring the developer environment..."
# Configure environment variables and bash prompt
echo "# DevOps Capstone Project additions" >> ~/.bashrc
echo "export GITHUB_ACCOUNT=$GITHUB_ACCOUNT" >> ~/.bashrc
echo 'export PS1="\[\e]0;\u:\W\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ "' >> ~/.bashrc
# Adjust virtual environment activation for Windows
echo "source ./venv/Scripts/activate" >> ~/.bashrc

echo "Installing Python dependencies..."
# Activate virtual environment and install dependencies
source ./venv/Scripts/activate && python -m pip install --upgrade pip wheel
source ./venv/Scripts/activate && pip install -r requirements.txt
source ./venv/Scripts/activate && pip install pytest

echo "Starting the Postgres Docker container..."
# Make sure Docker Desktop is running, else provide an instruction
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker Desktop for Windows: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Make sure the Docker service is running
docker ps > /dev/null
if [ $? -ne 0 ]; then
    echo "Docker Desktop is not running. Please start Docker Desktop and try again."
    exit 1
fi

# If make is not installed, you'll need to either install it or run the commands manually.
if ! command -v make &> /dev/null; then
    echo "Make is not installed. You need to either install Make for Windows or manually start the Postgres container."
    echo "To manually start the Postgres container, run: docker-compose up -d"
    exit 1
fi

make db

echo "Checking the Postgres Docker container..."
docker ps

echo "****************************************"
echo " Capstone Environment Setup Complete"
echo "****************************************"
echo ""
echo "Use 'exit' to close this terminal and open a new one to initialize the environment"
echo ""