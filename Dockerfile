# Set the required python
FROM python:3.10

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./ /code/

# Copy the start script
COPY start-library-service.sh /code/start-library-service.sh

# Ensure the script is executable
RUN chmod +x /code/start-library-service.sh

# Use the script as the entry point
ENTRYPOINT ["/code/start-library-service.sh"]