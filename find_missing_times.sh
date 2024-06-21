#!/bin/bash

# Loop over all possible hours and minutes
for hour in $(seq -w 0 23); do
    for minute in $(seq -w 0 59); do
        # Construct the time format
        time_format="${hour}:${minute}"

        # Check if the time format exists in times.csv
        if ! grep -qF "$time_format" times.csv; then
            # If it doesn't exist, print it
            echo "Missing: $time_format"
        fi
    done
done