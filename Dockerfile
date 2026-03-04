# Use a slim Python image to keep the size under 100MB
FROM python:3.11-slim

# Create the app directory
WORKDIR /app

# Copy the binaries and the script
# Ensure TCli and TCli_arm are in the same folder as this Dockerfile
COPY main.py .
COPY TCli .
COPY TCli_arm .

# Ensure the script is executable
RUN chmod +x main.py

# Run as a non-privileged user for better security
# We use /tmp for all writes, so this works perfectly
USER 1000

# Start the wrapper
CMD ["python3", "main.py"]
