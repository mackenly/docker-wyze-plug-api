# Start from a base Python 3.9 image
FROM python:3.9

# Set a directory for the app
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables for your username, password, and key
ENV USERNAME=""
ENV PASSWORD=""
ENV TOKEN=""
ENV KEY=""

EXPOSE 5000

# Run the command to start your API
CMD [ "python", "./server.py" ]
