#!/usr/bin/env bash

# Change directory into where email_notifer.py script is located.
echo "Changing into ~/email-notifier."
cd /home/uwcc-admin/email-notifier

# If no venv (python3 virtual environment) exists, then create one.
if [ ! -d "venv" ]
then
    echo "Creating venv python3 virtual environment."
    virtualenv -p python3 venv
fi

# Activate venv.
echo "Activating venv python3 virtual environment."
source venv/bin/activate

# Install PyMySQL using pip.
echo "Install PyMySQL."
pip install PyMySQL

# Run email_notifier.py script.
echo "Running email_notifier.py. Logs Available in notifier.log file."
python email_notifier.py >> notifier.log
