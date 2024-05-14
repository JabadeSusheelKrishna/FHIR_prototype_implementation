#!/bin/bash

# Run command 1 in a new terminal window
gnome-terminal -- python3 central_server.py &

# Run command 2 in a new terminal window
gnome-terminal -- python3 patient_consent.py &
