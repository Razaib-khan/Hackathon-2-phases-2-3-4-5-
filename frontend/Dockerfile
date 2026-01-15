# Use an official Node runtime as a parent image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

# Install serve globally to serve the static files
RUN npm install -g serve

# Set working directory
WORKDIR /app

# Copy the build output from the builder stage
COPY --from=builder /app/out ./out

# Expose port
EXPOSE 3000

# Run the application
CMD ["serve", "-s", "out", "-l", "3000"]