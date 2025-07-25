FROM php:8.2-cli

# Set working directory
WORKDIR /var/www/html

# Copy index.php into the container
COPY index.php .

# Expose the port the app runs on
EXPOSE 35749

# Set env
ENV FLAG=sctf{php_typ3_juggl1ng_1s_n0_j0k3}

# Start the built-in PHP server
CMD ["php", "-S", "0.0.0.0:35749", "index.php"]
