#!/bin/bash

# Start server
echo "Starting server"
uvicorn app.main:ap --host 0.0.0.0 --port 8004 --reload