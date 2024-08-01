#!/bin/sh


# Use environment variables if set, otherwise use default values
VALUE=${SERVER_IP}
PORT=9001

# Start uvicorn with the specified host and port
exec uvicorn main:app --host "$VALUE" --port "$PORT"
