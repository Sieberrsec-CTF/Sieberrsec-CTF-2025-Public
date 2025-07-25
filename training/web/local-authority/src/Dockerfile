FROM php:8.1.0-cli-alpine3.15

# Copy the application files to the container
COPY . /var/www/local-authority

# Set the working directory
WORKDIR /var/www/local-authority

CMD ["php", "-S", "0.0.0.0:10010"]
