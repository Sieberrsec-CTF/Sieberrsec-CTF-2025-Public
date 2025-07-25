# Use official Node.js LTS image
FROM node:18

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (adjust if not 3000)
EXPOSE 28576

# Set flag
ENV FLAG=sctf{minesweeper_is_a_very_co0l_gam3}

# Run the app
CMD [ "node", "server.js" ]
