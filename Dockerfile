# Use the official Node.js 12 image.
FROM node:12

# Create and change to the app directory.
WORKDIR /usr/src/app

# Copy package*.json files first for efficient Docker caching.
COPY package*.json ./

# Install production dependencies.
RUN npm install --only=production

# Copy local code to the container image.
COPY . .

# Expose port 9997 for the application.
EXPOSE 9997

# Run the web service on container startup.
CMD [ "node", "app.js" ]