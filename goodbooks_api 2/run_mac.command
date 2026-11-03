#!/bin/bash
# Double-click this file in Finder to run the Good Books API on a Mac.
# First time only: if macOS blocks it, right-click the file > Open > Open.

cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 was not found."
  echo "Install it from https://www.python.org/downloads/macos/ and try again."
  read -r -p "Press Return to close..."
  exit 1
fi

# Private environment for this project, so nothing system-wide changes
if [ ! -d ".venv" ]; then
  echo "Setting up for the first time (this takes a few seconds)..."
  python3 -m venv .venv || { read -r -p "Could not create environment. Press Return to close..."; exit 1; }
fi

source .venv/bin/activate
python3 -m pip install --quiet --upgrade pip >/dev/null 2>&1
python3 -m pip install --quiet -r requirements.txt || {
  echo "Could not install Flask. Check your internet connection."
  read -r -p "Press Return to close..."
  exit 1
}

python3 app.py
