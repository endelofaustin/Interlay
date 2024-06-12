#!/bin/bash

# Set environment variables
export ANDROIDSDK=~/.buildozer/android/platform/android-sdk
export ANDROIDNDK=~/.buildozer/android/platform/android-ndk-r25b
export JAVA_HOME=/opt/homebrew/Cellar/openjdk@11/11.0.23/libexec/openjdk.jdk/Contents/Home

# Clean previous builds
yes | buildozer android clean

# Ensure all dependencies are installed
pip install -r requirements.txt

# Build the app
yes | buildozer android debug

