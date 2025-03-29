# Stage 1: Builder
FROM node:16-alpine AS builder

WORKDIR /usr/src/app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application source code
COPY . .

# Stage 2: Tester
FROM builder AS tester
# Instead of RUN, use CMD so the container runs tests when started.
CMD ["npm", "test"]

# Stage 3: Production
FROM node:16-alpine AS production

WORKDIR /usr/src/app
# Copy built code from the builder stage
COPY --from=builder /usr/src/app .

# Expose the application port
EXPOSE 3000

# Run the application
CMD ["node", "main.js"]
