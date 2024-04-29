#!/bin/bash

while true; do
    streamlit run Welcome.py --server.port 8501
    echo "Streamlit has stopped. Attempting to restart in 5 seconds..."
    sleep 5
    # Replace with your actual notification command
    curl -X POST http://example.com/message -d "Streamlit crashed and will restart"
done
