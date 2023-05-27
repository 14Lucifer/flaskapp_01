# Use the official Python image as the base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Install the required dependencies
RUN pip install flask==2.3.2
RUN pip install pyyaml==6.0
RUN mkdir /app/data
RUN mkdir /app/config
RUN mkdir /app/log

# Copy the Flask app code and other necessary files to the container
COPY . .

# Expose the port on which the Flask app will run. 
# Even without mentioning EXPOSE, can still expose container port at runtime using "docker run -p 5000:50000".
# EXPOSE 5000

# Set the environment variables for Flask
ENV FLASK_APP=app.py

# Run the Flask app
ENTRYPOINT [ "python" ]
# --debug can be passed at the runtime as custom cmd.
CMD ["${FLASK_APP}","8080"]
