# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy source code
COPY . .

# Build the production-ready app
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy the Vite build output
COPY --from=build /app/dist /usr/share/nginx/html

# (Optional) Custom Nginx config for SPA routing
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
