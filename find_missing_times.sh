#!/bin/bash

# Loop over all possible hours and minutes
for hour in $(seq -w 0 23); do
    for minute in $(seq -w 0 59); do
        # Construct the time format
        time_format="${hour}:${minute}"
          echo "Missing: $time_format"
    done
done