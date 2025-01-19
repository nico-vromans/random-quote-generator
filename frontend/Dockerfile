FROM node:23.6-bookworm-slim

# Set up environment variables for builder
ENV ROOT_DIR="/usr/rqg" \
    APP_DIR="${ROOT_DIR}/app" \
    TZ="Europe/Brussels"

WORKDIR ${APP_DIR}

# Copy and install dependencies
COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps

# Copy the application code (overwritten by bind mount during development)
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Default command to run the Next.js development server
CMD ["npm", "run", "dev"]
