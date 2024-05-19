#!/bin/bash

# Show Raspberry Pi OS Version
cat /etc/os-release

# Check if the system is running on ARM64 architecture
if [[ $(uname -m) != "aarch64" ]]; then
    echo "This script is intended for ARM64 architecture only. Exiting."
    exit 1
fi

# Update and upgrade the system
sudo apt-get update
# sudo apt-get upgrade -y

# Enable Camera and VNC Interface
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint do_vnc 0

# Test camera
libcamera-hello --list-cameras

# Go to the home directory (or any preferred directory)
cd ~

# Remove any existing miniconda installation
# rm -rf ~/miniconda3

# # Download the latest Miniconda 3 installer script for ARM64 # change to install newest version of python
# Food for thought: https://raspberrytips.com/anaconda-on-raspberry-pi/
# Best shot: https://docs.anaconda.com/free/miniconda/
# Attempts at Miniconda 3 installers:
# https://repo.anaconda.com/miniconda/ #archive of Miniconda, at somepoint they started to fail at least two years ago for aarch64 on rpi
# https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/ # Python 3.11 fails
# https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh # Fails, turns out Miniconda has not been officially supported by Anaconda since at least 2022
# wget https://repo.anaconda.com/miniconda/Miniconda3-py39_24.1.2-0-Linux-aarch64.sh -O ~/miniconda.sh
# swapping to Miniforge since it is the only repo that has confirmed aarch64 for raspberry pi support - and it works! https://github.com/nwtaf/ASC/issues/27
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh # from https://github.com/conda-forge/miniforge/?tab=readme-ov-file#install

# Add source to the .bashrc file to initialize conda
# sudo echo 'export PATH="/home/pi/miniforge3/bin:$PATH"' >> ~/.bashrc
# echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc

# Add conda to the PATH environment variable
# echo "export PATH=~/miniconda3/bin:$PATH" >> ~/.bashrc

# Initialize conda without closing the current shell session
# echo "conda activate base" >> ~/.bashrc # alternate attempt to activate base environment
# . ~/miniconda3/etc/profile.d/conda.sh

# Conda config --set auto_activate_base false # optional, prevents base environment from auto-activating

# Create a conda environment with the required Python version
conda create -n minicondaenv python=3.11 -y

# Activate the newly created conda environment
conda activate minicondaenv

cd ~/Documents

# Git clone the project repository (To login, username is username but pass is token from Github settings>developer settings>Tokens(classic), which is https://github.com/settings/tokens)
# git clone 'https://github.com/username/reponame.git'

# Install dependencies using conda or pip depending on the existence of a requirements.txt file
if [[ -f requirements.txt ]]; then
    conda install --file requirements.txt || pip install -r requirements.txt
else
    echo "No requirements.txt file found. Skipping dependency installation."
fi

echo "Update and environment setup complete."
echo "Please restart the Raspberry Pi to apply changes."

# Restart Raspberry Pi to apply changes
sudo reboot

# good links
# https://help.realvnc.com/hc/en-us/articles/360002249917-RealVNC-Connect-and-Raspberry-Pi#changing-the-raspberry-pi%E2%80%99s-screen-resolution-0-11
# https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi